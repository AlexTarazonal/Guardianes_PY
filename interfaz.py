import pygame
import math
import time

# Configuración de colores modernos con temática ecológica
COLORES = {
    "fondo_principal": (15, 25, 35),  # Azul marino profundo
    "fondo_menu": (20, 40, 60),  # Azul oceánico
    "verde_principal": (34, 197, 94),  # Verde ecosistema
    "verde_claro": (74, 222, 128),  # Verde claro brillante
    "azul_agua": (14, 165, 233),  # Azul agua limpia
    "amarillo_sol": (251, 191, 36),  # Amarillo dorado
    "rojo_alerta": (239, 68, 68),  # Rojo advertencia
    "blanco": (255, 255, 255),
    "gris_claro": (209, 213, 219),
    "gris_oscuro": (75, 85, 99),
    "transparente": (0, 0, 0, 128),
    "naranja_energia": (251, 146, 60),  # Naranja energético
    "morado_misterio": (168, 85, 247),  # Morado místico
}


def obtener_dimensiones_pantalla():
    """Retorna las dimensiones estándar de la pantalla."""
    return 1024, 768


def inicializar_interfaz():
    """Inicializa pygame y configura la interfaz."""
    pygame.init()
    pygame.font.init()
    return True


# ─────────────────────────────────────────────────────────────
# Fuentes (cacheadas para no crearlas a cada llamada)
# ─────────────────────────────────────────────────────────────
_fuentes_cache = None


def get_fuentes():
    """Obtiene fuentes modernas con diferentes tamaños (cacheadas)."""
    global _fuentes_cache
    if _fuentes_cache is not None:
        return _fuentes_cache

    # Intentamos una fuente moderna; si no, pygame usará la por defecto
    nombre_fuente = pygame.font.match_font("montserrat,arial,sans-serif")

    try:
        fuente_principal = pygame.font.Font(nombre_fuente, 30)
        fuente_pequena = pygame.font.Font(nombre_fuente, 22)
        fuente_grande = pygame.font.Font(nombre_fuente, 44)
        fuente_titulo = pygame.font.Font(nombre_fuente, 58)
        fuente_subtitulo = pygame.font.Font(nombre_fuente, 32)
    except Exception:
        # Fallback a fuentes del sistema
        fuente_principal = pygame.font.SysFont("arial", 30, bold=True)
        fuente_pequena = pygame.font.SysFont("arial", 22)
        fuente_grande = pygame.font.SysFont("arial", 44, bold=True)
        fuente_titulo = pygame.font.SysFont("arial", 58, bold=True)
        fuente_subtitulo = pygame.font.SysFont("arial", 32, bold=True)

    _fuentes_cache = (
        fuente_principal,
        fuente_pequena,
        fuente_grande,
        fuente_titulo,
        fuente_subtitulo,
    )
    return _fuentes_cache


