import random
import math
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *

from interfaz import obtener_dimensiones_pantalla


# ─────────────────────────────────────────────────────────────
# Dibujos básicos mejorados
# ─────────────────────────────────────────────────────────────
def dibujar_cubo_ecologico():
    """
    Cubo central que representa el planeta con diferentes biomas
    en cada cara, ahora con bordes definidos.
    """
    # Caras con colores de biomas
    caras = [
        # Frente (bosque)
        ([(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)], (0.0, 0.8, 0.2)),
        # Atrás (océano)
        ([(-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1)], (0.0, 0.4, 0.9)),
        # Izquierda (selva)
        ([(-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1)], (0.0, 0.6, 0.15)),
        # Derecha (desierto)
        ([(1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1)], (0.95, 0.85, 0.3)),
        # Arriba (cielo)
        ([(-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1)], (0.5, 0.8, 1.0)),
        # Abajo (tierra)
        ([(-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)], (0.5, 0.3, 0.1)),
    ]

    glBegin(GL_QUADS)
    for vertices, color in caras:
        glColor3f(*color)
        for v in vertices:
            glVertex3f(*v)
    glEnd()

    # Dibujar bordes negros para definir mejor el cubo
    glLineWidth(2.0)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    # Bordes del cubo
    edges = [
        (-1, -1, -1), (-1, -1, 1),
        (-1, -1, 1), (1, -1, 1),
        (1, -1, 1), (1, -1, -1),
        (1, -1, -1), (-1, -1, -1),
        (-1, 1, -1), (-1, 1, 1),
        (-1, 1, 1), (1, 1, 1),
        (1, 1, 1), (1, 1, -1),
        (1, 1, -1), (-1, 1, -1),
        (-1, -1, -1), (-1, 1, -1),
        (-1, -1, 1), (-1, 1, 1),
        (1, -1, 1), (1, 1, 1),
        (1, -1, -1), (1, 1, -1),
    ]
    for i in range(0, len(edges), 2):
        glVertex3f(*edges[i])
        glVertex3f(*edges[i + 1])
    glEnd()


def dibujar_cubo_con_brillo(r, g, b, brillo=0.2):
    """Cubo con efecto de iluminación simple."""
    caras = [
        ([(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)], 1.0),      # Frente
        ([(-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1)], 0.6),  # Atrás
        ([(-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1)], 0.8),  # Izquierda
        ([(1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1)], 0.8),      # Derecha
        ([(-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1)], 1.0 + brillo),  # Arriba
        ([(-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)], 0.5),  # Abajo
    ]

    glBegin(GL_QUADS)
    for vertices, intensidad in caras:
        glColor3f(r * intensidad, g * intensidad, b * intensidad)
        for v in vertices:
            glVertex3f(*v)
    glEnd()


def dibujar_nave_ecologica():
    """Nave 3D mejorada con más detalle."""
    # Cuerpo principal (verde brillante)
    glPushMatrix()
    glScalef(1.8, 0.6, 1.2)
    dibujar_cubo_con_brillo(0.15, 0.9, 0.5, brillo=0.3)
    glPopMatrix()

    # Cabina (amarillo brillante)
    glPushMatrix()
    glTranslatef(0.0, 0.5, 0.0)
    glScalef(0.8, 0.4, 0.8)
    dibujar_cubo_con_brillo(0.95, 0.95, 0.3, brillo=0.4)
    glPopMatrix()

    # Alas laterales
    glPushMatrix()
    glTranslatef(-1.5, 0.0, 0.0)
    glScalef(0.5, 0.15, 0.8)
    dibujar_cubo_con_brillo(0.1, 0.7, 0.4)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.5, 0.0, 0.0)
    glScalef(0.5, 0.15, 0.8)
    dibujar_cubo_con_brillo(0.1, 0.7, 0.4)
    glPopMatrix()

    # Propulsores (azul brillante)
    for x_pos in [-1.0, 1.0]:
        glPushMatrix()
        glTranslatef(x_pos, -0.4, -0.6)
        glScalef(0.3, 0.3, 0.5)
        dibujar_cubo_con_brillo(0.3, 0.5, 0.95, brillo=0.5)
        glPopMatrix()


