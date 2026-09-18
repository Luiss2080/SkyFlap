import random

import pytest

import flappy_logic as L


def simular(dt, segundos, v=0.0, y=0.0):
    t = 0.0
    while t < segundos - 1e-9:
        v = L.actualizar_velocidad(v, dt)
        y += v * dt
        t += dt
    return y, v


def test_fisica_a_25_pasos_iguala_formula_original():
    v = 0.0
    y = 0.0
    for _ in range(25):  # 1 s con el bucle original: v+=1; v*=0.95; y+=v
        v = (v + 1) * 0.95
        y += v
    y2, v2 = simular(1 / 25, 1.0)
    assert y2 == pytest.approx(y, rel=1e-9)
    assert v2 / 25 == pytest.approx(v, rel=1e-9)


def test_fisica_casi_independiente_del_dt():
    y25, _ = simular(1 / 25, 1.0)
    y100, _ = simular(1 / 100, 1.0)
    assert y100 == pytest.approx(y25, rel=0.05)


def test_hueco_tamano_fijo_y_dentro_de_margenes():
    rng = random.Random(1)
    for _ in range(2000):
        sup, inf = L.generar_hueco(rng)
        assert inf - sup == L.HUECO
        assert sup >= L.MARGEN_HUECO
        assert inf <= L.ALTO - L.MARGEN_HUECO
        assert inf - sup > L.ALTO_PAJARO


def test_pajaro_pasa_por_el_centro_del_hueco():
    hueco = (250, 450)
    assert not L.colision_tubo(100, hueco, 100, 250 + 78)


def test_colision_con_tubo_superior_e_inferior():
    hueco = (250, 450)
    assert L.colision_tubo(100, hueco, 100, 240)        # roza arriba
    assert L.colision_tubo(100, hueco, 100, 420)        # 420+43 > 450
    assert L.colision_tubo(100, hueco, 100, 100)        # dentro del tubo superior


def test_sin_colision_cuando_el_tubo_esta_lejos():
    hueco = (250, 450)
    assert not L.colision_tubo(400, hueco, 100, 100)
    assert not L.colision_tubo(-100, hueco, 100, 100)


def test_tocar_borde_no_cuenta_como_solape():
    hueco = (250, 450)
    # pájaro a la izquierda pegado al tubo: borde derecho == borde izquierdo
    assert not L.colision_tubo(160, hueco, 100, 100)
    assert L.colision_tubo(159, hueco, 100, 100)


def test_bordes_techo_y_suelo():
    assert L.colision_bordes(0)
    assert L.colision_bordes(-5)
    assert L.colision_bordes(L.ALTO - L.ALTO_PAJARO)
    assert not L.colision_bordes(300)


def test_limitar_a_pantalla_mantiene_sprite_visible():
    assert L.limitar_a_pantalla(900, 50) == (L.ALTO - L.ALTO_PAJARO, 0.0)
    assert L.limitar_a_pantalla(-10, -50) == (0.0, 0.0)
    assert L.limitar_a_pantalla(300, 12) == (300, 12)


def test_tubo_superado_solo_cuando_pasa_al_pajaro():
    assert not L.tubo_superado(100, 100)
    assert not L.tubo_superado(50, 100)   # borde derecho == x pájaro
    assert L.tubo_superado(49, 100)


def test_puntaje_una_vez_por_tubo():
    """Reproduce el bucle del juego: un tubo completo suma exactamente 1."""
    x, contado, puntaje = float(L.X_INICIAL_TUBO), False, 0
    for _ in range(400):
        x, reinicio = L.mover_tubo(x, 1 / 60)
        if reinicio:
            contado = False
        elif not contado and L.tubo_superado(x, 100):
            contado = True
            puntaje += 1
        if reinicio:
            break
    assert puntaje == 1


def test_mover_tubo_reinicia_a_la_derecha():
    x, reinicio = L.mover_tubo(-19, 1 / 25)
    assert reinicio and x == L.X_INICIAL_TUBO
    x, reinicio = L.mover_tubo(300, 1 / 25)
    assert not reinicio and x == pytest.approx(290)


def test_salto_sube_al_pajaro():
    v = L.actualizar_velocidad(0.0, 1 / 60) + L.SALTO
    assert v < 0
