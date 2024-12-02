import pygame
import random

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

efecto_disparo = pygame.mixer.Sound("music/atesp.mp3")
efecto_daño = pygame.mixer.Sound("music/daño.mp3")
musica_menu = "music/menu.mp3"
musica_juego = "music/gamemusic.mp3"
musica_game_over = "music/gameover.mp3"

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
pygame.display.set_caption("Space Breaker")

# Cargar imágenes
imagen_fondo = pygame.image.load("fotos/fondos/menu.jpeg").convert()
imagen_fondo2 = pygame.image.load("fotos/fondos/fondo1.jpeg").convert()
imagen_fondo3 = pygame.image.load("fotos/fondos/game.jpeg").convert()
imagen_nave1 = pygame.image.load("fotos/nave.gif").convert_alpha() 
imagen_nave2 = pygame.image.load("fotos/nave2.png").convert_alpha()
imagen_bala = pygame.image.load("fotos/bala.png").convert_alpha()
ataqueEspecial = pygame.image.load("fotos/balas.png").convert_alpha()
imagen_enemigo = pygame.image.load("fotos/enemigo.png").convert_alpha()
imagen_enemigo2 = pygame.image.load("fotos/enem2.webp").convert_alpha()

# Función para mostrar la pantalla de selección de nave
def mostrar_seleccion_nave(): #3
    pygame.mixer.music.load(musica_menu)
    pygame.mixer.music.play(-1)  # Música en bucle

    pantalla.fill(NEGRO)
    pantalla.blit(imagen_fondo, (0, 0))
    fuente = pygame.font.Font(None, 36)
    
    # Título de la pantalla
    texto_titulo = fuente.render("Selecciona tu nave", True, VERDE)
    pantalla.blit(texto_titulo, (ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2 - 100))

    # Instrucciones
    texto_instrucciones = fuente.render("Pulsa 1 para elegir nave Thanos", True, BLANCO)
    pantalla.blit(texto_instrucciones, (ANCHO_PANTALLA // 2 - 125, ALTO_PANTALLA // 2 + 25))
    texto_instrucciones2 = fuente.render("Pulsa 2 para elegir nave Ultron", True, BLANCO)
    pantalla.blit(texto_instrucciones2, (ANCHO_PANTALLA // 2 - 125, ALTO_PANTALLA // 2 + 75))
    
    # Actualizar pantalla
    pygame.display.flip()

    # Esperar que el jugador elija la nave
    seleccionada = None
    while seleccionada is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:  # Selección nave 1
                    seleccionada = 1
                if evento.key == pygame.K_2:  # Selección nave 2
                    seleccionada = 2
    pygame.mixer.music.stop()  # Detener la música
    return seleccionada

# Clase para la nave del jugador
class NaveJugador(pygame.sprite.Sprite):
    def __init__(self, seleccion_nave):
        super().__init__()
        if seleccion_nave == 1: 
            self.image = pygame.transform.scale(imagen_nave1, (70, 70))
        elif seleccion_nave == 2:
            self.image = pygame.transform.scale(imagen_nave2, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO_PANTALLA // 2
        self.rect.bottom = ALTO_PANTALLA - 10
        self.velocidad_x = 0
        self.energia = 0  # Comienza con 0 de energía
        self.energia_maxima = 100  # El valor máximo de energía
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 0
        self.ultimo_disparo_ataque = 0

    def update(self): 
        if self.invulnerable:
            if pygame.time.get_ticks() - self.tiempo_invulnerabilidad > 2000:  # 2 segundos de invulnerabilidad
                self.invulnerable = False

        self.rect.x += self.velocidad_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA

    def disparar(self):
        bala = Bala(self.rect.centerx, self.rect.top)
        todas_las_sprites.add(bala)
        balas.add(bala)
        efecto_disparo.play()

    def aumentar_energia(self, cantidad):
        self.energia = min(self.energia + cantidad, self.energia_maxima)

    def disparar_ataque_especial(self):
        if self.energia == self.energia_maxima:  # Solo dispara si la energía está llena
            self.energia = 0
            ataque = AtaqueEspecial(self.rect.centerx, self.rect.top)
            todas_las_sprites.add(ataque)
            ataque_especial.add(ataque)
            pygame.mixer.Sound("music/disparo.wav").play()

    def hacer_invulnerable(self):
        self.invulnerable = True
        self.tiempo_invulnerabilidad = pygame.time.get_ticks()  # Guardar el momento en que se hace invulnerable

# Clase para las balas disparadas por el jugador
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(imagen_bala, (25, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.velocidad_y = -10

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

class AtaqueEspecial(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

# Cargar la imagen del proyectil especial
        self.image = pygame.transform.scale(ataqueEspecial, (150, 150))  
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.velocidad_y = -5

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()
    
    def colision_en_area(self, enemigos, puntaje):
        colisiones = pygame.sprite.spritecollide(self, enemigos, False)
        for enemigo in colisiones:
            if self.rect.colliderect(enemigo.rect):  # Si el enemigo está dentro del área de colisión
                enemigo.kill()  # Destruir el enemigo
                puntaje += 1  # Sumar puntos por eliminar al enemigo
                enemigo = Enemigo()
                todas_las_sprites.add(enemigo)
                enemigos.add(enemigo)
        return puntaje 


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

#Clase para los enemigos especiales
class EnemigoEspecial(Enemigo):
    def __init__(self):
        super().__init__()
        self.vida = 2  # El enemigo especial necesita dos disparos para morir
        self.image = pygame.transform.scale(imagen_enemigo2, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidad_y = random.randint(3, 5)

    def update(self):
        super().update()

    def recibir_disparo(self):
        # Reducir la vida del enemigo al recibir un disparo
        self.vida -= 1
        if self.vida <= 0:
            self.kill()  # Eliminar el enemigo cuando su vida llega a 0
            return True  # Devuelve True para indicar que murió
        return False  # Devuelve False si aún tiene vida


def mostrar_pantalla_game_over(puntaje, tiempo_transcurrido):
    pygame.mixer.music.load(musica_game_over)
    pygame.mixer.music.play(-1)  # Reproducir música de Game Over en bucle
    
    pantalla.fill(NEGRO)
    pantalla.blit(imagen_fondo3, (0, 0))
    fuente = pygame.font.Font(None, 74)
    texto_game_over = fuente.render("GAME OVER", True, ROJO)
    pantalla.blit(texto_game_over, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 - 100))
    
    fuente_opciones = pygame.font.Font(None, 36)
    texto_reintentar = fuente_opciones.render("Presiona R para Reintentar", True, BLANCO)
    texto_salir = fuente_opciones.render("Presiona Esc para Salir", True, BLANCO)
    pantalla.blit(texto_reintentar, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2))
    pantalla.blit(texto_salir, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 40))
    
    texto_puntaje = fuente_opciones.render(f"Puntaje final: {puntaje}", True, BLANCO)
    pantalla.blit(texto_puntaje, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 80))
    
    texto_tiempo = fuente_opciones.render(f"Tiempo jugado: {tiempo_transcurrido // 1000} s", True, BLANCO)
    pantalla.blit(texto_tiempo, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 120))
    
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False
                    pygame.mixer.music.stop()  # Detener la música de Game Over
                    main()  # Reiniciar el juego
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

def mostrar_menu():
    pygame.mixer.music.load(musica_menu)
    pygame.mixer.music.play(-1)  # Reproducir música del menú en bucle
    
    pantalla.fill(NEGRO)
    pantalla.blit(imagen_fondo, (0, 0))
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_opciones = pygame.font.Font(None, 36)
    
    texto_titulo = fuente_titulo.render("Juego de naves", True, VERDE)
    pantalla.blit(texto_titulo, (ANCHO_PANTALLA // 2 - 180, ALTO_PANTALLA // 2 - 200))
    texto_iniciar = fuente_opciones.render("Presiona Espacio para Iniciar", True, BLANCO)
    pantalla.blit(texto_iniciar, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 - 100))
    texto_salir = fuente_opciones.render("Presiona Esc para Salir", True, BLANCO)
    pantalla.blit(texto_salir, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 - 50))

    texto_con = fuente_opciones.render("CONTROLES", True, BLANCO)
    pantalla.blit(texto_con, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 25))
    imagen_iniciar = pygame.image.load('fotos/teclas/a.png')
    pantalla.blit(imagen_iniciar, (ANCHO_PANTALLA // 2 - 200, ALTO_PANTALLA // 2 + 50))
    texto_iniciar = fuente_opciones.render("mover a la izquierda", True, BLANCO)
    pantalla.blit(texto_iniciar, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 65))
    imagen_iniciar = pygame.image.load('fotos/teclas/d.png')
    pantalla.blit(imagen_iniciar, (ANCHO_PANTALLA // 2 - 200, ALTO_PANTALLA // 2 + 100))
    texto_iniciar = fuente_opciones.render("mover a la derecha", True, BLANCO)
    pantalla.blit(texto_iniciar, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 115))
    imagen_iniciar = pygame.image.load('fotos/teclas/espacio.png')
    pantalla.blit(imagen_iniciar, (ANCHO_PANTALLA // 2 - 200, ALTO_PANTALLA // 2 + 150))
    texto_iniciar = fuente_opciones.render("disparar", True, BLANCO)
    pantalla.blit(texto_iniciar, (ANCHO_PANTALLA // 2 + 75, ALTO_PANTALLA // 2 + 165))
    imagen_iniciar = pygame.image.load('fotos/teclas/e.png')
    pantalla.blit(imagen_iniciar, (ANCHO_PANTALLA // 2 - 200, ALTO_PANTALLA // 2 + 200))
    texto_iniciar = fuente_opciones.render("ataque especial", True, BLANCO)
    pantalla.blit(texto_iniciar, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 215))

    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando = False  # Iniciar el juego
                    pygame.mixer.music.stop()  # Detener la música del menú
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()       

def main():
    global todas_las_sprites, enemigos, balas, ataque_especial

    seleccion_nave = mostrar_seleccion_nave()  # Mostrar pantalla de selección de nave
    
    pygame.mixer.music.load(musica_juego)
    pygame.mixer.music.play(-1)
    
    # Inicializar el grupo de sprites
    todas_las_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    balas = pygame.sprite.Group()
    ataque_especial = pygame.sprite.Group()
    
    # Crear la nave del jugador con la nave seleccionada
    jugador = NaveJugador(seleccion_nave)
    todas_las_sprites.add(jugador)

    # Crear los enemigos, algunos de ellos pueden ser especiales
    for _ in range(8):
        if random.random() < 0.2:  # Probabilidad del 20% de crear un enemigo especial
            enemigo = EnemigoEspecial()
        else:
            enemigo = Enemigo()
        todas_las_sprites.add(enemigo)
        enemigos.add(enemigo)

    # Inicializar las vidas
    vidas = 3

    tiempo_inicio = pygame.time.get_ticks()
    tiempo_90_segundos = tiempo_inicio + 90000  # 90 segundos
    tiempo_150_segundos = tiempo_inicio + 150000 # 180 segundos

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
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_d:
                    jugador.velocidad_x = -8
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_a:
                    jugador.velocidad_x = 8
                elif evento.key == pygame.K_SPACE:
                    jugador.disparar()
                elif evento.key == pygame.K_e:
                    if jugador.disparar_ataque_especial():  # Solo disparar si la energía está llena
                        pass  # Disparar ataque especial
                    #jugador.disparar_ataque_especial()
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    jugador.velocidad_x = 0
        
        # Actualizar
        todas_las_sprites.update()

        # Colisiones entre balas y enemigos
        colisiones = pygame.sprite.groupcollide(enemigos, balas, False, True)
        for enemigo, balas_impactadas in colisiones.items():
            if isinstance(enemigo, EnemigoEspecial):
                # Reducir la vida de los enemigos especiales al ser alcanzados
                enemigo_muerto = enemigo.recibir_disparo()  # Reducir vida
                if enemigo_muerto:
                    puntaje += 2  # Aumentar puntaje al morir
                    jugador.aumentar_energia(10)
            else:
                # Los enemigos normales se destruyen inmediatamente
                puntaje += 1
                jugador.aumentar_energia(5)
                enemigo.kill()
                # Reemplazar el enemigo destruido por uno nuevo
                nuevo_enemigo = Enemigo()
                todas_las_sprites.add(nuevo_enemigo)
                enemigos.add(nuevo_enemigo)
        
        for ataque in ataque_especial:
            puntaje = ataque.colision_en_area(enemigos, puntaje)
        
        # Colisiones entre jugador y enemigos #9
        if not jugador.invulnerable:  # Solo chequear si no está invulnerable
            colision_jugador = pygame.sprite.spritecollideany(jugador, enemigos)
            if colision_jugador:
                vidas -= 1  # Perder una vida
                efecto_daño.play()
                if vidas <= 0:
                    jugando = False  # Termina el juego si el jugador no tiene vidas
                else:
                    # Hacer invulnerable al jugador por 2 segundos
                    jugador.hacer_invulnerable()
                    # Mover al jugador a la posición inicial
                    jugador.rect.centerx = ANCHO_PANTALLA // 2
                    jugador.rect.bottom = ALTO_PANTALLA - 10
                    pygame.time.delay(500)  # Pausar un poco después de perder una vida

        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio
        segundos_transcurridos = tiempo_transcurrido // 1000
        milisegundos_transcurridos = (tiempo_transcurrido % 1000) // 10

        if pygame.time.get_ticks() >= tiempo_90_segundos:
            for _ in range(8): # Agregar 8 enemigos adicionales
                if random.random() < 0.4:  # Probabilidad del 40% de crear un enemigo especial
                    enemigo = EnemigoEspecial()
                else:
                    enemigo = Enemigo()
                todas_las_sprites.add(enemigo)
                enemigos.add(enemigo)
            tiempo_90_segundos = float('inf')  # Evitar que agregue más de una vez

        # Agregar aún más enemigos a los 180 segundos
        if pygame.time.get_ticks() >= tiempo_150_segundos:
            for _ in range(16):  # Agregar 16 enemigos adicionales
                if random.random() < 0.6:  # Probabilidad del 60% de crear un enemigo especial
                    enemigo = EnemigoEspecial()
                else:
                    enemigo = Enemigo()
                todas_las_sprites.add(enemigo)
                enemigos.add(enemigo)
            tiempo_150_segundos = float('inf') 

        # Dibujar
        pantalla.fill(NEGRO)
        pantalla.blit(imagen_fondo2, (0, 0)) #8
        todas_las_sprites.draw(pantalla)
        
        # Mostrar la puntuación
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        pantalla.blit(texto_puntaje, (10, 10))

        texto_tiempo = fuente.render(f"Tiempo: {segundos_transcurridos}:{milisegundos_transcurridos:02d}", True, BLANCO)
        pantalla.blit(texto_tiempo, (ANCHO_PANTALLA - 200, 10))

        # Mostrar las vidas
        texto_vidas = fuente.render(f"Vidas: {vidas}", True, ROJO)
        pantalla.blit(texto_vidas, (10, 50))  # Mostrar debajo de la puntuación

        # Mostrar la barra de energía
        pygame.draw.rect(pantalla, (255, 0, 0), (10, 90, jugador.energia * 2, 20))  # Rojo
        pygame.draw.rect(pantalla, (255, 255, 255), (10, 90, jugador.energia_maxima * 2, 20), 2)  # Borde blanco

        # Actualizar la pantalla
        pygame.display.flip()
        
        # Controlar la tasa de fotogramas
        reloj.tick(60)

    pygame.mixer.music.stop()
    mostrar_pantalla_game_over(puntaje, tiempo_transcurrido)

# Iniciar el juego desde el menú
mostrar_menu()
main()