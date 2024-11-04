import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Galaga Básico con Imágenes")

# Cargar imágenes
imagen_jugador = pygame.image.load("nave.gif").convert_alpha()
imagen_bala = pygame.image.load("bala.png").convert_alpha()
imagen_enemigo = pygame.image.load("enemigo.png").convert_alpha()

# Clase para la nave del jugador
class NaveJugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(imagen_jugador, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO_PANTALLA // 2
        self.rect.bottom = ALTO_PANTALLA - 10
        self.velocidad_x = 0

    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA

    def disparar(self):
        bala = Bala(self.rect.centerx, self.rect.top)
        todas_las_sprites.add(bala)
        balas.add(bala)