def dibujar_estrella(puntas=5, radio_ext=1.0, radio_int=0.4):
    """Dibuja una estrella decorativa en 3D."""
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(puntas * 2 + 1):
        angulo = math.pi * i / puntas
        radio = radio_ext if i % 2 == 0 else radio_int
        x = radio * math.cos(angulo)
        y = radio * math.sin(angulo)
        glVertex3f(x, y, 0)
    glEnd()


def dibujar_particula_reciclaje():
    """Partícula con símbolo de reciclaje simplificado."""
    # Base verde
    glPushMatrix()
    glScalef(1.0, 1.0, 0.3)
    dibujar_cubo_con_brillo(0.2, 0.95, 0.45, brillo=0.4)
    glPopMatrix()

    # Símbolo de reciclaje (triángulos pequeños)
    glColor3f(1.0, 1.0, 1.0)
    for angulo in [0, 120, 240]:
        glPushMatrix()
        glRotatef(angulo, 0, 0, 1)
        glTranslatef(0.4, 0.0, 0.5)
        glScalef(0.2, 0.2, 0.2)
        glBegin(GL_TRIANGLES)
        glVertex3f(0, 0.5, 0)
        glVertex3f(-0.4, -0.5, 0)
        glVertex3f(0.4, -0.5, 0)
        glEnd()
        glPopMatrix()


def dibujar_particula_toxica():
    """Partícula tóxica con efecto peligroso."""
    # Base roja pulsante
    glPushMatrix()
    glScalef(1.0, 1.0, 0.3)
    dibujar_cubo_con_brillo(0.95, 0.15, 0.15, brillo=0.3)
    glPopMatrix()

    # Símbolo de peligro (X amarilla)
    glColor3f(1.0, 1.0, 0.0)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex3f(-0.4, -0.4, 0.5)
    glVertex3f(0.4, 0.4, 0.5)
    glVertex3f(-0.4, 0.4, 0.5)
    glVertex3f(0.4, -0.4, 0.5)
    glEnd()


def dibujar_power_up():
    """Power-up especial (estrella dorada)."""
    glColor3f(1.0, 0.9, 0.0)
    glPushMatrix()
    glRotatef(45, 0, 0, 1)
    dibujar_estrella(5, 0.8, 0.3)
    glPopMatrix()

    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glRotatef(45, 0, 0, 1)
    dibujar_estrella(5, 0.8, 0.3)
    glPopMatrix()


def dibujar_fondo_estrellas(estrellas):
    """Dibuja un campo de estrellas en el fondo."""
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for estrella in estrellas:
        glColor3f(*estrella["color"])
        glVertex3f(*estrella["pos"])
    glEnd()


