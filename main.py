import pygame
import sys
from interfaz import (
    inicializar_interfaz, dibujar_menu_completo, 
    obtener_dimensiones_pantalla
)
# Importar los modos de juego
from modos.modo_campaña import jugar_campaña
from modos.modo_libre import jugar_libre
from modos.modo_educativo import jugar_educativo

pygame.init()

# Obtener dimensiones desde interfaz
ANCHO, ALTO = obtener_dimensiones_pantalla()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🌍 Guardianes del Planeta - Aventura Ecológica Peruana")

def main():
    # Inicializar interfaz
    inicializar_interfaz()
    
    seleccion = 0  # 0: Campaña, 1: Libre, 2: Educativo
    en_menu = True
    clock = pygame.time.Clock()
    tiempo_animacion = 0
    
    while en_menu:
        tiempo_animacion += 1
        
        # Dibujar todo el menú desde interfaz.py
        dibujar_menu_completo(pantalla, seleccion, tiempo_animacion)
        pygame.display.flip()
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % 3
                elif evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % 3
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    en_menu = False
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        clock.tick(60)  # 60 FPS para animaciones suaves
    
    # Ejecutar modo seleccionado
    if seleccion == 0:
        jugar_campaña(pantalla)
    elif seleccion == 1:
        jugar_libre(pantalla)
    elif seleccion == 2:
        jugar_educativo(pantalla)

if __name__ == "__main__":
    main()