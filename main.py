import pygame
import sys
import os

from interfaz import (
    inicializar_interfaz,
    dibujar_menu_completo,
    obtener_dimensiones_pantalla,
)
from modos.modo_campaña import jugar_campaña
from modos.modo_libre import jugar_libre
from modos.modo_educativo import jugar_educativo
from ranking import mostrar_ranking
from opengl_demo import ejecutar_demo_opengl

pygame.init()

ANCHO, ALTO = obtener_dimensiones_pantalla()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🌍 Guardianes del Planeta - Aventura Ecológica Peruana")

# Fuentes
fuente_titulo = pygame.font.SysFont("arial", 48, bold=True)
fuente_input = pygame.font.SysFont("arial", 36)

# Ruta ABSOLUTA para la hoja
ruta_base = os.path.dirname(__file__)
ruta_hoja = os.path.join(ruta_base, "assets", "hoja.png")
hoja_img = pygame.image.load(ruta_hoja).convert_alpha()
hoja_img = pygame.transform.scale(hoja_img, (64, 64))


def dibujar_fondo_degradado():
    for i in range(ALTO):
        r = min(30 + int(i * 0.1), 255)
        g = min(60 + int(i * 0.2), 255)
        b = min(90 + int(i * 0.3), 255)
        color = (r, g, b)
        pygame.draw.line(pantalla, color, (0, i), (ANCHO, i))


def pedir_nickname():
    nickname = ""
    activo = True
    clock = pygame.time.Clock()

    while activo:
        dibujar_fondo_degradado()

        hoja_rect = hoja_img.get_rect(center=(ANCHO // 2, ALTO // 4 - 40))
        pantalla.blit(hoja_img, hoja_rect)

        titulo = fuente_titulo.render("Bienvenido Guardián", True, (255, 255, 255))
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 4 + 20))

        instruccion = fuente_input.render("Ingresa tu Nickname:", True, (200, 255, 200))
        pantalla.blit(
            instruccion, (ANCHO // 2 - instruccion.get_width() // 2, ALTO // 2 - 80)
        )

        input_box = pygame.Rect(ANCHO // 2 - 200, ALTO // 2 - 30, 400, 60)
        pygame.draw.rect(pantalla, (255, 255, 255, 50), input_box, border_radius=8)
        pygame.draw.rect(pantalla, (200, 255, 200), input_box, 3, border_radius=8)

        texto = fuente_input.render(nickname, True, (0, 255, 0))
        pantalla.blit(
            texto,
            (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2),
        )

        tip = pygame.font.SysFont("arial", 20).render(
            "Presiona ENTER para continuar", True, (220, 220, 220)
        )
        pantalla.blit(tip, (ANCHO // 2 - tip.get_width() // 2, ALTO // 2 + 50))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nickname.strip() != "":
                    activo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                else:
                    if len(nickname) < 15 and evento.unicode.isprintable():
                        nickname += evento.unicode

        clock.tick(30)

    return nickname


def main():
    jugador_nickname = pedir_nickname()
    print(f"Jugador registrado como: {jugador_nickname}")

    while True:
        inicializar_interfaz()

        seleccion = 0
        en_menu = True
        clock = pygame.time.Clock()
        tiempo_animacion = 0

        # Bucle del menú principal
        while en_menu:
            tiempo_animacion += 1
            dibujar_menu_completo(pantalla, seleccion, tiempo_animacion)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % 5  # 👈 5 opciones
                    elif evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % 5
                    elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                        en_menu = False
                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            clock.tick(60)

        # ───────────────────────────────
        # Ejecutar modo seleccionado
        # ───────────────────────────────
        if seleccion == 0:
            resultado = jugar_campaña(pantalla, jugador_nickname)

        elif seleccion == 1:
            resultado = jugar_libre(pantalla)

        elif seleccion == 2:
            resultado = jugar_educativo(pantalla)

        elif seleccion == 3:
            mostrar_ranking(pantalla)
            resultado = None

        elif seleccion == 4:
            ejecutar_demo_opengl()
            resultado = None

        # ───────────────────────────────
        # Después de volver de un modo
        # ───────────────────────────────
        if resultado == "reiniciar":
            continue
        else:
            # volver al menú sin pedir nickname
            pass


if __name__ == "__main__":
    main()
