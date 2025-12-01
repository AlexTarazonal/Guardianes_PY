import datetime
import pygame
import sys
import random
import os
from nave import Nave
from objetos import Basura, Animal, PowerUp, Obstaculo
from mapas import dibujar_fondo
from interfaz import mostrar_puntaje, mostrar_vidas, mostrar_frase, mostrar_contadores, mostrar_nivel, pantalla_pausa, pantalla_game_over, pantalla_victoria
from frases import FRASES_EDUCATIVAS

ANCHO, ALTO = 800, 600
NOMBRES_NIVELES = ['Océano', 'Amazonía', 'Ciudad']

def siguiente_nivel(nivel_actual):
    return (nivel_actual + 1) % 3

# === Asegúrate de inicializar el mixer ===
pygame.mixer.init()

# === Prepara audios con ruta absoluta ===
RUTA_BASE = os.path.dirname(__file__)
AUDIO_RUTA = os.path.join(RUTA_BASE, "..", "assets", "audios")

AUDIOS = [
    pygame.mixer.Sound(os.path.join(AUDIO_RUTA, "frase1.wav")),
    pygame.mixer.Sound(os.path.join(AUDIO_RUTA, "frase2.wav")),
    pygame.mixer.Sound(os.path.join(AUDIO_RUTA, "frase3.wav")),
    pygame.mixer.Sound(os.path.join(AUDIO_RUTA, "frase4.wav")),
    pygame.mixer.Sound(os.path.join(AUDIO_RUTA, "frase5.wav")),
    pygame.mixer.Sound(os.path.join(AUDIO_RUTA, "frase6.wav"))
]

def jugar_campaña(pantalla, nickname):
    pygame.display.set_caption("Modo Campaña - Guardianes del Planeta")
    FPS = 60
    reloj = pygame.time.Clock()
    nivel = 0
    puntaje = 0
    vidas = 3
    nave = Nave(ANCHO // 2, ALTO - 80)
    basuras, animales, powerups, obstaculos = [], [], [], []
    ticks_basura, ticks_animal, ticks_power, ticks_obstaculo = 0, 0, 0, 0
    mensaje = ""
    recogidos, rescatados = 0, 0
    pausado = False
    en_juego = True

    UMBRALES_NIVEL = [250, 500, 750]
    umbral_idx = 0

    tiempo_inicio = pygame.time.get_ticks()
    audio_reproducido = False

    while en_juego:
        reloj.tick(FPS)
        dibujar_fondo(pantalla, nivel)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pausado = not pausado

        if pausado and vidas > 0:
            pantalla_pausa(pantalla)
            pygame.display.flip()
            continue

        teclas = pygame.key.get_pressed()
        nave.mover(teclas, ANCHO, ALTO)

        ticks_basura += 1
        ticks_animal += 1
        ticks_power += 1
        ticks_obstaculo += 1

        if ticks_basura > max(20, 40 - nivel * 6):
            basuras.append(Basura(random.randint(30, ANCHO - 40), -40, nivel))
            ticks_basura = 0
        if ticks_animal > max(60, 130 - nivel * 10):
            animales.append(Animal(random.randint(40, ANCHO - 60), -40, nivel))
            ticks_animal = 0
        if ticks_power > 600:
            powerups.append(PowerUp(random.randint(50, ANCHO - 50), -40, nivel))
            ticks_power = 0
        if ticks_obstaculo > 280:
            obstaculos.append(Obstaculo(random.randint(40, ANCHO - 50), -40, nivel))
            ticks_obstaculo = 0

        for basura in basuras[:]:
            basura.mover()
            basura.dibujar(pantalla)
            if nave.rect.colliderect(basura.rect):
                basuras.remove(basura)
                puntaje += 10
                recogidos += 1
                mensaje = "¡Recolectaste basura! +10"
            elif basura.rect.top > ALTO:
                basuras.remove(basura)
                vidas -= 1
                mensaje = "Dejaste pasar basura... -1 vida"

        for animal in animales[:]:
            animal.mover()
            animal.dibujar(pantalla)
            if nave.rect.colliderect(animal.rect):
                animales.remove(animal)
                puntaje += 20
                rescatados += 1
                mensaje = "¡Rescataste un animal! +20"
            elif animal.rect.top > ALTO:
                animales.remove(animal)
                mensaje = "Un animal se escapó..."

        for power in powerups[:]:
            power.mover()
            power.dibujar(pantalla)
            if nave.rect.colliderect(power.rect):
                powerups.remove(power)
                power.activar(nave)
                mensaje = f"¡Power-up: {power.nombre}!"

        for obstaculo in obstaculos[:]:
            obstaculo.mover()
            obstaculo.dibujar(pantalla)
            if nave.rect.colliderect(obstaculo.rect):
                obstaculos.remove(obstaculo)
                vidas -= 1
                mensaje = "¡Cuidado, obstáculo! -1 vida"

        nave.dibujar(pantalla)
        mostrar_puntaje(pantalla, puntaje)
        mostrar_vidas(pantalla, vidas)
        mostrar_frase(pantalla, mensaje)
        mostrar_contadores(pantalla, recogidos, rescatados)
        mostrar_nivel(pantalla, nivel, NOMBRES_NIVELES[nivel])

        tiempo_actual = pygame.time.get_ticks()
        if not audio_reproducido and tiempo_actual - tiempo_inicio >= 5000:
            audio = random.choice(AUDIOS)
            audio.play()
            audio_reproducido = True

        if umbral_idx < len(UMBRALES_NIVEL) and puntaje >= UMBRALES_NIVEL[umbral_idx]:
            nivel = siguiente_nivel(nivel)
            mensaje = f"Nivel: {NOMBRES_NIVELES[nivel]} — {random.choice(FRASES_EDUCATIVAS)}"
            basuras.clear()
            animales.clear()
            powerups.clear()
            obstaculos.clear()
            umbral_idx += 1
            pygame.display.flip()
            pygame.time.wait(1200)
            tiempo_inicio = pygame.time.get_ticks()
            audio_reproducido = False

        if puntaje >= 1000:
            pantalla_victoria(pantalla, puntaje, recogidos, rescatados)
            pygame.display.flip()
            guardar_puntaje(nickname, puntaje)
            esperando = True
            while esperando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_r:
                            return "reiniciar"
                        elif evento.key == pygame.K_ESCAPE:
                            return "menu"
                pygame.time.wait(20)
            return

        if vidas <= 0:
            pantalla_game_over(pantalla, puntaje, recogidos, rescatados, random.choice(FRASES_EDUCATIVAS))
            pygame.display.flip()
            guardar_puntaje(nickname, puntaje)
            esperando = True
            while esperando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_r:
                            return "reiniciar"
                        elif evento.key == pygame.K_ESCAPE:
                            return "menu"
                pygame.time.wait(20)
            return

        pygame.display.flip()

def guardar_puntaje(nickname, puntaje):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("puntajes.txt", "a") as f:
        f.write(f"{nickname},{puntaje},{fecha}\n")
