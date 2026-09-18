import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_assets_existen():
    import Final6

    for partes in [("Imagenes", "FondoVioleta.png"), ("Imagenes", "bird.png"),
                   ("Imagenes", "pipe_top.png"), ("Imagenes", "pipe_bot.png"),
                   ("Imagenes", "Corazones.png"),
                   ("Imagenes", "Sonidos", "Salto.wav"),
                   ("Imagenes", "Sonidos", "PasarObstaculo.wav"),
                   ("Imagenes", "Sonidos", "Colision.wav"),
                   ("Imagenes", "Sonidos", "FondoAmarillo.mp3")]:
        assert os.path.isfile(Final6.ruta(*partes)), partes


def test_sin_dispositivo_de_audio_no_falla(monkeypatch):
    monkeypatch.setenv("SDL_AUDIODRIVER", "controlador_inexistente")
    import pygame

    import Final6

    pygame.mixer.quit()
    salto, pasar, fallo = Final6.iniciar_audio()
    salto.play(); pasar.play(); fallo.play()  # no lanzan
