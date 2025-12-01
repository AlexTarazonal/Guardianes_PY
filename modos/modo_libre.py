import pygame
import sys
import random
import os
from nave import Nave
from objetos import Basura, Animal, PowerUp, Obstaculo
from mapas import dibujar_fondo
from interfaz import (mostrar_puntaje, mostrar_vidas, mostrar_frase, 
                      mostrar_contadores, mostrar_nivel, pantalla_pausa, 
                      pantalla_game_over, mostrar_opciones_libre)
from frases import FRASES_EDUCATIVAS

ANCHO, ALTO = 800, 600
NOMBRES_NIVELES = ['Océano', 'Amazonía', 'Ciudad']

# === Inicializar mixer ===
pygame.mixer.init()

# === Ruta y carga de audios ===
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

def jugar_libre(pantalla):
    # === MENÚ DE CONFIGURACIÓN ===
    nivel = 0
    velocidad_basura = 30
    velocidad_animal = 100
    vidas = 3
    en_config = True
    opcion = 0
    opciones = ["Mapa", "Velocidad Basura", "Velocidad Animal", "Vidas", "Iniciar"]
    
    reloj_config = pygame.time.Clock()
    
    while en_config:
        reloj_config.tick(60)
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
                    if opcion == 0: 
                        nivel = (nivel - 1) % 3
                    elif opcion == 1: 
                        velocidad_basura = max(10, velocidad_basura - 5)
                    elif opcion == 2: 
                        velocidad_animal = max(40, velocidad_animal - 5)
                    elif opcion == 3: 
                        vidas = max(1, vidas - 1)
                elif evento.key == pygame.K_RIGHT:
                    if opcion == 0: 
                        nivel = (nivel + 1) % 3
                    elif opcion == 1: 
                        velocidad_basura = min(50, velocidad_basura + 5)
                    elif opcion == 2: 
                        velocidad_animal = min(200, velocidad_animal + 5)
                    elif opcion == 3: 
                        vidas = min(5, vidas + 1)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    if opcion == 4:
                        en_config = False
                elif evento.key == pygame.K_ESCAPE:
                    return "menu"
    
    # === INICIALIZACIÓN DEL JUEGO LIBRE ===
    FPS = 60
    reloj = pygame.time.Clock()
    puntaje = 0
    
    # Crear nave centrada en la parte inferior
    nave = Nave(ANCHO // 2, ALTO - 80)
    
    # Listas de objetos
    basuras = []
    animales = []
    powerups = []
    obstaculos = []
    
    # Contadores de spawn
    ticks_basura = 0
    ticks_animal = 0
    ticks_power = 0
    ticks_obstaculo = 0
    
    # Variables de juego
    mensaje = ""
    recogidos = 0
    rescatados = 0
    pausado = False
    en_juego = True
    
    # Control de audio educativo
    tiempo_inicio = pygame.time.get_ticks()
    audio_reproducido = False
    
    # === BUCLE PRINCIPAL DEL JUEGO ===
    while en_juego:
        reloj.tick(FPS)
        
        # Dibujar fondo
        dibujar_fondo(pantalla, nivel)
        
        # === EVENTOS ===
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pausado = not pausado
        
        # === PAUSA ===
        if pausado:
            pantalla_pausa(pantalla)
            pygame.display.flip()
            continue
        
        # === MOVIMIENTO DE NAVE ===
        teclas = pygame.key.get_pressed()
        nave.mover(teclas, ANCHO, ALTO)
        
        # === SPAWN DE OBJETOS ===
        ticks_basura += 1
        ticks_animal += 1
        ticks_power += 1
        ticks_obstaculo += 1
        
        if ticks_basura > velocidad_basura:
            x_spawn = random.randint(30, ANCHO - 40)
            basuras.append(Basura(x_spawn, -40, nivel))
            ticks_basura = 0
        
        if ticks_animal > velocidad_animal:
            x_spawn = random.randint(40, ANCHO - 60)
            animales.append(Animal(x_spawn, -40, nivel))
            ticks_animal = 0
        
        if ticks_power > 700:
            x_spawn = random.randint(50, ANCHO - 50)
            powerups.append(PowerUp(x_spawn, -40, nivel))
            ticks_power = 0
        
        if ticks_obstaculo > 320:
            x_spawn = random.randint(40, ANCHO - 50)
            obstaculos.append(Obstaculo(x_spawn, -40, nivel))
            ticks_obstaculo = 0
        
        # === ACTUALIZAR Y DIBUJAR BASURA ===
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
        
        # === ACTUALIZAR Y DIBUJAR ANIMALES ===
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
        
        # === ACTUALIZAR Y DIBUJAR POWER-UPS ===
        for power in powerups[:]:
            power.mover()
            power.dibujar(pantalla)
            
            if nave.rect.colliderect(power.rect):
                powerups.remove(power)
                power.activar(nave)
                mensaje = f"¡Power-up: {power.nombre}!"
            elif power.rect.top > ALTO:
                powerups.remove(power)
        
        # === ACTUALIZAR Y DIBUJAR OBSTÁCULOS ===
        for obstaculo in obstaculos[:]:
            obstaculo.mover()
            obstaculo.dibujar(pantalla)
            
            if nave.rect.colliderect(obstaculo.rect):
                obstaculos.remove(obstaculo)
                vidas -= 1
                mensaje = "¡Cuidado, obstáculo! -1 vida"
            elif obstaculo.rect.top > ALTO:
                obstaculos.remove(obstaculo)
        
        # === DIBUJAR NAVE ===
        nave.dibujar(pantalla)
        
        # === INTERFAZ ===
        mostrar_puntaje(pantalla, puntaje)
        mostrar_vidas(pantalla, vidas)
        mostrar_frase(pantalla, mensaje)
        mostrar_contadores(pantalla, recogidos, rescatados)
        mostrar_nivel(pantalla, nivel, NOMBRES_NIVELES[nivel])
        
        # === AUDIO EDUCATIVO ===
        tiempo_actual = pygame.time.get_ticks()
        if not audio_reproducido and tiempo_actual - tiempo_inicio >= 5000:
            try:
                audio = random.choice(AUDIOS)
                audio.play()
                audio_reproducido = True
            except:
                pass  # Si hay error con audio, continuar sin él
        
        # === GAME OVER ===
        if vidas <= 0:
            pantalla_game_over(pantalla, puntaje, recogidos, rescatados, 
                             random.choice(FRASES_EDUCATIVAS))
            pygame.display.flip()
            
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
            return "menu"
        
        pygame.display.flip()
    
    return "menu"