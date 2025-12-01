import pygame
import random
import os

pygame.mixer.init()

# Ruta base ABSOLUTA a la carpeta de audios
RUTA_AUDIOS = os.path.join(
    os.path.dirname(__file__), "assets", "audios"
)

# Lista de frases
AUDIOS_FRASES = [
    os.path.join(RUTA_AUDIOS, f"frase{i}.wav")
    for i in range(1, 7)
]

def reproducir_frase_aleatoria():
    frase = random.choice(AUDIOS_FRASES)
    sonido = pygame.mixer.Sound(frase)
    sonido.set_volume(0.7)  # volumen (0.0 a 1.0)
    sonido.play()
