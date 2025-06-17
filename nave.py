import pygame
import math
import random

class Nave:
    def __init__(self, x, y):
        # Dimensiones mejoradas
        self.ancho = 70
        self.alto = 50
        
        # Superficie principal con transparencia
        self.imagen_base = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        self.imagen = self.imagen_base.copy()
        
        # Posición y movimiento
        self.rect = pygame.Rect(x - self.ancho//2, y - self.alto//2, self.ancho, self.alto)
        self.vel = 7
        self.vel_original = 7
        
        # Sistema de power-ups
        self.velocidad_extra = False
        self.tiempo_velocidad = 0
        self.escudo_activo = False
        self.tiempo_escudo = 0
        self.iman_activo = False
        self.tiempo_iman = 0
        
        # Animaciones y efectos
        self.angulo_rotacion = 0
        self.contador_pulso = 0
        self.contador_particulas = 0
        self.particulas_propulsion = []
        
        # Colores temáticos ecológicos
        self.colores = {
            'casco_principal': (45, 180, 85),      # Verde ecológico
            'casco_secundario': (25, 150, 65),     # Verde más oscuro
            'energia': (100, 255, 120),            # Verde brillante
            'propulsion': (80, 200, 255),          # Azul cristalino
            'detalle': (255, 255, 255),            # Blanco puro
            'escudo': (255, 215, 0),               # Dorado
            'velocidad': (255, 100, 100),          # Rojo energético
            'iman': (138, 43, 226)                 # Púrpura magnético
        }
        
        self.dibujar_nave()
    
    def dibujar_nave(self):
        """Dibuja la nave ecológica con un diseño mejorado y futurista"""
        self.imagen_base.fill((0, 0, 0, 0))  # Limpiar superficie
        
        # Efecto de pulso para la energía
        pulso = abs(math.sin(self.contador_pulso * 0.1)) * 20 + 10
        
        # === PROPULSORES TRASEROS ===
        # Propulsores principales (efecto de llama)
        for i in range(3):
            intensidad = random.randint(150, 255)
            color_llama = (100, intensidad, 255)
            tamaño = random.randint(8, 15)
            pygame.draw.ellipse(self.imagen_base, color_llama, 
                              (5 + i*2, self.alto - tamaño, 8, tamaño))
        
        # === CASCO PRINCIPAL ===
        # Cuerpo principal (forma aerodinámica)
        puntos_casco = [
            (self.ancho//2, 5),                    # Punta frontal
            (self.ancho - 10, self.alto//2 - 8),   # Lado derecho superior
            (self.ancho - 8, self.alto//2 + 8),    # Lado derecho inferior
            (self.ancho - 20, self.alto - 8),      # Cola derecha
            (20, self.alto - 8),                   # Cola izquierda
            (8, self.alto//2 + 8),                 # Lado izquierdo inferior
            (10, self.alto//2 - 8)                 # Lado izquierdo superior
        ]
        
        pygame.draw.polygon(self.imagen_base, self.colores['casco_principal'], puntos_casco)
        pygame.draw.polygon(self.imagen_base, self.colores['casco_secundario'], puntos_casco, 3)
        
        # === CABINA/COCKPIT ===
        # Ventana principal (cristal azulado)
        cockpit_rect = pygame.Rect(self.ancho//2 - 8, 12, 16, 20)
        pygame.draw.ellipse(self.imagen_base, (150, 200, 255, 180), cockpit_rect)
        pygame.draw.ellipse(self.imagen_base, (255, 255, 255), cockpit_rect, 2)
        
        # Reflejo en el cristal
        reflejo_rect = pygame.Rect(self.ancho//2 - 5, 14, 6, 8)
        pygame.draw.ellipse(self.imagen_base, (255, 255, 255, 100), reflejo_rect)
        
        # === SISTEMA DE ENERGÍA ECOLÓGICA ===
        # Núcleo energético central
        centro_x, centro_y = self.ancho//2, self.alto//2
        
        # Anillo exterior de energía (pulsa)
        color_energia = (*self.colores['energia'][:3], int(pulso * 8))
        pygame.draw.circle(self.imagen_base, self.colores['energia'], 
                         (centro_x, centro_y), int(12 + pulso//3), 2)
        
        # Núcleo central brillante
        pygame.draw.circle(self.imagen_base, (255, 255, 255), 
                         (centro_x, centro_y), 4)
        pygame.draw.circle(self.imagen_base, self.colores['energia'], 
                         (centro_x, centro_y), 6, 2)
        
        # === PANELES SOLARES LATERALES ===
        # Panel izquierdo
        panel_izq = pygame.Rect(15, self.alto//2 - 6, 12, 12)
        pygame.draw.rect(self.imagen_base, (50, 100, 200), panel_izq)
        # Líneas del panel solar
        for i in range(4):
            pygame.draw.line(self.imagen_base, (100, 150, 255), 
                           (16, panel_izq.top + i*3), (26, panel_izq.top + i*3))
        
        # Panel derecho
        panel_der = pygame.Rect(self.ancho - 27, self.alto//2 - 6, 12, 12)
        pygame.draw.rect(self.imagen_base, (50, 100, 200), panel_der)
        for i in range(4):
            pygame.draw.line(self.imagen_base, (100, 150, 255), 
                           (panel_der.left + 1, panel_der.top + i*3), 
                           (panel_der.right - 1, panel_der.top + i*3))
        
        # === DETALLES DECORATIVOS ===
        # Símbolo ecológico en la parte frontal
        simbolo_x, simbolo_y = self.ancho//2, 18
        pygame.draw.circle(self.imagen_base, self.colores['detalle'], 
                         (simbolo_x, simbolo_y), 6, 2)
        # Hoja dentro del círculo
        pygame.draw.arc(self.imagen_base, self.colores['energia'], 
                       (simbolo_x - 4, simbolo_y - 4, 8, 8), 0, math.pi/2, 2)
        
        # Líneas aerodinámicas
        for i in range(3):
            start_x = 25 + i*5
            pygame.draw.line(self.imagen_base, self.colores['detalle'],
                           (start_x, self.alto//2 - 2), (start_x + 8, self.alto//2 - 2), 1)
            pygame.draw.line(self.imagen_base, self.colores['detalle'],
                           (start_x, self.alto//2 + 2), (start_x + 8, self.alto//2 + 2), 1)
        
        # Copiar imagen base a imagen actual
        self.imagen = self.imagen_base.copy()
    
    def aplicar_efectos_powerup(self):
        """Aplica efectos visuales según los power-ups activos"""
        if self.escudo_activo:
            # Efecto de escudo dorado pulsante
            pulso_escudo = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 15 + 5
            pygame.draw.circle(self.imagen, (*self.colores['escudo'], 100), 
                             (self.ancho//2, self.alto//2), int(35 + pulso_escudo), 3)
            
        if self.velocidad_extra:
            # Efecto de velocidad (rastro rojo)
            for i in range(5):
                alpha = 255 - i * 50
                color = (*self.colores['velocidad'][:3], max(0, alpha))
                pygame.draw.circle(self.imagen, self.colores['velocidad'], 
                                 (10, self.alto//2 + i*2), 3 - i//2)
                pygame.draw.circle(self.imagen, self.colores['velocidad'], 
                                 (10, self.alto//2 - i*2), 3 - i//2)
        
        if self.iman_activo:
            # Efecto magnético (ondas púrpuras)
            tiempo = pygame.time.get_ticks()
            for i in range(3):
                radio = 40 + i*10 + (tiempo % 1000) // 50
                pygame.draw.circle(self.imagen, (*self.colores['iman'][:3], 50), 
                                 (self.ancho//2, self.alto//2), radio, 2)
    
    def actualizar_particulas(self):
        """Actualiza las partículas de propulsión"""
        # Crear nuevas partículas
        if self.contador_particulas % 3 == 0:
            for i in range(2):
                particula = {
                    'x': 15 + i*10,
                    'y': self.alto - 5,
                    'vel_x': random.uniform(-1, 1),
                    'vel_y': random.uniform(2, 5),
                    'vida': random.randint(20, 40),
                    'color': random.choice([(100, 180, 255), (150, 220, 255), (80, 160, 255)])
                }
                self.particulas_propulsion.append(particula)
        
        # Actualizar partículas existentes
        for particula in self.particulas_propulsion[:]:
            particula['x'] += particula['vel_x']
            particula['y'] += particula['vel_y']
            particula['vida'] -= 1
            
            if particula['vida'] <= 0:
                self.particulas_propulsion.remove(particula)
    
    def dibujar_particulas(self, pantalla):
        """Dibuja las partículas de propulsión en la pantalla"""
        for particula in self.particulas_propulsion:
            alpha = int((particula['vida'] / 40) * 255)
            color = (*particula['color'], alpha)
            pos_x = self.rect.x + particula['x']
            pos_y = self.rect.y + particula['y']
            
            # Dibujar partícula como círculo pequeño
            s = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(s, particula['color'], (3, 3), 2)
            pantalla.blit(s, (pos_x-3, pos_y-3))
    
    def mover(self, teclas, ancho, alto):
        """Movimiento mejorado con efectos"""
        # Guardar posición anterior para efectos
        pos_anterior = (self.rect.x, self.rect.y)
        
        # Movimiento básico
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT] and self.rect.right < ancho:
            self.rect.x += self.vel
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.vel
        if teclas[pygame.K_DOWN] and self.rect.bottom < alto:
            self.rect.y += self.vel
        
        # Actualizar contadores de animación
        self.contador_pulso += 1
        self.contador_particulas += 1
        
        # Actualizar efectos de power-ups
        self.actualizar_powerups()
        
        # Actualizar partículas
        self.actualizar_particulas()
        
        # Redibujar nave con efectos
        self.dibujar_nave()
        self.aplicar_efectos_powerup()
    
    def actualizar_powerups(self):
        """Actualiza el estado de los power-ups"""
        tiempo_actual = pygame.time.get_ticks()
        
        # Velocidad extra
        if self.velocidad_extra:
            if tiempo_actual - self.tiempo_velocidad > 5000:  # 5 segundos
                self.velocidad_extra = False
                self.vel = self.vel_original
        
        # Escudo
        if self.escudo_activo:
            if tiempo_actual - self.tiempo_escudo > 8000:  # 8 segundos
                self.escudo_activo = False
        
        # Imán
        if self.iman_activo:
            if tiempo_actual - self.tiempo_iman > 6000:  # 6 segundos
                self.iman_activo = False
    
    def activar_velocidad_extra(self):
        """Activa el power-up de velocidad extra"""
        self.velocidad_extra = True
        self.tiempo_velocidad = pygame.time.get_ticks()
        self.vel = self.vel_original * 1.5
    
    def activar_escudo(self):
        """Activa el power-up de escudo"""
        self.escudo_activo = True
        self.tiempo_escudo = pygame.time.get_ticks()
    
    def activar_iman(self):
        """Activa el power-up de imán ecológico"""
        self.iman_activo = True
        self.tiempo_iman = pygame.time.get_ticks()
    
    def dibujar(self, pantalla):
        """Dibuja la nave y sus efectos en pantalla"""
        # Dibujar partículas primero (atrás de la nave)
        self.dibujar_particulas(pantalla)
        
        # Dibujar la nave
        pantalla.blit(self.imagen, self.rect)
    
    def obtener_estado_powerups(self):
        """Retorna el estado actual de los power-ups para la interfaz"""
        return {
            'velocidad': self.velocidad_extra,
            'escudo': self.escudo_activo,
            'iman': self.iman_activo,
            'tiempo_velocidad': max(0, 5000 - (pygame.time.get_ticks() - self.tiempo_velocidad)) if self.velocidad_extra else 0,
            'tiempo_escudo': max(0, 8000 - (pygame.time.get_ticks() - self.tiempo_escudo)) if self.escudo_activo else 0,
            'tiempo_iman': max(0, 6000 - (pygame.time.get_ticks() - self.tiempo_iman)) if self.iman_activo else 0
        }