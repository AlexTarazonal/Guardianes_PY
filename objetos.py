import pygame
import random

COLORES_BASURA = [(150,150,150), (80,80,180), (120,60,30)]
COLORES_ANIMALES = [(230,230,80), (180,80,230), (60,200,180)]

class Basura:
    def __init__(self, x, y, nivel):
        self.imagen = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self.imagen, random.choice(COLORES_BASURA), (4,8,24,16))
        pygame.draw.circle(self.imagen, (200,200,200), (16,8), 6, 2)
        self.rect = self.imagen.get_rect(center=(x, y))
        self.vel = 3 + nivel

    def mover(self):
        self.rect.y += self.vel

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class Animal:
    def __init__(self, x, y, nivel):
        self.imagen = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.ellipse(self.imagen, random.choice(COLORES_ANIMALES), (4,8,28,20))
        pygame.draw.circle(self.imagen, (255,255,255), (30,16), 5)
        self.rect = self.imagen.get_rect(center=(x, y))
        self.vel = 2 + nivel

    def mover(self):
        self.rect.y += self.vel

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
class PowerUp:
    def __init__(self, x, y, nivel):
        self.nombre = random.choice(["Velocidad", "Escudo", "Imán"])
        self.color = {"Velocidad": (30, 160, 250), "Escudo": (250, 230, 50), "Imán": (80, 255, 100)}[self.nombre]
        self.imagen = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(self.imagen, self.color, (16, 16), 15)
        self.rect = self.imagen.get_rect(center=(x, y))
        self.vel = 3 + nivel

    def mover(self):
        self.rect.y += self.vel

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def activar(self, nave):
        # Aplica el efecto, aquí solo ejemplo
        # Puedes mejorar: aumentar velocidad, proteger nave, etc
        pass

class Obstaculo:
    def __init__(self, x, y, nivel):
        colores = [(90, 60, 30), (10,10,10), (40,40,40)]
        self.color = colores[nivel % len(colores)]
        self.imagen = pygame.Surface((36, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.imagen, self.color, (0,0,36,20))
        self.rect = self.imagen.get_rect(center=(x, y))
        self.vel = 3 + nivel

    def mover(self):
        self.rect.y += self.vel

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)