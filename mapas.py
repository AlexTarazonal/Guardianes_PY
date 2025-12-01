# ===== ARCHIVO: mapas.py - VERSIÓN MEJORADA =====
import pygame
import random
import math

def dibujar_amazonas(pantalla):
    pantalla.fill((0, 0, 0))
    ancho, alto = pantalla.get_size()

    # Proporciones clave
    cielo_alto = int(alto * 0.32)
    suelo_y = int(alto * 0.80)
    suelo_alto = int(alto * 0.20)

    # Gradiente de cielo amazónico (verde-azul degradado)
    for y in range(0, cielo_alto):
        color_r = int(45 + (y * 0.3))
        color_g = int(120 + (y * 0.4))
        color_b = int(60 + (y * 0.5))
        pygame.draw.line(pantalla, (color_r, color_g, color_b), (0, y), (ancho, y))

    # Suelo de la selva con textura
    pygame.draw.rect(pantalla, (45, 85, 30), (0, suelo_y, ancho, suelo_alto))
    for _ in range(int(ancho * 0.15)):
        x = random.randint(0, ancho)
        y = random.randint(suelo_y, alto)
        pygame.draw.circle(pantalla, (35, 75, 25), (x, y), random.randint(1, 3))

    # ───────── Río serpenteante (CORREGIDO, sin picos) ─────────
    base_y = int(alto * 0.64)          # altura base del río
    altura_rio = int(alto * 0.09)      # grosor del río

    puntos_superior = []
    puntos_inferior = []
    paso_x = max(12, int(ancho / 16))

    for x in range(-60, ancho + 80, paso_x):
        y_top = base_y + int(20 * math.sin(x * 0.01))
        y_bottom = y_top + altura_rio
        puntos_superior.append((x, y_top))
        puntos_inferior.append((x, y_bottom))

    # Primero todo el borde de arriba, luego el de abajo al revés
    puntos_rio = puntos_superior + list(reversed(puntos_inferior))
    pygame.draw.polygon(pantalla, (25, 140, 200), puntos_rio)

    # Reflejos en el agua
    for i in range(0, ancho, int(ancho / 28)):
        pygame.draw.line(
            pantalla, (40, 160, 220),
            (i, base_y + int(10 * math.sin(i * 0.02))),
            (i + int(ancho / 50), base_y + 10 + int(10 * math.sin(i * 0.02))),
            2
        )

    # Árboles escalados
    arboles_pos = [
        (int(ancho * 0.12), int(alto * 0.44)),
        (int(ancho * 0.30), int(alto * 0.39)),
        (int(ancho * 0.48), int(alto * 0.48)),
        (int(ancho * 0.65), int(alto * 0.41)),
        (int(ancho * 0.80), int(alto * 0.46)),
        (int(ancho * 0.90), int(alto * 0.38))
    ]
    for x, y_base in arboles_pos:
        altura_tronco = random.randint(int(alto * 0.08), int(alto * 0.13))
        grosor = random.randint(int(ancho * 0.014), int(ancho * 0.024))
        pygame.draw.rect(pantalla, (70, 40, 15), (x, y_base, grosor, altura_tronco))
        for i in range(0, altura_tronco, 10):
            pygame.draw.line(pantalla, (55, 30, 10), (x, y_base + i), (x + grosor, y_base + i), 1)
        copa_y = y_base - 20
        pygame.draw.ellipse(pantalla, (40, 140, 50), (x - 35, copa_y, 80, 45))
        pygame.draw.ellipse(pantalla, (50, 160, 60), (x - 25, copa_y - 15, 60, 35))
        pygame.draw.ellipse(pantalla, (60, 180, 70), (x - 15, copa_y - 25, 40, 25))
        if random.random() < 0.6:
            for _ in range(random.randint(2, 5)):
                fruta_x = x + random.randint(-20, 30)
                fruta_y = copa_y + random.randint(-10, 20)
                color_fruta = random.choice([(200, 50, 50), (220, 180, 50), (180, 100, 200)])
                pygame.draw.circle(pantalla, color_fruta, (fruta_x, fruta_y), 3)

    # Plantas del sotobosque
    for _ in range(int(ancho * 0.03)):
        x = random.randint(0, ancho)
        y = random.randint(int(alto * 0.63), int(alto * 0.68))
        pygame.draw.ellipse(pantalla, (35, 120, 40), (x, y, 30, 8))
        pygame.draw.ellipse(pantalla, (45, 140, 50), (x + 5, y - 5, 20, 6))

    # Lianas más realistas
    for _ in range(12):
        start_x = random.randint(50, ancho - 50)
        start_y = random.randint(50, int(alto * 0.18))
        for i in range(0, int(alto * 0.39), 15):
            curve_x = start_x + int(15 * math.sin(i * 0.02))
            curve_y = start_y + i
            if curve_y < suelo_y:
                pygame.draw.circle(pantalla, (25, 80, 20), (curve_x, curve_y), 2)
                if i % 30 == 0:
                    pygame.draw.ellipse(pantalla, (40, 100, 30), (curve_x - 3, curve_y, 8, 4))

    # Mariposas y efectos de vida
    for _ in range(8):
        x = random.randint(0, ancho)
        y = random.randint(100, int(alto * 0.52))
        color = random.choice([(255, 200, 50), (200, 100, 255), (100, 255, 150)])
        pygame.draw.circle(pantalla, color, (x, y), 2)
        pygame.draw.circle(pantalla, color, (x + 3, y), 2)

    # Rayos de sol filtrándose
    for _ in range(6):
        x = random.randint(0, ancho)
        for i in range(0, int(cielo_alto * 0.6), 10):
            light_color = (150 + i // 4, 180 + i // 4, 100 + i // 4)
            pygame.draw.line(pantalla, light_color, (x, i), (x + 2, i + 8), 1)



def dibujar_oceano(pantalla):
    pantalla.fill((0, 0, 0))
    ancho, alto = pantalla.get_size()
    import time

    # Gradiente del cielo marino
    cielo_alto = int(alto * 0.33)
    for y in range(0, cielo_alto):
        color_r = int(30 + (y * 0.4))
        color_g = int(80 + (y * 0.6))
        color_b = int(180 + (y * 0.3))
        color = (color_r, color_g, color_b)
        pygame.draw.line(pantalla, color, (0, y), (ancho, y))

    # Horizonte
    pygame.draw.line(pantalla, (255, 255, 200), (0, cielo_alto), (ancho, cielo_alto), 2)

    # Mar con diferentes tonos de profundidad
    num_franjas = 6
    altura_franja = (alto - cielo_alto) // num_franjas
    for depth in range(num_franjas):
        y_start = cielo_alto + depth * altura_franja
        color_intensity = 170 - depth * 20
        pygame.draw.rect(pantalla, (10, color_intensity // 3, color_intensity),
                         (0, y_start, ancho, altura_franja))

    # Olas dinámicas en múltiples capas
    wave_offset = int(time.time() * 50) % ancho  # Simular movimiento
    for layer in range(4):
        y_wave = cielo_alto + layer * (altura_franja // 2)
        wave_color = (80 + layer * 20, 180 + layer * 10, 255 - layer * 15)
        for x in range(-100, ancho + 100, 40):
            wave_x = (x + wave_offset) % ancho
            wave_height = int(15 * math.sin((wave_x + layer * 50) * 0.02))
            pygame.draw.arc(pantalla, wave_color,
                            (wave_x - 20, y_wave + wave_height - 10, 80, 20),
                            0, math.pi, 3)

    # Espuma de las olas
    for _ in range(30):
        x = random.randint(0, ancho)
        y = random.randint(cielo_alto, alto - 50)
        foam_size = random.randint(2, 6)
        pygame.draw.circle(pantalla, (200, 220, 255), (x, y), foam_size)

    # Islas Ballestas inspiradas
    isla_y = cielo_alto + int(altura_franja * 1.8)
    pygame.draw.ellipse(pantalla, (160, 140, 80), (ancho // 8, isla_y, ancho // 8, altura_franja // 2))
    pygame.draw.ellipse(pantalla, (140, 120, 60), (ancho // 8 + 10, isla_y - 10, ancho // 10, altura_franja // 4))
    # Vegetación en la isla
    for _ in range(8):
        x = random.randint(ancho // 8 + 10, ancho // 8 + ancho // 8 - 10)
        y = random.randint(isla_y - 10, isla_y + altura_franja // 3)
        pygame.draw.circle(pantalla, (80, 140, 60), (x, y), random.randint(3, 8))

    # Isla más pequeña
    pygame.draw.ellipse(pantalla, (140, 120, 70), (ancho // 2, isla_y + altura_franja // 3, ancho // 10, altura_franja // 5))

    # Rocas emergentes
    rocas_pos = [
        (ancho // 12, isla_y + altura_franja // 2),
        (ancho // 2, isla_y + altura_franja // 2),
        (int(ancho * 0.75), isla_y + altura_franja // 2),
        (int(ancho * 0.88), isla_y + altura_franja // 2),
    ]
    for x, y in rocas_pos:
        pygame.draw.ellipse(pantalla, (90, 80, 60), (x, y, 30, 15))
        pygame.draw.arc(pantalla, (150, 200, 255), (x - 10, y - 5, 50, 25), 0, math.pi, 2)

    # Algas marinas ondulantes
    for _ in range(20):
        x = random.randint(0, ancho)
        base_y = alto - random.randint(60, 100)
        for i in range(0, 60, 5):
            sway = int(8 * math.sin((x + i) * 0.05))
            pygame.draw.circle(pantalla, (30, 120, 60), (x + sway, base_y - i), 2)
        for i in range(0, 60, 15):
            sway = int(8 * math.sin((x + i) * 0.05))
            pygame.draw.ellipse(pantalla, (40, 140, 70), (x + sway - 5, base_y - i, 12, 4))

    # Peces ocasionales (siluetas)
    for _ in range(6):
        x = random.randint(0, ancho)
        y = random.randint(cielo_alto + altura_franja, alto - 120)
        pygame.draw.ellipse(pantalla, (100, 150, 200), (x, y, 20, 8))
        pygame.draw.polygon(pantalla, (80, 130, 180), [(x, y + 4), (x - 8, y), (x - 8, y + 8)])

    # Gaviotas en el cielo
    for _ in range(4):
        x = random.randint(0, ancho)
        y = random.randint(50, cielo_alto - 10)
        pygame.draw.arc(pantalla, (255, 255, 255), (x, y, 20, 8), 0, math.pi, 2)
        pygame.draw.arc(pantalla, (255, 255, 255), (x + 10, y, 20, 8), 0, math.pi, 2)

def dibujar_lima(pantalla):
    import random
    ancho, alto = pantalla.get_size()
    cielo_alto = int(alto * 0.55)  # El cielo ocupa el 55% del alto

    # Gradiente del cielo limeño con smog
    for y in range(cielo_alto):
        gris_base = 160
        if y < int(cielo_alto * 0.33):
            color_val = gris_base + int(y * 0.3)
        else:
            color_val = gris_base + int((y - int(cielo_alto * 0.33)) * 0.1)
        pygame.draw.line(pantalla, (color_val, color_val - 10, color_val - 20), (0, y), (ancho, y))

    # Suelo de la ciudad (gris oscuro)
    suelo_y = int(alto * 0.85)
    pygame.draw.rect(pantalla, (60, 60, 60), (0, suelo_y, ancho, alto - suelo_y))

    # Calles principales (verticales)
    main_streets = [int(ancho * f) for f in [0.2, 0.4, 0.6, 0.8]]
    for x in main_streets:
        pygame.draw.rect(pantalla, (80, 80, 80), (x - 15, cielo_alto, 30, suelo_y - cielo_alto))
        pygame.draw.line(pantalla, (150, 150, 100), (x, cielo_alto), (x, suelo_y), 2)

    # Avenidas horizontales (una a mitad y otra cerca del suelo)
    ave_y1 = int(cielo_alto + (suelo_y - cielo_alto) * 0.5)
    ave_y2 = int(suelo_y - 40)
    for y in [ave_y1, ave_y2]:
        pygame.draw.rect(pantalla, (85, 85, 85), (0, y - 12, ancho, 24))
        pygame.draw.line(pantalla, (150, 150, 100), (0, y), (ancho, y), 2)

    # Edificios altos, llenando el skyline
    edificios_data = []
    x = 20
    while x < ancho - 60:
        tipo = random.choice(["moderno", "colonial", "residencial", "oficina"])
        width = random.randint(45, 80)
        height = random.randint(int(cielo_alto * 0.3), int(cielo_alto * 0.7))
        edificios_data.append({"x": x, "width": width, "height": height, "tipo": tipo})
        x += width + random.randint(10, 20)

    for edificio in edificios_data:
        ex, width, height = edificio["x"], edificio["width"], edificio["height"]
        ey = cielo_alto - height
        tipo = edificio["tipo"]

        if tipo == "colonial":
            color_base = (180, 160, 120)
            pygame.draw.rect(pantalla, color_base, (ex, ey, width, height))
            # Balcones
            for piso in range(1, height // 40):
                balcon_y = ey + piso * 40
                pygame.draw.rect(pantalla, (160, 140, 100), (ex + 10, balcon_y, width - 20, 8))
        elif tipo == "moderno":
            color_base = (120, 140, 160)
            pygame.draw.rect(pantalla, color_base, (ex, ey, width, height))
            for piso in range(0, height, 25):
                for ventana in range(0, width, 20):
                    if ventana + 15 < width and piso + 20 < height:
                        pygame.draw.rect(pantalla, (150, 180, 220), (ex + ventana + 5, ey + piso + 5, 15, 20))
        elif tipo == "residencial":
            color_base = (160, 150, 130)
            pygame.draw.rect(pantalla, color_base, (ex, ey, width, height))
            pygame.draw.polygon(pantalla, (120, 80, 60), [(ex, ey), (ex + width // 2, ey - 15), (ex + width, ey)])
            pygame.draw.rect(pantalla, (80, 60, 40), (ex + width // 2 - 8, ey + height - 30, 16, 30))
        else:  # oficina o comercial
            color_base = (100, 120, 140)
            pygame.draw.rect(pantalla, color_base, (ex, ey, width, height))
            for piso in range(0, height, 30):
                for col in range(0, width, 25):
                    if col + 20 < width and piso + 25 < height:
                        pygame.draw.rect(pantalla, (180, 200, 220), (ex + col + 5, ey + piso + 5, 20, 25))

    # Elementos urbanos en el suelo
    for i in range(0, ancho, ancho // 10):
        # Árboles urbanos
        if random.random() < 0.7:
            pygame.draw.rect(pantalla, (60, 40, 20), (i + 6, suelo_y - 15, 8, 15))
            pygame.draw.circle(pantalla, (80, 120, 60), (i + 10, suelo_y - 16), 10)
        # Papeleras y bancas
        if random.random() < 0.4:
            pygame.draw.rect(pantalla, (100, 100, 100), (i + 30, suelo_y - 10, 8, 10))
            pygame.draw.rect(pantalla, (200, 200, 240), (i + 30, suelo_y - 12, 8, 4))

    # Faroles en el borde del suelo
    for i in range(5):
        x = int((i + 1) * ancho / 6)
        pygame.draw.rect(pantalla, (80, 80, 90), (x, suelo_y - 30, 5, 30))
        pygame.draw.circle(pantalla, (255, 255, 180), (x + 2, suelo_y - 30), 7)

    # Cables de luz, solo arriba
    for _ in range(6):
        start_x = random.randint(0, ancho)
        end_x = start_x + random.randint(80, 180)
        if end_x > ancho: end_x = ancho
        y_cable = random.randint(int(cielo_alto * 0.25), int(cielo_alto * 0.5))
        pygame.draw.line(pantalla, (20, 20, 20), (start_x, y_cable), (end_x, y_cable + random.randint(-8, 12)), 2)

    # Detalles extra: autos simples (rectángulos de colores)
    for _ in range(6):
        x = random.randint(0, ancho)
        y = random.choice([ave_y1 + 10, ave_y2 + 8])
        color_auto = random.choice([(255,0,0),(80,200,80),(30,180,250),(200,180,40),(120,120,120)])
        pygame.draw.rect(pantalla, color_auto, (x, y, 32, 12))
        pygame.draw.rect(pantalla, (30, 30, 30), (x+2, y+9, 28, 4))


def dibujar_fondo(pantalla, nivel):
    pantalla.fill((0, 0, 0))
    ancho, alto = pantalla.get_size()
    """Función principal que selecciona qué mapa dibujar"""
    if nivel == 1:
        dibujar_amazonas(pantalla)
    elif nivel == 0:
        dibujar_oceano(pantalla)
    elif nivel == 2:
        dibujar_lima(pantalla)
    else:
        # Mapa por defecto si hay error
        pantalla.fill((50, 50, 50))
        
# Función adicional para efectos especiales por mapa
def efectos_ambientales(pantalla, nivel):
    ancho, alto = pantalla.get_size()
    """Añade efectos ambientales específicos de cada región"""
    if nivel == 0:  # Amazonas
        # Partículas de polen/insectos
        for _ in range(5):
            x = random.randint(0, ancho)
            y = random.randint(0, 400)
            pygame.draw.circle(pantalla, (255, 255, 200), (x, y), 1)
    
    elif nivel == 1:  # Océano
        # Gotas de agua ocasionales
        for _ in range(3):
            x = random.randint(0, ancho)
            y = random.randint(250, 400)
            pygame.draw.circle(pantalla, (200, 230, 255), (x, y), 2)
    
    elif nivel == 2:  # Lima
        # Partículas de smog
        for _ in range(8):
            x = random.randint(0, ancho)
            y = random.randint(0, 200)
            pygame.draw.circle(pantalla, (180, 180, 170), (x, y), 1)