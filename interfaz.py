import pygame
import time

def inicializar_interfaz():
    # Aquí puedes inicializar pygame y crear la pantalla, por ejemplo
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Guardianes del Planeta")
    return pantalla

def get_fuentes():
    fuente = pygame.font.SysFont("arial", 28)
    fuente_chica = pygame.font.SysFont("arial", 22)
    fuente_grande = pygame.font.SysFont("arial", 42, bold=True)
    return fuente, fuente_chica, fuente_grande

def mostrar_titulo(pantalla):
    _, _, fuente_grande = get_fuentes()
    texto = fuente_grande.render("GUARDIANES DEL PLANETA", True, (32, 200, 120))
    pantalla.blit(texto, (80, 80))
def mostrar_pregunta(pantalla, pregunta):
    """
    pregunta: diccionario con 'texto', 'opciones', 'respuesta'
    Retorna True si respondió bien, False si mal.
    """
    fuente = pygame.font.SysFont("arial", 28)
    fuente_op = pygame.font.SysFont("arial", 24)
    seleccionado = -1
    esperando = True
    while esperando:
        pantalla.fill((80, 120, 160))
        texto = fuente.render(pregunta["texto"], True, (255, 255, 255))
        pantalla.blit(texto, (60, 120))
        for i, op in enumerate(pregunta["opciones"]):
            color = (255, 255, 0) if i == seleccionado else (230, 230, 230)
            txt = fuente_op.render(f"{i+1}. {op}", True, color)
            pantalla.blit(txt, (100, 200 + i * 40))
        info = fuente_op.render("Selecciona opción (1, 2, 3)...", True, (200,200,200))
        pantalla.blit(info, (90, 360))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    seleccionado = 0
                    esperando = False
                elif evento.key == pygame.K_2:
                    seleccionado = 1
                    esperando = False
                elif evento.key == pygame.K_3:
                    seleccionado = 2
                    esperando = False
        pygame.time.wait(80)
    time.sleep(0.5)  # Pequeña pausa antes de volver al juego
    return seleccionado == pregunta["respuesta"]
def mostrar_menu(pantalla, seleccion):
    _, fuente_chica, _ = get_fuentes()
    opciones = ["Modo Campaña", "Modo Libre Configurable", "Modo Educativo"]
    for i, opcion in enumerate(opciones):
        color = (255, 255, 0) if i == seleccion else (220, 220, 220)
        texto = fuente_chica.render(opcion, True, color)
        pantalla.blit(texto, (150, 210 + 50 * i))

def mostrar_opciones_libre(pantalla, nivel, vel_basura, vel_animal, vidas, opcion):
    _, fuente_chica, fuente_grande = get_fuentes()
    mapas = ["Océano", "Amazonas", "Ciudad"]
    opciones = [
        f"Mapa: {mapas[nivel]}",
        f"Velocidad Basura: {vel_basura}",
        f"Velocidad Animales: {vel_animal}",
        f"Vidas: {vidas}",
        "Iniciar"
    ]
    pantalla.fill((60, 100, 160))
    texto = fuente_grande.render("Configura el Modo Libre", True, (255,255,255))
    pantalla.blit(texto, (100, 60))
    for i, txt in enumerate(opciones):
        color = (0, 255, 100) if i == opcion else (220, 220, 220)
        t = fuente_chica.render(txt, True, color)
        pantalla.blit(t, (160, 180 + 45 * i))

def mostrar_creditos(pantalla):
    _, fuente_chica, _ = get_fuentes()
    txt = fuente_chica.render("By Tu Nombre - Computación Gráfica y Visual (2024)", True, (130, 170, 140))
    pantalla.blit(txt, (120, 570))

def mostrar_puntaje(pantalla, puntaje, y=10):
    fuente, _, _ = get_fuentes()
    txt = fuente.render(f"Puntaje: {puntaje}", True, (30, 70, 160))
    pantalla.blit(txt, (20, y))

def mostrar_vidas(pantalla, vidas):
    fuente, _, _ = get_fuentes()
    txt = fuente.render(f"Vidas: {vidas}", True, (180, 30, 30))
    pantalla.blit(txt, (650, 10))

def mostrar_frase(pantalla, mensaje, y=70):
    _, fuente_chica, _ = get_fuentes()
    if mensaje:
        txt = fuente_chica.render(mensaje, True, (0, 80, 0))
        pantalla.blit(txt, (60, y))

def mostrar_contadores(pantalla, recogidos, rescatados):
    _, fuente_chica, _ = get_fuentes()
    txt1 = fuente_chica.render(f"Basura recogida: {recogidos}", True, (0, 90, 150))
    txt2 = fuente_chica.render(f"Animales rescatados: {rescatados}", True, (80, 120, 40))
    pantalla.blit(txt1, (20, 50))
    pantalla.blit(txt2, (20, 75))

def mostrar_nivel(pantalla, nivel, nombre):
    _, _, fuente_grande = get_fuentes()
    txt = fuente_grande.render(f"{nombre}", True, (180, 120, 30))
    pantalla.blit(txt, (330, 12))

def pantalla_pausa(pantalla):
    _, fuente_chica, fuente_grande = get_fuentes()
    txt = fuente_grande.render("PAUSA", True, (255, 255, 0))
    info = fuente_chica.render("Presiona ESC para continuar", True, (255, 255, 220))
    pantalla.blit(txt, (320, 220))
    pantalla.blit(info, (260, 280))

def pantalla_game_over(pantalla, puntaje, recogidos, rescatados, frase):
    pantalla.fill((30, 30, 30))
    _, fuente_chica, fuente_grande = get_fuentes()
    txt1 = fuente_grande.render("FIN DEL JUEGO", True, (255, 80, 80))
    txt2 = fuente_chica.render(f"Puntaje final: {puntaje}", True, (200, 200, 200))
    txt3 = fuente_chica.render(f"Basura recogida: {recogidos}", True, (130, 180, 255))
    txt4 = fuente_chica.render(f"Animales rescatados: {rescatados}", True, (80, 255, 120))
    txt5 = fuente_chica.render(frase, True, (230, 230, 90))
    pantalla.blit(txt1, (250, 110))
    pantalla.blit(txt2, (300, 190))
    pantalla.blit(txt3, (300, 250))
    pantalla.blit(txt4, (300, 280))
    pantalla.blit(txt5, (90, 420))

def pantalla_victoria(pantalla, puntaje, recogidos, rescatados):
    pantalla.fill((20, 80, 40))
    _, fuente_chica, fuente_grande = get_fuentes()
    txt1 = fuente_grande.render("¡VICTORIA!", True, (90, 255, 120))
    txt2 = fuente_chica.render(f"Puntaje final: {puntaje}", True, (200, 255, 220))
    txt3 = fuente_chica.render(f"Basura recogida: {recogidos}", True, (80, 180, 255))
    txt4 = fuente_chica.render(f"Animales rescatados: {rescatados}", True, (180, 255, 80))
    txt5 = fuente_chica.render("¡Completaste la campaña ecológica!", True, (240, 255, 160))
    pantalla.blit(txt1, (250, 110))
    pantalla.blit(txt2, (300, 180))
    pantalla.blit(txt3, (300, 230))
    pantalla.blit(txt4, (300, 270))
    pantalla.blit(txt5, (160, 380))
