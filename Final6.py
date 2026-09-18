import os

import pygame

import flappy_logic as logica

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FPS = 60


def ruta(*partes):
    return os.path.join(BASE_DIR, *partes)


class SonidoNulo:
    """Sustituto silencioso cuando no hay dispositivo de audio."""

    def play(self, *args, **kwargs):
        pass


def iniciar_audio():
    """Devuelve (salto, pasar, fallo). Sin audio disponible, el juego sigue mudo."""
    try:
        pygame.mixer.init()
        salto = pygame.mixer.Sound(ruta("Imagenes", "Sonidos", "Salto.wav"))
        pasar = pygame.mixer.Sound(ruta("Imagenes", "Sonidos", "PasarObstaculo.wav"))
        fallo = pygame.mixer.Sound(ruta("Imagenes", "Sonidos", "Colision.wav"))
        pygame.mixer.music.load(ruta("Imagenes", "Sonidos", "FondoAmarillo.mp3"))
        pygame.mixer.music.play(-1)  # Repetir música de fondo
        return salto, pasar, fallo
    except (pygame.error, FileNotFoundError) as error:
        print(f"Audio desactivado: {error}")
        nulo = SonidoNulo()
        return nulo, nulo, nulo


def main():
    pygame.init()
    superficie_juego = pygame.display.set_mode((logica.ANCHO, logica.ALTO))
    imagen_fondo = pygame.image.load(ruta("Imagenes", "FondoVioleta.png")).convert()
    imagen_pajaro = pygame.image.load(ruta("Imagenes", "bird.png")).convert_alpha()
    tubo_superior = pygame.image.load(ruta("Imagenes", "pipe_top.png")).convert_alpha()
    tubo_inferior = pygame.image.load(ruta("Imagenes", "pipe_bot.png")).convert_alpha()
    imagen_corazon = pygame.transform.scale(
        pygame.image.load(ruta("Imagenes", "Corazones.png")).convert_alpha(), (15, 15))
    fuente = pygame.font.Font(None, 36)
    reloj = pygame.time.Clock()
    sonido_salto, sonido_pasar, sonido_fallo = iniciar_audio()

    puntaje = 0
    vidas = 3
    tiempo_inicio = pygame.time.get_ticks()
    x_pajaro, y_pajaro = 100.0, 350.0
    velocidad = 0.0

    x_tubo = float(logica.X_INICIAL_TUBO)
    hueco = logica.generar_hueco()
    tubo_contado = False   # el tubo actual ya sumó punto
    tubo_golpeado = False  # el tubo actual ya quitó una vida
    en_borde = False       # el pájaro está tocando techo/suelo

    ejecutando = True
    while ejecutando:
        # dt en segundos, acotado para que una pausa larga no "teletransporte" objetos
        dt = min(reloj.tick(FPS) / 1000.0, 0.05)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                velocidad += logica.SALTO
                sonido_salto.play()

        velocidad = logica.actualizar_velocidad(velocidad, dt)
        y_pajaro += velocidad * dt

        x_tubo, reinicio = logica.mover_tubo(x_tubo, dt)
        if reinicio:
            hueco = logica.generar_hueco()
            tubo_contado = False
            tubo_golpeado = False
        elif not tubo_contado and logica.tubo_superado(x_tubo, x_pajaro):
            tubo_contado = True
            puntaje += 1
            sonido_pasar.play()

        # Colisiones: cada tubo y cada contacto con un borde cuestan una sola vida
        golpe = False
        if not tubo_golpeado and logica.colision_tubo(x_tubo, hueco, x_pajaro, y_pajaro):
            tubo_golpeado = True
            golpe = True
        toca_borde = logica.colision_bordes(y_pajaro)
        if toca_borde and not en_borde:
            golpe = True
        en_borde = toca_borde
        y_pajaro, velocidad = logica.limitar_a_pantalla(y_pajaro, velocidad)

        if golpe:
            sonido_fallo.play()
            vidas -= 1
            print(f"¡Colisión! Vidas restantes: {vidas}")
            if vidas <= 0:
                print(f"¡Fin del juego! Puntaje final: {puntaje}")
                ejecutando = False

        superficie_juego.blit(imagen_fondo, (0, 0))
        superior, inferior = logica.rects_tubo(x_tubo, hueco)
        superficie_juego.blit(tubo_superior, (superior[0], superior[1]))
        superficie_juego.blit(tubo_inferior, (inferior[0], inferior[1]))
        superficie_juego.blit(imagen_pajaro, (int(x_pajaro), int(y_pajaro)))

        segundos = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        superficie_juego.blit(
            fuente.render(f"Tiempo: {segundos}s  Puntos: {puntaje}", True, (255, 255, 255)),
            (10, 10))
        for i in range(vidas):
            superficie_juego.blit(imagen_corazon, (logica.ANCHO - 30 - i * 20, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