# ─────────────────────────────────────────────────────────────
# FONDO / DECORACIÓN
# ─────────────────────────────────────────────────────────────
def dibujar_fondo_animado(pantalla, tiempo):
    """Dibuja un fondo animado con elementos naturales del Perú."""
    ancho, alto = pantalla.get_size()

    # Gradiente de fondo (cielo/océano)
    for y in range(alto):
        intensidad = int(15 + (y / alto) * 40)
        color = (intensidad, max(25, intensidad + 15), min(255, intensidad + 45))
        pygame.draw.line(pantalla, color, (0, y), (ancho, y))

    # Ondas del océano (animadas)
    for i in range(3):
        y_onda = alto - 150 + i * 20
        puntos = []
        for x in range(0, ancho + 20, 20):
            y = y_onda + math.sin((x + tiempo * 2) * 0.01 + i) * 8
            puntos.append((x, y))

        if len(puntos) > 2:
            color_onda = (14 + i * 10, 165 - i * 20, 233 - i * 30)
            for j in range(len(puntos) - 1):
                pygame.draw.line(pantalla, color_onda, puntos[j], puntos[j + 1], 3)

    # Montañas de los Andes (silueta)
    puntos_montana = [
        (0, alto - 100),
        (150, alto - 200),
        (300, alto - 180),
        (450, alto - 250),
        (600, alto - 220),
        (750, alto - 280),
        (900, alto - 240),
        (ancho, alto - 200),
        (ancho, alto),
        (0, alto),
    ]
    pygame.draw.polygon(pantalla, (45, 55, 75), puntos_montana)

    # Estrellas brillantes (parpadean)
    for i in range(15):
        x = (i * 67 + 50) % ancho
        y = (i * 43 + 30) % (alto // 3)
        brillo = abs(math.sin(tiempo * 0.05 + i)) * 255
        color_estrella = (int(brillo), int(brillo), 255)
        tamano = 2 + int(brillo / 128)
        pygame.draw.circle(pantalla, color_estrella, (x, y), tamano)


def dibujar_elementos_decorativos(pantalla, tiempo):
    """Dibuja elementos decorativos animados (hojas)."""
    ancho, alto = pantalla.get_size()

    # Hojas flotantes
    for i in range(8):
        x = (i * 120 + tiempo * 0.5) % (ancho + 100) - 50
        y = 200 + math.sin(tiempo * 0.02 + i) * 30 + i * 40
        rotacion = tiempo * 0.03 + i

        tamano = 8 + i % 3
        dx = math.cos(rotacion) * tamano
        dy = math.sin(rotacion) * tamano

        puntos = [(x, y), (x + dx, y + dy), (x - dx / 2, y + dy / 2)]
        pygame.draw.polygon(pantalla, COLORES["verde_principal"], puntos)


# ─────────────────────────────────────────────────────────────
# TÍTULO Y MENÚ PRINCIPAL
# ─────────────────────────────────────────────────────────────
def dibujar_titulo_principal(pantalla, tiempo):
    """Dibuja el título principal con efectos visuales."""
    ancho, _ = pantalla.get_size()
    _, _, _, fuente_titulo, fuente_subtitulo = get_fuentes()

    # Efecto de brillo en el título
    offset_brillo = int(math.sin(tiempo * 0.08) * 3)

    # Sombra del título
    titulo_sombra = fuente_titulo.render("🌍 GUARDIANES DEL PLANETA", True, (0, 0, 0))
    rect_sombra = titulo_sombra.get_rect(center=(ancho // 2 + 3, 120 + 3))
    pantalla.blit(titulo_sombra, rect_sombra)

    # Título principal con brillo
    titulo = fuente_titulo.render(
        "🌍 GUARDIANES DEL PLANETA", True, COLORES["verde_claro"]
    )
    rect_titulo = titulo.get_rect(center=(ancho // 2 + offset_brillo, 120))
    pantalla.blit(titulo, rect_titulo)

    # Subtítulo
    subtitulo = fuente_subtitulo.render(
        "Aventura Ecológica Peruana", True, COLORES["amarillo_sol"]
    )
    rect_subtitulo = subtitulo.get_rect(center=(ancho // 2, 170))
    pantalla.blit(subtitulo, rect_subtitulo)


def dibujar_menu_opciones(pantalla, seleccion, tiempo):
    """Dibuja las opciones del menú con animaciones."""
    ancho, alto = pantalla.get_size()
    fuente_principal, fuente_pequena, _, _, _ = get_fuentes()

    opciones = [
        {"texto": "🎯 Modo Campaña", "desc": "Aventura progresiva por el Perú"},
        {"texto": "🎮 Modo Libre", "desc": "Juego personalizable infinito"},
        {"texto": "🎓 Modo Educativo", "desc": "Aprende mientras juegas"},
        {"texto": "🏆 Ranking", "desc": "Ver los mejores puntajes"},
        {"texto": "🌀 Demo 3D OpenGL", "desc": "Explora un cubo ecológico en 3D"},
    ]

    # Ajuste para que no se pegue a las instrucciones
    y_inicio = 260
    espacio_vertical = 80

    for i, opcion in enumerate(opciones):
        y_pos = y_inicio + i * espacio_vertical

        # Efecto de selección
        if i == seleccion:
            ancho_rect = 500 + int(math.sin(tiempo * 0.1) * 20)
            rect_seleccion = pygame.Rect(
                ancho // 2 - ancho_rect // 2, y_pos - 25, ancho_rect, 70
            )
            pygame.draw.rect(
                pantalla, COLORES["verde_principal"], rect_seleccion, border_radius=15
            )
            pygame.draw.rect(
                pantalla, COLORES["verde_claro"], rect_seleccion, 3, border_radius=15
            )

            color_texto = COLORES["blanco"]
            color_desc = COLORES["gris_claro"]
        else:
            color_texto = COLORES["gris_claro"]
            color_desc = COLORES["gris_oscuro"]

        # Texto principal de la opción
        texto = fuente_principal.render(opcion["texto"], True, color_texto)
        rect_texto = texto.get_rect(center=(ancho // 2, y_pos))
        pantalla.blit(texto, rect_texto)

        # Descripción
        desc = fuente_pequena.render(opcion["desc"], True, color_desc)
        rect_desc = desc.get_rect(center=(ancho // 2, y_pos + 25))
        pantalla.blit(desc, rect_desc)


def dibujar_instrucciones(pantalla):
    """Dibuja las instrucciones de navegación."""
    ancho, alto = pantalla.get_size()
    _, fuente_pequena, _, _, _ = get_fuentes()

    instrucciones = ["↑↓ Navegar   ENTER/ESPACIO Seleccionar   ESC Salir"]

    for i, instruccion in enumerate(instrucciones):
        texto = fuente_pequena.render(instruccion, True, COLORES["amarillo_sol"])
        rect = texto.get_rect(center=(ancho // 2, alto - 60 + i * 25))
        pantalla.blit(texto, rect)


def dibujar_menu_completo(pantalla, seleccion, tiempo):
    """Dibuja el menú completo con todos sus elementos."""
    dibujar_fondo_animado(pantalla, tiempo)
    dibujar_elementos_decorativos(pantalla, tiempo)
    dibujar_titulo_principal(pantalla, tiempo)
    dibujar_menu_opciones(pantalla, seleccion, tiempo)
    dibujar_instrucciones(pantalla)


# ─────────────────────────────────────────────────────────────
# HUD Y TEXTOS DURANTE EL JUEGO
# ─────────────────────────────────────────────────────────────
def mostrar_nivel(pantalla, nivel, nombre_nivel, posicion=(300, 15)):
    """Muestra el nombre del nivel actual."""
    _, fuente_pequena, _, _, _ = get_fuentes()
    texto = fuente_pequena.render(
        f"🌎 Nivel {nivel + 1}: {nombre_nivel}", True, COLORES["morado_misterio"]
    )
    pantalla.blit(texto, posicion)


def mostrar_contadores(pantalla, recogidos, rescatados, posicion=(20, 50)):
    """Muestra los contadores de basura y animales."""
    _, fuente_pequena, _, _, _ = get_fuentes()
    x, y = posicion

    texto_basura = fuente_pequena.render(
        f"🗑️ Basura: {recogidos}", True, COLORES["azul_agua"]
    )
    pantalla.blit(texto_basura, (x, y))

    texto_animales = fuente_pequena.render(
        f"🐾 Animales: {rescatados}", True, COLORES["naranja_energia"]
    )
    pantalla.blit(texto_animales, (x, y + 25))


def mostrar_vidas(pantalla, vidas, posicion=(650, 15)):
    """Muestra las vidas del jugador en pantalla."""
    fuente_principal, _, _, _, _ = get_fuentes()
    texto = fuente_principal.render(f"❤️ {vidas}", True, COLORES["rojo_alerta"])
    pantalla.blit(texto, posicion)


def mostrar_frase(pantalla, mensaje, posicion=(20, 100)):
    """Muestra un mensaje temporal en pantalla (HUD)."""
    _, fuente_pequena, _, _, _ = get_fuentes()
    texto = fuente_pequena.render(mensaje, True, COLORES["verde_principal"])
    pantalla.blit(texto, posicion)


def mostrar_puntaje(pantalla, puntaje, posicion=(20, 15)):
    """Muestra el puntaje en pantalla."""
    fuente_principal, _, _, _, _ = get_fuentes()
    texto = fuente_principal.render(f"💎 {puntaje}", True, COLORES["amarillo_sol"])
    pantalla.blit(texto, posicion)


def mostrar_hud_juego(
    pantalla,
    puntaje,
    vidas,
    basura_recogida,
    animales_rescatados,
    nivel,
    nombre_nivel,
    mensaje=None,
):
    """Muestra el HUD durante el juego con diseño moderno."""
    ancho, _ = pantalla.get_size()
    fuente_principal, fuente_pequena, _, _, _ = get_fuentes()

    # Panel superior translúcido
    panel_superior = pygame.Surface((ancho, 100), pygame.SRCALPHA)
    panel_superior.fill((0, 0, 0, 120))
    pantalla.blit(panel_superior, (0, 0))

    # Puntaje
    texto_puntaje = fuente_principal.render(
        f"💎 {puntaje}", True, COLORES["amarillo_sol"]
    )
    pantalla.blit(texto_puntaje, (20, 15))

    # Vidas
    texto_vidas = fuente_principal.render(f"❤️ {vidas}", True, COLORES["rojo_alerta"])
    pantalla.blit(texto_vidas, (ancho - 150, 15))

    # Nivel
    texto_nivel = fuente_principal.render(nombre_nivel, True, COLORES["verde_claro"])
    rect_nivel = texto_nivel.get_rect(center=(ancho // 2, 25))
    pantalla.blit(texto_nivel, rect_nivel)

    # Contadores
    texto_basura = fuente_pequena.render(
        f"🗑️ {basura_recogida}", True, COLORES["azul_agua"]
    )
    texto_animales = fuente_pequena.render(
        f"🐾 {animales_rescatados}", True, COLORES["naranja_energia"]
    )
    pantalla.blit(texto_basura, (20, 50))
    pantalla.blit(texto_animales, (20, 70))

    # Mensaje temporal
    if mensaje:
        texto_mensaje = fuente_pequena.render(mensaje, True, COLORES["verde_claro"])
        rect_mensaje = texto_mensaje.get_rect(center=(ancho // 2, 60))
        pantalla.blit(texto_mensaje, rect_mensaje)


# ─────────────────────────────────────────────────────────────
# PANTALLAS ESPECIALES (PAUSA, GAME OVER, VICTORIA)
# ─────────────────────────────────────────────────────────────
def pantalla_pausa(pantalla):
    """Pantalla de pausa con diseño moderno."""
    ancho, alto = pantalla.get_size()
    _, fuente_pequena, fuente_grande, _, _ = get_fuentes()

    # Overlay semi-transparente
    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    pantalla.blit(overlay, (0, 0))

    # Panel central
    panel_rect = pygame.Rect(ancho // 4, alto // 4, ancho // 2, alto // 2)
    pygame.draw.rect(pantalla, COLORES["fondo_menu"], panel_rect, border_radius=20)
    pygame.draw.rect(
        pantalla, COLORES["verde_principal"], panel_rect, 4, border_radius=20
    )

    # Texto de pausa
    texto_pausa = fuente_grande.render("⏸️ PAUSA", True, COLORES["amarillo_sol"])
    rect_pausa = texto_pausa.get_rect(center=(ancho // 2, alto // 2 - 40))
    pantalla.blit(texto_pausa, rect_pausa)

    # Instrucciones
    instruccion = fuente_pequena.render(
        "Presiona ESC para continuar", True, COLORES["gris_claro"]
    )
    rect_instr = instruccion.get_rect(center=(ancho // 2, alto // 2 + 20))
    pantalla.blit(instruccion, rect_instr)


def pantalla_game_over(pantalla, puntaje, recogidos, rescatados, frase):
    """Pantalla de game over con estadísticas."""
    ancho, alto = pantalla.get_size()
    fuente_principal, fuente_pequena, fuente_grande, _, _ = get_fuentes()

    # Fondo oscuro
    pantalla.fill((20, 20, 30))

    # Panel central
    panel_rect = pygame.Rect(80, 60, ancho - 160, alto - 120)
    pygame.draw.rect(pantalla, (40, 40, 50), panel_rect, border_radius=20)
    pygame.draw.rect(pantalla, COLORES["rojo_alerta"], panel_rect, 4, border_radius=20)

    # Título
    titulo = fuente_grande.render("💔 MISIÓN TERMINADA", True, COLORES["rojo_alerta"])
    rect_titulo = titulo.get_rect(center=(ancho // 2, 140))
    pantalla.blit(titulo, rect_titulo)

    # Estadísticas
    estadisticas = [
        f"Puntaje Final: {puntaje}",
        f"🗑️ Basura Recogida: {recogidos}",
        f"🐾 Animales Rescatados: {rescatados}",
    ]

    y_stats = 220
    for stat in estadisticas:
        texto = fuente_principal.render(stat, True, COLORES["gris_claro"])
        rect = texto.get_rect(center=(ancho // 2, y_stats))
        pantalla.blit(texto, rect)
        y_stats += 40

    # Frase educativa
    if frase:
        palabras = frase.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            if len(linea_actual + palabra) < 60:
                linea_actual += palabra + " "
            else:
                lineas.append(linea_actual.strip())
                linea_actual = palabra + " "
        if linea_actual:
            lineas.append(linea_actual.strip())

        y_frase = 400
        for linea in lineas:
            texto = fuente_pequena.render(linea, True, COLORES["amarillo_sol"])
            rect = texto.get_rect(center=(ancho // 2, y_frase))
            pantalla.blit(texto, rect)
            y_frase += 25

    # Instrucciones
    instruccion = fuente_pequena.render(
        "Presiona R para reiniciar o ESC para salir", True, COLORES["verde_claro"]
    )
    rect_instr = instruccion.get_rect(center=(ancho // 2, alto - 80))
    pantalla.blit(instruccion, rect_instr)


def pantalla_victoria(pantalla, puntaje, recogidos, rescatados):
    """Pantalla de victoria épica."""
    ancho, alto = pantalla.get_size()
    fuente_principal, fuente_pequena, fuente_grande, _, _ = get_fuentes()

    # Fondo celebratorio
    for y in range(alto):
        intensidad = int(20 + (y / alto) * 60)
        color = (intensidad, intensidad + 40, intensidad + 20)
        pygame.draw.line(pantalla, color, (0, y), (ancho, y))

    # Panel central brillante
    panel_rect = pygame.Rect(80, 60, ancho - 160, alto - 120)
    pygame.draw.rect(pantalla, (255, 255, 255), panel_rect, border_radius=20)
    pygame.draw.rect(
        pantalla, COLORES["verde_principal"], panel_rect, 6, border_radius=20
    )

    # Título épico
    titulo = fuente_grande.render(
        "🏆 ¡MISIÓN CUMPLIDA!", True, COLORES["verde_principal"]
    )
    rect_titulo = titulo.get_rect(center=(ancho // 2, 130))
    pantalla.blit(titulo, rect_titulo)

    subtitulo = fuente_principal.render(
        "¡Salvaste el ecosistema peruano!", True, COLORES["verde_claro"]
    )
    rect_sub = subtitulo.get_rect(center=(ancho // 2, 170))
    pantalla.blit(subtitulo, rect_sub)

    # Estadísticas finales
    estadisticas = [
        f"🎯 Puntaje Final: {puntaje}",
        f"♻️ Basura Reciclada: {recogidos}",
        f"🦋 Animales Salvados: {rescatados}",
        f"🌱 Impacto: ¡EXTRAORDINARIO!",
    ]

    y_stats = 240
    for stat in estadisticas:
        texto = fuente_principal.render(stat, True, COLORES["gris_oscuro"])
        rect = texto.get_rect(center=(ancho // 2, y_stats))
        pantalla.blit(texto, rect)
        y_stats += 45

    # Mensaje inspirador
    mensaje = "Gracias por proteger la biodiversidad del Perú 🇵🇪"
    texto_mensaje = fuente_principal.render(mensaje, True, COLORES["amarillo_sol"])
    rect_mensaje = texto_mensaje.get_rect(center=(ancho // 2, 480))
    pantalla.blit(texto_mensaje, rect_mensaje)

    # Instrucciones
    instruccion = fuente_pequena.render(
        "Presiona cualquier tecla para continuar", True, COLORES["verde_principal"]
    )
    rect_instr = instruccion.get_rect(center=(ancho // 2, alto - 80))
    pantalla.blit(instruccion, rect_instr)


# ─────────────────────────────────────────────────────────────
# PREGUNTAS EDUCATIVAS
# ─────────────────────────────────────────────────────────────
def mostrar_pregunta(pantalla, pregunta):
    """Muestra una pregunta educativa con diseño moderno."""
    ancho, alto = pantalla.get_size()
    fuente_principal, fuente_pequena, _, _, fuente_subtitulo = get_fuentes()

    seleccionado = -1
    esperando = True
    tiempo_anim = 0

    while esperando:
        tiempo_anim += 1

        # Fondo con gradiente
        for y in range(alto):
            intensidad = int(40 + (y / alto) * 30)
            color = (intensidad, intensidad + 20, intensidad + 40)
            pygame.draw.line(pantalla, color, (0, y), (ancho, y))

        # Panel central (con ligera transparencia)
        panel_surface = pygame.Surface((ancho - 120, alto - 160), pygame.SRCALPHA)
        panel_surface.fill((255, 255, 255, 220))
        pantalla.blit(panel_surface, (60, 80))
        panel_rect = pygame.Rect(60, 80, ancho - 120, alto - 160)
        pygame.draw.rect(
            pantalla, COLORES["verde_principal"], panel_rect, 4, border_radius=20
        )

        # Título de pregunta
        titulo = fuente_subtitulo.render(
            "🧠 Pregunta Ecológica", True, COLORES["verde_principal"]
        )
        rect_titulo = titulo.get_rect(center=(ancho // 2, 120))
        pantalla.blit(titulo, rect_titulo)

        # Texto de la pregunta (dividir en líneas si es muy larga)
        palabras = pregunta["texto"].split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            if len(linea_actual + palabra) < 50:
                linea_actual += palabra + " "
            else:
                lineas.append(linea_actual.strip())
                linea_actual = palabra + " "
        if linea_actual:
            lineas.append(linea_actual.strip())

        y_pregunta = 180
        for linea in lineas:
            texto = fuente_principal.render(linea, True, COLORES["gris_oscuro"])
            rect = texto.get_rect(center=(ancho // 2, y_pregunta))
            pantalla.blit(texto, rect)
            y_pregunta += 35

        # Opciones de respuesta
        y_opciones = y_pregunta + 40
        for i, opcion in enumerate(pregunta["opciones"]):
            y_pos = y_opciones + i * 60

            rect_opcion = pygame.Rect(120, y_pos - 20, ancho - 240, 50)

            if i == seleccionado:
                pygame.draw.rect(
                    pantalla, COLORES["amarillo_sol"], rect_opcion, border_radius=10
                )
                color_texto = COLORES["gris_oscuro"]
            else:
                pygame.draw.rect(
                    pantalla, COLORES["gris_claro"], rect_opcion, border_radius=10
                )
                color_texto = COLORES["gris_oscuro"]

            pygame.draw.rect(
                pantalla, COLORES["gris_oscuro"], rect_opcion, 2, border_radius=10
            )

            texto_opcion = f"{i+1}. {opcion}"
            texto = fuente_principal.render(texto_opcion, True, color_texto)
            rect_texto = texto.get_rect(center=rect_opcion.center)
            pantalla.blit(texto, rect_texto)

        # Instrucciones
        instruccion = fuente_pequena.render(
            "Presiona 1, 2 o 3 para seleccionar", True, COLORES["verde_principal"]
        )
        rect_instr = instruccion.get_rect(center=(ancho // 2, alto - 100))
        pantalla.blit(instruccion, rect_instr)

        pygame.display.flip()

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1 and len(pregunta["opciones"]) >= 1:
                    seleccionado = 0
                    esperando = False
                elif evento.key == pygame.K_2 and len(pregunta["opciones"]) >= 2:
                    seleccionado = 1
                    esperando = False
                elif evento.key == pygame.K_3 and len(pregunta["opciones"]) >= 3:
                    seleccionado = 2
                    esperando = False

        pygame.time.wait(16)  # ~60 FPS

    time.sleep(0.5)
    return seleccionado == pregunta["respuesta"]


# ─────────────────────────────────────────────────────────────
# MODO LIBRE – CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────
def mostrar_opciones_libre(pantalla, nivel, vel_basura, vel_animal, vidas, opcion):
    """Muestra las opciones de configuración del modo libre."""
    ancho, alto = pantalla.get_size()
    fuente_principal, fuente_pequena, _, fuente_titulo, _ = get_fuentes()

    mapas = ["🌊 Océano Pacífico", "🌿 Amazonas", "🏙️ Ciudad de Lima"]
    opciones_config = [
        f"Mapa: {mapas[nivel]}",
        f"Velocidad Basura: {vel_basura}",
        f"Velocidad Animales: {vel_animal}",
        f"Vidas: {vidas}",
        "🚀 ¡Iniciar Aventura!",
    ]

    # Fondo gradiente
    for y in range(alto):
        intensidad = int(30 + (y / alto) * 40)
        color = (intensidad, intensidad + 15, intensidad + 35)
        pygame.draw.line(pantalla, color, (0, y), (ancho, y))

    # Título
    titulo = fuente_titulo.render(
        "⚙️ Configuración Personalizada", True, COLORES["verde_claro"]
    )
    rect_titulo = titulo.get_rect(center=(ancho // 2, 100))
    pantalla.blit(titulo, rect_titulo)

    # Opciones
    y_inicio = 200
    for i, texto in enumerate(opciones_config):
        y_pos = y_inicio + i * 80

        rect_opcion = pygame.Rect(150, y_pos - 25, ancho - 300, 60)

        if i == opcion:
            pygame.draw.rect(
                pantalla, COLORES["verde_principal"], rect_opcion, border_radius=15
            )
            color_texto = COLORES["blanco"]
        else:
            pygame.draw.rect(
                pantalla, (255, 255, 255), rect_opcion, border_radius=15
            )
            color_texto = COLORES["gris_claro"]

        pygame.draw.rect(
            pantalla, COLORES["verde_claro"], rect_opcion, 3, border_radius=15
        )

        texto_render = fuente_principal.render(texto, True, color_texto)
        rect_texto = texto_render.get_rect(center=rect_opcion.center)
        pantalla.blit(texto_render, rect_texto)

    # Instrucciones
    instrucciones = ["↑↓ Navegar   ←→ Cambiar valores   ENTER Confirmar"]

    for i, instr in enumerate(instrucciones):
        texto = fuente_pequena.render(instr, True, COLORES["amarillo_sol"])
        rect = texto.get_rect(center=(ancho // 2, alto - 80 + i * 25))
        pantalla.blit(texto, rect)
