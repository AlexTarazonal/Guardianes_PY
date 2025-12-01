import pygame
import sys
import os

ANCHO, ALTO = 1024, 768  # Usa tus dimensiones globales

# Inicializa pygame aquí si quieres usar fuentes ya
pygame.init()
fuente_titulo = pygame.font.SysFont("arial", 48, bold=True)
fuente_ranking = pygame.font.SysFont("arial", 28)

def mostrar_ranking(pantalla):
    pygame.display.set_caption("Ranking - Guardianes del Planeta")

    # ✅ Carga del trofeo AHORA que ya hay display
    ruta_base = os.path.dirname(__file__)
    ruta_trofeo = os.path.join(ruta_base, "assets", "trofeo.png")
    trofeo_img = pygame.image.load(ruta_trofeo).convert_alpha()
    trofeo_img = pygame.transform.scale(trofeo_img, (80, 80))  # Ajusta tamaño a gusto

    # 1️⃣ Leer puntajes
    puntajes = []
    if os.path.exists("puntajes.txt"):
        with open("puntajes.txt", "r") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 3:
                    nombre, puntaje, fecha = partes
                    try:
                        puntajes.append((nombre, int(puntaje), fecha))
                    except ValueError:
                        pass  # Ignorar líneas corruptas
    else:
        puntajes = []

    puntajes.sort(key=lambda x: x[1], reverse=True)

    clock = pygame.time.Clock()
    mostrando = True

    while mostrando:
        # Usa fondo estilo inicio
        for i in range(ALTO):
            intensidad = int(15 + (i / ALTO) * 40)
            color = (intensidad, max(25, intensidad + 15), min(255, intensidad + 45))
            pygame.draw.line(pantalla, color, (0, i), (ANCHO, i))

        # Dibuja el trofeo
        pantalla.blit(trofeo_img, (ANCHO // 2 - trofeo_img.get_width() // 2, 40))

        titulo = fuente_titulo.render("Ranking de Puntajes", True, (255, 255, 255))
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 140))

        # Mostrar TOP 10
        for idx, (nombre, puntaje, fecha) in enumerate(puntajes[:10]):
            texto = fuente_ranking.render(
                f"{idx + 1}. {nombre} - {puntaje} pts - {fecha}",
                True,
                (200, 255, 200)
            )
            pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 200 + idx * 40))

        instruccion = pygame.font.SysFont("arial", 20).render(
            "Presiona ESC para volver al menú", True, (220, 220, 220)
        )
        pantalla.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, ALTO - 60))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mostrando = False

        clock.tick(30)
