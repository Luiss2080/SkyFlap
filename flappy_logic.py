"""Lógica pura de Flappy Bird (sin pygame): física, tubos, colisiones y puntaje.

Todo lo que se puede probar sin abrir una ventana vive aquí; ``Final6.py``
solo dibuja y lee el teclado.
"""
import random
from typing import Optional, Tuple

ANCHO = 500
ALTO = 700

# Sprites (px)
ANCHO_PAJARO = 60
ALTO_PAJARO = 43
ANCHO_TUBO = 50
ALTO_IMAGEN_TUBO = 500

# Física original: 25 pasos por segundo (fps.tick(25) en las versiones previas).
PASOS_POR_SEGUNDO = 25
GRAVEDAD = 1 * PASOS_POR_SEGUNDO * PASOS_POR_SEGUNDO  # px/s^2 (1 px/paso^2)
SALTO = -30 * PASOS_POR_SEGUNDO                       # px/s (impulso, -30 px/paso)
AMORTIGUACION = 0.95                                  # por paso de 1/25 s
VELOCIDAD_TUBO = 10 * PASOS_POR_SEGUNDO               # px/s (10 px/paso)

# Tubos
X_INICIAL_TUBO = 700
X_REINICIO_TUBO = -20
HUECO = 200          # separación vertical fija entre tubo superior e inferior
MARGEN_HUECO = 100   # distancia mínima del hueco al techo y al suelo


def actualizar_velocidad(velocidad: float, dt: float) -> float:
    """Aplica gravedad y amortiguación durante ``dt`` segundos.

    Equivale a ``v += 1; v *= 0.95`` a 25 pasos/s, pero independiente de la
    tasa de cuadros real.
    """
    velocidad += GRAVEDAD * dt
    velocidad *= AMORTIGUACION ** (dt * PASOS_POR_SEGUNDO)
    return velocidad


def generar_hueco(rng: Optional[random.Random] = None) -> Tuple[int, int]:
    """Devuelve ``(y_superior, y_inferior)`` del hueco: borde inferior del
    tubo de arriba y borde superior del tubo de abajo.

    El hueco mide siempre ``HUECO`` px y queda a ``MARGEN_HUECO`` px de techo
    y suelo, de modo que el pájaro (43 px) siempre puede pasar.
    """
    rng = rng or random
    y_sup = rng.randint(MARGEN_HUECO, ALTO - MARGEN_HUECO - HUECO)
    return y_sup, y_sup + HUECO


def rects_tubo(x_tubo: float, hueco: Tuple[int, int]):
    """Rectángulos ``(x, y, ancho, alto)`` de los tubos superior e inferior."""
    y_sup, y_inf = hueco
    superior = (x_tubo, y_sup - ALTO_IMAGEN_TUBO, ANCHO_TUBO, ALTO_IMAGEN_TUBO)
    inferior = (x_tubo, y_inf, ANCHO_TUBO, ALTO_IMAGEN_TUBO)
    return superior, inferior


def _solapan(a, b) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def colision_tubo(x_tubo: float, hueco: Tuple[int, int],
                  x_pajaro: float, y_pajaro: float) -> bool:
    """True si el pájaro toca el tubo superior o el inferior."""
    pajaro = (x_pajaro, y_pajaro, ANCHO_PAJARO, ALTO_PAJARO)
    return any(_solapan(pajaro, t) for t in rects_tubo(x_tubo, hueco))


def colision_bordes(y_pajaro: float) -> bool:
    """True si el pájaro toca el techo o el suelo."""
    return y_pajaro <= 0 or y_pajaro + ALTO_PAJARO >= ALTO


def limitar_a_pantalla(y_pajaro: float, velocidad: float) -> Tuple[float, float]:
    """Mantiene el pájaro dentro de la pantalla (su sprite completo)."""
    maximo = ALTO - ALTO_PAJARO
    if y_pajaro >= maximo:
        return maximo, 0.0
    if y_pajaro <= 0:
        return 0.0, 0.0
    return y_pajaro, velocidad


def tubo_superado(x_tubo: float, x_pajaro: float) -> bool:
    """True cuando el borde derecho del tubo ya quedó detrás del pájaro."""
    return x_tubo + ANCHO_TUBO < x_pajaro


def mover_tubo(x_tubo: float, dt: float) -> Tuple[float, bool]:
    """Avanza el tubo; devuelve ``(nueva_x, reinicio)``.

    ``reinicio`` es True cuando salió por la izquierda y reaparece a la derecha.
    """
    x_tubo -= VELOCIDAD_TUBO * dt
    if x_tubo < X_REINICIO_TUBO:
        return float(X_INICIAL_TUBO), True
    return x_tubo, False
