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

# Clase para las balas disparadas por el jugador
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(imagen_bala, (5, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.velocidad_y = -10

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

# Clase para los enemigos
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(imagen_enemigo, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidad_y = random.randint(1, 5)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO_PANTALLA:
            self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.velocidad_y = random.randint(1, 5)

# Inicializar el grupo de sprites
todas_las_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()
  
# Crear la nave del jugador
jugador = NaveJugador()
todas_las_sprites.add(jugador)

# Crear los enemigos
for _ in range(8):
    enemigo = Enemigo()
    todas_las_sprites.add(enemigo)
    enemigos.add(enemigo)

# Puntuación
puntaje = 0
fuente = pygame.font.Font(None, 36)

# Reloj para controlar la tasa de fotogramas
reloj = pygame.time.Clock()

# Bucle principal del juego
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador.velocidad_x = -8
            elif evento.key == pygame.K_RIGHT:
                jugador.velocidad_x = 8
            elif evento.key == pygame.K_SPACE:
                jugador.disparar()
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador.velocidad_x = 0
    
    # Actualizar
    todas_las_sprites.update()

# Colisiones entre balas y enemigos
    colisiones = pygame.sprite.groupcollide(enemigos, balas, True, True)
    for colision in colisiones:
        puntaje += 1
        enemigo = Enemigo()
        todas_las_sprites.add(enemigo)
        enemigos.add(enemigo)
    
    # Colisiones entre jugador y enemigos
    colision_jugador = pygame.sprite.spritecollideany(jugador, enemigos)
    if colision_jugador:
        jugando = False  # Termina el juego si un enemigo toca al jugador
    
    # Dibujar
    pantalla.fill(NEGRO)
    todas_las_sprites.draw(pantalla)
    
    # Mostrar la puntuación
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    pantalla.blit(texto_puntaje, (10, 10))
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Controlar la tasa de fotogramas
    reloj.tick(60)

# Finalizar Pygame
pygame.quit()

# Mostrar el mensaje de fin del juego
print(f"¡Perdiste! Puntaje final: {puntaje}")