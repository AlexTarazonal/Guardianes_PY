import pygame

class Nave:
    def __init__(self, x, y):
        self.imagen = pygame.Surface((60, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.imagen, (40, 200, 90), [(0,40),(30,0),(60,40)])
        self.rect = self.imagen.get_rect(center=(x, y))
        self.vel = 7

    def mover(self, teclas, ancho, alto):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT] and self.rect.right < ancho:
            self.rect.x += self.vel
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.vel
        if teclas[pygame.K_DOWN] and self.rect.bottom < alto:
            self.rect.y += self.vel

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
