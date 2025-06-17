import pygame
import random

def dibujar_amazonas(pantalla):
    pantalla.fill((32, 110, 40))
    # Río
    pygame.draw.ellipse(pantalla, (40, 180, 250), (90, 390, 620, 120))
    # Árboles (tronco + copa)
    for x in range(80, 800, 150):
        pygame.draw.rect(pantalla, (90, 50, 20), (x, 340, 15, 50))
        pygame.draw.ellipse(pantalla, (50, 200, 70), (x-15, 320, 50, 35))
    # Plantas menores
    for _ in range(10):
        x = random.randint(0, 800)
        y = random.randint(500, 590)
        pygame.draw.ellipse(pantalla, (30, 160, 40), (x, y, 40, 12))
    # Lianas
    for x in range(0, 800, 120):
        pygame.draw.arc(pantalla, (25, 80, 20), (x, 60, 80, 120), 0, 3.14, 3)

def dibujar_oceano(pantalla):
    pantalla.fill((10, 60, 170))
    # Ondas del mar
    for y in range(100, 600, 60):
        pygame.draw.arc(pantalla, (80, 180, 255), (0, y, 800, 50), 0, 3.14, 2)
    # Islas y rocas
    pygame.draw.ellipse(pantalla, (180, 180, 90), (110, 430, 60, 24))
    pygame.draw.ellipse(pantalla, (120, 120, 70), (600, 370, 40, 15))
    # Alguitas
    for x in range(100, 800, 140):
        pygame.draw.line(pantalla, (30, 160, 80), (x, 600), (x, 570), 3)
        pygame.draw.line(pantalla, (50, 220, 110), (x+10, 600), (x+5, 580), 2)

def dibujar_lima(pantalla):
    pantalla.fill((190, 190, 190))
    # Calles
    for x in range(0, 800, 100):
        pygame.draw.rect(pantalla, (160, 160, 160), (x+40, 0, 20, 600))
    for y in range(0, 600, 100):
        pygame.draw.rect(pantalla, (170, 170, 170), (0, y+40, 800, 20))
    # Edificios
    for x in range(40, 800, 130):
        alto = random.randint(60, 140)
        pygame.draw.rect(pantalla, (100, 120, 170), (x, 400-alto, 50, alto))
        # Ventanas
        for v in range(4):
            pygame.draw.rect(pantalla, (220, 220, 240), (x+8, 410-alto+v*25, 12, 12))

def dibujar_fondo(pantalla, nivel):
    if nivel == 0:
        dibujar_amazonas(pantalla)
    elif nivel == 1:
        dibujar_oceano(pantalla)
    elif nivel == 2:
        dibujar_lima(pantalla)
