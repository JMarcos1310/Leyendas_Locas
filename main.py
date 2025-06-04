import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO, ALTO = 800, 600
FPS = 60

# Colores
AZUL_AGUA = (0, 102, 204)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
BOTON_COLOR = (0, 150, 255)
BOTON_HOVER = (0, 200, 255)

# Configurar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajolote vs Tláloc - ¡Corre por tu vida!")
reloj = pygame.time.Clock()

# Cargar recursos
ajolote_img = pygame.image.load("ajolote.png").convert_alpha()
ajolote_img = pygame.transform.scale(ajolote_img, (50, 50))

try:
    fondo_img = pygame.image.load("fondo.jpg").convert()
    fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))
except:
    fondo_img = None

# Música y sonidos
pygame.mixer.music.load("musica_fondo.mp3")
pygame.mixer.music.play(-1)
golpe_sonido = pygame.mixer.Sound("golpe.wav")

# Fuente
fuente = pygame.font.SysFont("Arial", 36)
fuente_chica = pygame.font.SysFont("Arial", 24)

def dibujar_texto(texto, fuente, color, x, y, centrado=True):
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect()
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    pantalla.blit(superficie, rect)

def boton(texto, x, y, ancho, alto):
    mouse = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()
    color = BOTON_HOVER if x < mouse[0] < x + ancho and y < mouse[1] < y + alto else BOTON_COLOR
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    dibujar_texto(texto, fuente_chica, BLANCO, x + ancho // 2, y + alto // 2)
    if x < mouse[0] < x + ancho and y < mouse[1] < y + alto:
        if clic[0] == 1:
            return True
    return False

def pantalla_inicio():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if fondo_img:
            pantalla.blit(fondo_img, (0, 0))
        else:
            pantalla.fill(AZUL_AGUA)

        dibujar_texto("Ajolote vs Tláloc", fuente, BLANCO, ANCHO // 2, 150)
        if boton("JUGAR", ANCHO // 2 - 75, 300, 150, 50):
            esperando = False

        pygame.display.flip()
        reloj.tick(FPS)

def pantalla_game_over(puntaje):
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.fill(NEGRO)
        dibujar_texto("¡Game Over!", fuente, BLANCO, ANCHO // 2, 150)
        dibujar_texto(f"Puntaje: {puntaje}", fuente_chica, BLANCO, ANCHO // 2, 220)

        if boton("Volver a jugar", ANCHO // 2 - 100, 300, 200, 50):
            esperando = False

        pygame.display.flip()
        reloj.tick(FPS)

def juego():
    ajolote = pygame.Rect(375, 500, 50, 50)
    velocidad = 5
    gotas = []
    enemigos = []
    contador_lluvia = 0
    contador_enemigos = 0
    puntaje = 0
    dificultad = 1
    vidas = 3

    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and ajolote.left > 0:
            ajolote.x -= velocidad
        if teclas[pygame.K_RIGHT] and ajolote.right < ANCHO:
            ajolote.x += velocidad
        if teclas[pygame.K_UP] and ajolote.top > 0:
            ajolote.y -= velocidad
        if teclas[pygame.K_DOWN] and ajolote.bottom < ALTO:
            ajolote.y += velocidad

        if fondo_img:
            pantalla.blit(fondo_img, (0, 0))
        else:
            pantalla.fill(AZUL_AGUA)

        pantalla.blit(ajolote_img, ajolote)

        # Generar lluvia
        contador_lluvia += 1
        if contador_lluvia >= max(10, 30 - dificultad):
            x = random.randint(0, ANCHO - 10)
            gotas.append(pygame.Rect(x, 0, 10, 20))
            contador_lluvia = 0

        # Generar enemigos
        contador_enemigos += 1
        if contador_enemigos >= 200:
            x = random.randint(0, ANCHO - 40)
            enemigos.append(pygame.Rect(x, 0, 40, 40))
            contador_enemigos = 0

        # Dibujar gotas
        for gota in gotas:
            gota.y += 5 + dificultad
            pygame.draw.rect(pantalla, (0, 0, 255), gota)

        # Dibujar enemigos
        for enemigo in enemigos:
            enemigo.y += 3 + dificultad // 2
            pygame.draw.rect(pantalla, (139, 0, 0), enemigo)

        # Colisiones con gotas
        for gota in gotas:
            if ajolote.colliderect(gota):
                vidas -= 1
                golpe_sonido.play()
                gotas.remove(gota)
                break

        # Colisiones con enemigos
        for enemigo in enemigos:
            if ajolote.colliderect(enemigo):
                vidas = 0
                golpe_sonido.play()
                break

        if vidas <= 0:
            pantalla_game_over(puntaje)
            return

        # Aumentar dificultad
        puntaje += 1
        if puntaje % 300 == 0:
            dificultad += 1

        # Dibujar texto
        dibujar_texto(f"Puntaje: {puntaje}", fuente_chica, BLANCO, 10, 10, centrado=False)
        dibujar_texto(f"Vidas: {vidas}", fuente_chica, BLANCO, 10, 40, centrado=False)

        pygame.display.flip()
        reloj.tick(FPS)

# Bucle principal
while True:
    pantalla_inicio()
    juego()