def dibujar_texto_3d(texto, x, y, z, escala, color):
    """Dibuja texto flotante en el espacio 3D (muy básico)."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(escala, escala, escala)
    glColor3f(*color)

    glLineWidth(3.0)
    offset_x = 0
    for char in texto:
        if char == '+':
            glBegin(GL_LINES)
            glVertex3f(offset_x - 0.15, 0, 0)
            glVertex3f(offset_x + 0.15, 0, 0)
            glVertex3f(offset_x, -0.15, 0)
            glVertex3f(offset_x, 0.15, 0)
            glEnd()
            offset_x += 0.4
        elif char == '-':
            glBegin(GL_LINES)
            glVertex3f(offset_x - 0.15, 0, 0)
            glVertex3f(offset_x + 0.15, 0, 0)
            glEnd()
            offset_x += 0.4
        elif char.isdigit():
            # Números simplificados: solo avanzamos
            offset_x += 0.4

    glPopMatrix()


# ─────────────────────────────────────────────────────────────
# Minijuego 3D mejorado: Lluvia de Basura
# ─────────────────────────────────────────────────────────────
def ejecutar_demo_opengl():
    """
    Modo 3D OpenGL mejorado:
    - Mueves la nave con ← / → o A / D
    - ESPACIO para usar escudo temporal (si tienes carga)
    - Atrapa cubos verdes (reciclables) = +10 puntos
    - Evita cubos rojos (tóxicos) = -1 vida
    - Estrellas doradas = +25 puntos + recarga escudo
    - Sistema de niveles con dificultad progresiva
    - Efectos visuales mejorados con FEEDBACK CLARO
    - ESC para salir
    """

    pygame.init()
    ANCHO, ALTO = obtener_dimensiones_pantalla()

    pantalla = pygame.display.set_mode((ANCHO, ALTO), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Guardianes del Planeta - Modo 3D OpenGL")

    # Configuración OpenGL
    glViewport(0, 0, ANCHO, ALTO)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, ANCHO / ALTO, 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    clock = pygame.time.Clock()
    fuente = pygame.font.Font(None, 48)
    fuente_grande = pygame.font.Font(None, 72)

    # Estado del jugador
    jugador_x = 0.0
    jugador_y = -3.8
    velocidad_base = 7.0
    velocidad_jugador = velocidad_base

    # Sistema de escudo
    escudo_activo = False
    escudo_duracion = 0.0
    escudo_max = 3.0
    escudo_carga = escudo_max
    escudo_cooldown = 0.0

    # Objetos y juego
    objetos = []
    particulas_efectos = []
    mensajes_flotantes = []  # mensajes de feedback

    # Flash de pantalla para feedback
    flash_pantalla = 0.0
    flash_color = (0, 0, 0)

    # Estrellas de fondo
    estrellas_fondo = []
    for _ in range(100):
        estrellas_fondo.append({
            "pos": (
                random.uniform(-15, 15),
                random.uniform(-10, 10),
                random.uniform(-30, -10)
            ),
            "color": (
                random.uniform(0.7, 1.0),
                random.uniform(0.7, 1.0),
                random.uniform(0.8, 1.0)
            )
        })

    # Variables de spawning
    tiempo_spawn = 0.0
    intervalo_spawn = 1.0
    tiempo_powerup = 0.0
    intervalo_powerup = 8.0

    # Puntuación y progreso
    puntaje = 0
    vidas = 3
    nivel = 1
    puntaje_siguiente_nivel = 100

    # Rotaciones
    angulo_cubo = 0.0
    angulo_nave = 0.0

    # Combo system
    combo = 0
    tiempo_combo = 0.0
    max_combo = 0

    # Textura para el flash (HUD)
    hud_texture = glGenTextures(1)

    ejecutando = True

    while ejecutando:
        dt_ms = clock.tick(60)
        dt = dt_ms / 1000.0

        # ── Eventos ───────────────────────────────────────────
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_SPACE:
                    if escudo_carga >= escudo_max and escudo_cooldown <= 0:
                        escudo_activo = True
                        escudo_duracion = 0.0
                        escudo_carga = 0.0
                        escudo_cooldown = 5.0

        # ── Movimiento del jugador ────────────────────────────
        teclas = pygame.key.get_pressed()
        velocidad_actual = velocidad_jugador * dt

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jugador_x -= velocidad_actual
            angulo_nave = min(15, angulo_nave + 300 * dt)
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jugador_x += velocidad_actual
            angulo_nave = max(-15, angulo_nave - 300 * dt)
        else:
            if angulo_nave > 0:
                angulo_nave = max(0, angulo_nave - 200 * dt)
            else:
                angulo_nave = min(0, angulo_nave + 200 * dt)

        jugador_x = max(-5.0, min(5.0, jugador_x))

        # ── Sistema de escudo ─────────────────────────────────
        if escudo_activo:
            escudo_duracion += dt
            if escudo_duracion >= 3.0:
                escudo_activo = False

        if escudo_cooldown > 0:
            escudo_cooldown -= dt

        if escudo_carga < escudo_max and not escudo_activo:
            escudo_carga = min(escudo_max, escudo_carga + dt * 0.5)

        # ── Sistema de combo ──────────────────────────────────
        if tiempo_combo > 0:
            tiempo_combo -= dt
        else:
            combo = 0

        # ── Flash de pantalla ─────────────────────────────────
        if flash_pantalla > 0:
            flash_pantalla -= dt * 3

        # ── Spawning de objetos ───────────────────────────────
        tiempo_spawn += dt
        dificultad = 1.0 + (nivel - 1) * 0.15
        intervalo_actual = max(0.5, intervalo_spawn - (nivel - 1) * 0.05)

        if tiempo_spawn >= intervalo_actual:
            tiempo_spawn = 0.0
            x = random.uniform(-5.0, 5.0)

            rand = random.random()
            if rand < 0.65:
                kind = "good"
            else:
                kind = "bad"

            speed = random.uniform(2.5, 3.5) * dificultad
            objetos.append({
                "x": x,
                "y": 5.5,
                "speed": speed,
                "kind": kind,
                "rotation": random.uniform(0, 360),
                "rot_speed": random.uniform(-180, 180)
            })

        # Power-ups
        tiempo_powerup += dt
        if tiempo_powerup >= intervalo_powerup:
            tiempo_powerup = 0.0
            x = random.uniform(-4.5, 4.5)
            objetos.append({
                "x": x,
                "y": 5.5,
                "speed": 2.0,
                "kind": "powerup",
                "rotation": 0,
                "rot_speed": 360
            })

        # ── Actualizar objetos ────────────────────────────────
        nuevos_objetos = []
        for obj in objetos:
            obj["y"] -= obj["speed"] * dt
            obj["rotation"] += obj["rot_speed"] * dt

            # Colisión
            distancia = math.sqrt((obj["x"] - jugador_x) ** 2 + (obj["y"] - jugador_y) ** 2)
            if distancia < 0.9:
                if obj["kind"] == "good":
                    puntos_ganados = 10 * (1 + combo // 3)
                    puntaje += puntos_ganados
                    combo += 1
                    max_combo = max(max_combo, combo)
                    tiempo_combo = 2.0

                    # FEEDBACK VISUAL - Mensaje flotante
                    mensajes_flotantes.append({
                        "texto": f"+{puntos_ganados}",
                        "x": obj["x"],
                        "y": obj["y"],
                        "vida": 1.0,
                        "color": (0.2, 1.0, 0.45),
                        "escala": 0.02
                    })

                    # Flash verde
                    flash_pantalla = 0.3
                    flash_color = (0, 255, 0)

                    # Partículas
                    for _ in range(8):
                        particulas_efectos.append({
                            "x": obj["x"],
                            "y": obj["y"],
                            "vx": random.uniform(-2, 2),
                            "vy": random.uniform(1, 3),
                            "vida": 0.6,
                            "color": (0.2, 0.95, 0.45)
                        })

                elif obj["kind"] == "bad":
                    if not escudo_activo:
                        vidas -= 1
                        combo = 0

                        # FEEDBACK VISUAL - Mensaje de daño
                        mensajes_flotantes.append({
                            "texto": "-1 VIDA",
                            "x": obj["x"],
                            "y": obj["y"],
                            "vida": 1.2,
                            "color": (1.0, 0.1, 0.1),
                            "escala": 0.025
                        })

                        # Flash rojo
                        flash_pantalla = 0.5
                        flash_color = (255, 0, 0)

                        # Partículas rojas
                        for _ in range(12):
                            particulas_efectos.append({
                                "x": obj["x"],
                                "y": obj["y"],
                                "vx": random.uniform(-3, 3),
                                "vy": random.uniform(1, 4),
                                "vida": 0.7,
                                "color": (0.95, 0.15, 0.15)
                            })
                    else:
                        # Bloqueado por escudo
                        mensajes_flotantes.append({
                            "texto": "BLOQUEADO",
                            "x": obj["x"],
                            "y": obj["y"],
                            "vida": 0.8,
                            "color": (0.3, 0.7, 1.0),
                            "escala": 0.015
                        })

                elif obj["kind"] == "powerup":
                    puntaje += 25
                    escudo_carga = escudo_max

                    # FEEDBACK VISUAL - Power-up
                    mensajes_flotantes.append({
                        "texto": "+25 POWER!",
                        "x": obj["x"],
                        "y": obj["y"],
                        "vida": 1.5,
                        "color": (1.0, 0.9, 0.0),
                        "escala": 0.03
                    })

                    # Flash dorado
                    flash_pantalla = 0.4
                    flash_color = (255, 215, 0)

                    # Partículas doradas
                    for _ in range(15):
                        particulas_efectos.append({
                            "x": obj["x"],
                            "y": obj["y"],
                            "vx": random.uniform(-4, 4),
                            "vy": random.uniform(2, 5),
                            "vida": 0.9,
                            "color": (1.0, 0.9, 0.0)
                        })
                continue

            # Salió de pantalla
            if obj["y"] < -6.5:
                if obj["kind"] == "good":
                    puntaje = max(0, puntaje - 5)
                    combo = 0

                    # FEEDBACK - Perdiste puntos
                    mensajes_flotantes.append({
                        "texto": "-5",
                        "x": obj["x"],
                        "y": -6.0,
                        "vida": 0.8,
                        "color": (1.0, 0.5, 0.0),
                        "escala": 0.015
                    })
                continue

            nuevos_objetos.append(obj)

        objetos = nuevos_objetos

        # ── Actualizar partículas ─────────────────────────────
        nuevas_particulas = []
        for p in particulas_efectos:
            p["vida"] -= dt
            if p["vida"] > 0:
                p["x"] += p["vx"] * dt
                p["y"] += p["vy"] * dt
                p["vy"] -= 5 * dt
                nuevas_particulas.append(p)
        particulas_efectos = nuevas_particulas

        # ── Actualizar mensajes flotantes ─────────────────────
        nuevos_mensajes = []
        for msg in mensajes_flotantes:
            msg["vida"] -= dt
            if msg["vida"] > 0:
                msg["y"] += dt * 2  # Flotar hacia arriba
                msg["escala"] += dt * 0.01  # Crecer ligeramente
                nuevos_mensajes.append(msg)
        mensajes_flotantes = nuevos_mensajes

        # ── Sistema de niveles ────────────────────────────────
        if puntaje >= puntaje_siguiente_nivel:
            nivel += 1
            puntaje_siguiente_nivel += 100 * nivel
            velocidad_jugador = velocidad_base + (nivel - 1) * 0.5

            # Mensaje de nivel
            mensajes_flotantes.append({
                "texto": f"NIVEL {nivel}",
                "x": 0,
                "y": 0,
                "vida": 2.0,
                "color": (1.0, 1.0, 1.0),
                "escala": 0.04
            })

        # ── Rotación del cubo central ─────────────────────────
        angulo_cubo += 35.0 * dt

        # ── Condición de fin ──────────────────────────────────
        if vidas <= 0:
            ejecutando = False

        # ── Renderizado OpenGL 3D ─────────────────────────────
        glClearColor(0.01, 0.02, 0.08, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(0.0, 0.0, 14.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        # Estrellas de fondo
        dibujar_fondo_estrellas(estrellas_fondo)

        # Cubo ecológico central
        glPushMatrix()
        glTranslatef(0.0, 1.2, -5.0)
        glRotatef(angulo_cubo, 0, 1, 0)
        glRotatef(angulo_cubo / 2.5, 1, 0, 0)
        glScalef(1.6, 1.6, 1.6)
        dibujar_cubo_ecologico()
        glPopMatrix()

        # Nave del jugador
        glPushMatrix()
        glTranslatef(jugador_x, jugador_y, 0.0)
        glRotatef(angulo_nave, 0, 0, 1)
        glScalef(0.5, 0.5, 0.5)
        dibujar_nave_ecologica()
        glPopMatrix()

        # Escudo visual
        if escudo_activo:
            glPushMatrix()
            glTranslatef(jugador_x, jugador_y, 0.0)
            alpha = 0.3 + 0.2 * math.sin(escudo_duracion * 10)
            glColor4f(0.3, 0.7, 1.0, alpha)
            glScalef(1.5, 1.5, 1.5)
            for lat in range(0, 180, 30):
                glBegin(GL_LINE_LOOP)
                for lon in range(0, 360, 20):
                    x = math.sin(math.radians(lat)) * math.cos(math.radians(lon))
                    y = math.sin(math.radians(lat)) * math.sin(math.radians(lon))
                    z = math.cos(math.radians(lat))
                    glVertex3f(x, y, z)
                glEnd()
            glPopMatrix()

        # Objetos que caen
        for obj in objetos:
            glPushMatrix()
            glTranslatef(obj["x"], obj["y"], 0.0)
            glRotatef(obj["rotation"], 0, 1, 0)
            glScalef(0.6, 0.6, 0.6)

            if obj["kind"] == "good":
                dibujar_particula_reciclaje()
            elif obj["kind"] == "bad":
                dibujar_particula_toxica()
            elif obj["kind"] == "powerup":
                dibujar_power_up()

            glPopMatrix()

        # Partículas de efectos
        for p in particulas_efectos:
            glPushMatrix()
            glTranslatef(p["x"], p["y"], 0.5)
            alpha = max(0.0, min(1.0, p["vida"] / 0.8))
            glColor4f(p["color"][0], p["color"][1], p["color"][2], alpha)
            glPointSize(8.0)
            glBegin(GL_POINTS)
            glVertex3f(0, 0, 0)
            glEnd()
            glPopMatrix()

        # ── Mensajes flotantes en 3D ──────────────────────────
        for msg in mensajes_flotantes:
            dibujar_texto_3d(
                msg["texto"],
                msg["x"],
                msg["y"],
                1.0,
                msg["escala"],
                msg["color"]
            )

        # ── HUD con OpenGL 2D (flash, etc) ────────────────────
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, ANCHO, ALTO, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)

        # Flash de pantalla
        if flash_pantalla > 0:
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((*flash_color, int(flash_pantalla * 100)))

            texture_data = pygame.image.tostring(overlay, "RGBA", True)

            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, hud_texture)
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGBA,
                ANCHO,
                ALTO,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                texture_data
            )
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glColor4f(1, 1, 1, 1)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(0, 0)
            glTexCoord2f(1, 0)
            glVertex2f(ANCHO, 0)
            glTexCoord2f(1, 1)
            glVertex2f(ANCHO, ALTO)
            glTexCoord2f(0, 1)
            glVertex2f(0, ALTO)
            glEnd()
            glDisable(GL_TEXTURE_2D)

        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        # ── HUD en título de la ventana ───────────────────────
        titulo = f"Guardianes 3D | Pts: {puntaje} | ❤️×{vidas} | Nv.{nivel}"
        if combo > 2:
            titulo += f" | Combo ×{combo}!"
        if escudo_activo:
            titulo += " | 🛡️ ESCUDO"
        pygame.display.set_caption(titulo)

        # Flip FINAL del frame
        pygame.display.flip()

    # Pantalla final (fuera del while pero dentro de la función)
    pygame.display.set_mode((ANCHO, ALTO))

    print("\n" + "=" * 50)
    print("  MISIÓN COMPLETADA - GUARDIANES DEL PLANETA")
    print("=" * 50)
    print(f"  Puntaje Final: {puntaje}")
    print(f"  Nivel Alcanzado: {nivel}")
    print(f"  Combo Máximo: {max_combo}")
    print("=" * 50 + "\n")
