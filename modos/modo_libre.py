import pygame
import sys
import random
from nave import Nave
from objetos import Basura, Animal, PowerUp, Obstaculo
from mapas import dibujar_fondo
from interfaz import mostrar_puntaje, mostrar_vidas, mostrar_frase, mostrar_contadores, mostrar_nivel, pantalla_pausa, pantalla_game_over, mostrar_opciones_libre
from frases import FRASES_EDUCATIVAS

ANCHO, ALTO = 800, 600
NOMBRES_NIVELES = ['Océano', 'Amazonía', 'Ciudad']

def jugar_libre(pantalla):
    # Menú de configuración
    nivel = 0  # 0: Océano, 1: Amazonas, 2: Lima
    velocidad_basura = 30
    velocidad_animal = 100
    vidas = 3
    en_config = True
    opcion = 0
    opciones = ["Mapa", "Velocidad Basura", "Velocidad Animal", "Vidas", "Iniciar"]

    while en_config:
        pantalla.fill((80, 100, 150))
        mostrar_opciones_libre(pantalla, nivel, velocidad_basura, velocidad_animal, vidas, opcion)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcion = (opcion + 1) % len(opciones)
                elif evento.key == pygame.K_UP:
                    opcion = (opcion - 1) % len(opciones)
                elif evento.key == pygame.K_LEFT:
                    if opcion == 0: nivel = (nivel - 1) % 3
                    if opcion == 1: velocidad_basura = max(10, velocidad_basura - 5)
                    if opcion == 2: velocidad_animal = max(40, velocidad_animal - 5)
                    if opcion == 3: vidas = max(1, vidas - 1)
                elif evento.key == pygame.K_RIGHT:
                    if opcion == 0: nivel = (nivel + 1) % 3
                    if opcion == 1: velocidad_basura = min(50, velocidad_basura + 5)
                    if opcion == 2: velocidad_animal = min(200, velocidad_animal + 5)
                    if opcion == 3: vidas = min(5, vidas + 1)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    if opcion == 4:
                        en_config = False
        pygame.time.wait(90)

    # Lógica de juego infinita en el mapa elegido
    FPS = 60
    reloj = pygame.time.Clock()
    puntaje = 0
    nave = Nave(ANCHO // 2, ALTO - 80)
    basuras, animales, powerups, obstaculos = [], [], [], []
    ticks_basura, ticks_animal, ticks_power, ticks_obstaculo = 0, 0, 0, 0
    mensaje = ""
    recogidos, rescatados = 0, 0
    pausado = False
    en_juego = True

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

        if pausado:
            pantalla_pausa(pantalla)
            pygame.display.flip()
            continue

        teclas = pygame.key.get_pressed()
        nave.mover(teclas, ANCHO, ALTO)

        # Generar objetos
        ticks_basura += 1
        ticks_animal += 1
        ticks_power += 1
        ticks_obstaculo += 1

        if ticks_basura > velocidad_basura:
            basuras.append(Basura(random.randint(30, ANCHO - 40), -40, nivel))
            ticks_basura = 0
        if ticks_animal > velocidad_animal:
            animales.append(Animal(random.randint(40, ANCHO - 60), -40, nivel))
            ticks_animal = 0
        if ticks_power > 700:
            powerups.append(PowerUp(random.randint(50, ANCHO - 50), -40, nivel))
            ticks_power = 0
        if ticks_obstaculo > 320:
            obstaculos.append(Obstaculo(random.randint(40, ANCHO - 50), -40, nivel))
            ticks_obstaculo = 0

        # Objetos (igual que en campaña)
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

        if vidas <= 0:
            pantalla_game_over(pantalla, puntaje, recogidos, rescatados, random.choice(FRASES_EDUCATIVAS))
            pygame.display.flip()
            pygame.time.wait(4000)
            return

        pygame.display.flip()
