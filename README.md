# SkyFlap

Recreación de Flappy Bird en Python con [pygame](https://www.pygame.org/), construida paso a paso como ejercicio de aprendizaje. El repositorio conserva las etapas intermedias del desarrollo y una versión final jugable (`Final6.py`).

## Qué hace la versión final (`Final6.py`)

- Un pájaro que salta con la barra espaciadora y cae por gravedad.
- Un tubo a la vez que avanza de derecha a izquierda; el hueco tiene siempre 200 px y su altura es aleatoria.
- Tres vidas: cada tubo golpeado, y cada contacto con techo o suelo, cuesta una vida. Con 0 vidas el juego termina y muestra el puntaje en la consola.
- Puntaje: 1 punto por tubo superado.
- Cronómetro, puntaje y corazones de vida en pantalla.
- Sonidos de salto, colisión y paso de obstáculo, más música de fondo. Sin dispositivo de audio el juego corre en silencio.

## Etapas del desarrollo

| Archivo | Contenido |
|---|---|
| `Logica, imagen1.py` | Física básica, tubos e imágenes |
| `Colision2.py` | Detección de colisión |
| `Sonidos3.py` | Sonidos y música |
| `Cronometro4.py` | Cronómetro en pantalla |
| `vidas5.py` | Sistema de vidas |
| `Final6.py` | Versión final, usa `flappy_logic.py` |

Las etapas 1 a 5 son históricas: se dejan tal cual, dependen del directorio de trabajo (ejecutar desde la raíz del repositorio) y conservan los errores de la versión original.

`flappy_logic.py` contiene la lógica pura (física, generación del hueco, colisiones, puntaje) sin depender de pygame, para poder probarla.

## Instalación y ejecución

Requiere Python 3.9 o superior.

```bash
pip install -r requirements.txt
python Final6.py
```

Controles: `Espacio` salta; cerrar la ventana sale.

## Pruebas

```bash
pip install -r requirements-dev.txt
python -m pytest
```

En un entorno sin pantalla ni audio: `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m pytest`. GitHub Actions ejecuta lo mismo en cada push y pull request.

## Limitaciones conocidas

- Las imágenes de `Imagenes/` incluyen fondos (`FondoAmarillo`, `FondoNormal`, `FondoRojo`) y pájaros (`PajaroAmarillo`, `PajaroAzul`, `PajaroGris`, `PajaroRosa`) alternativos y un `Restart.png`, pero **el código no los usa**: no hay selección de escenarios ni de pájaros, ni pantalla de reinicio. Al terminar, el juego se cierra.
- No hay puntuación máxima persistente; el puntaje solo se imprime en la consola.
- Solo hay un tubo en pantalla a la vez.
- Los saltos se suman a la velocidad actual (comportamiento original), por lo que pulsar muy rápido acumula impulso.
- Las colisiones usan rectángulos del tamaño del sprite (60x43 el pájaro, 50 px de ancho los tubos); no son pixel-perfect.
- Las pruebas cubren la lógica pura y la carga de recursos; el bucle gráfico no se prueba automáticamente.
- El archivo `FondoAmarillo.mp3` se usa como música en todas las etapas; `FondoNormal.mp3` y `FondoVioleta.mp3` no se usan.

## Licencia

Este repositorio no incluye un archivo de licencia. Sin licencia explícita, todos los derechos quedan reservados por su autor. Las imágenes y sonidos tampoco declaran su origen ni licencia.
