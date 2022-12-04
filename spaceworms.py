import pygame
import sys
import random

# Variables para creacion de la ventana de juego

blanco = (255, 255, 255)
ancho = 650
alto = 550
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Proyecto Python - SpaceWorm")
FPS = 60
reloj = pygame.time.Clock()
# Cargar imagen de fondo


class Gusano(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.gusano = pygame.image.load("Imagenes/cabeza.png").convert()
        self.angulo = 0
        self.image = pygame.transform.rotate(self.gusano, self.angulo)
        self.rect = self.gusano.get_rect()
        self.rect.centerx = ancho/2
        self.rect.centery = alto/2
        self.corazones = True
        self.velocidad_x = 0
        self.velocidad_y = 0

    def update(self):
        # Los inputs del teclado para determinar la direccion
        # Al iniciar el movimiento, este no para, solo puede cambiar direccion
        direccion_tecla = pygame.key.get_pressed()
        if direccion_tecla[pygame.K_UP]:
            self.angulo = 0
            self.velocidad_x = 0
            self.velocidad_y = -2
        if direccion_tecla[pygame.K_DOWN]:
            self.angulo = 180
            self.velocidad_x = 0
            self.velocidad_y = 2

        if direccion_tecla[pygame.K_RIGHT]:
            self.angulo = -90
            self.velocidad_x = 2
            self.velocidad_y = 0
        if direccion_tecla[pygame.K_LEFT]:
            self.angulo = 90
            self.velocidad_x = -2
            self.velocidad_y = 0

        # Esto bloquea el moviemiento en diagonal, obligando a moverse arriba
        # o abajo.
        if direccion_tecla[pygame.K_UP] and direccion_tecla[pygame.K_RIGHT] \
           or direccion_tecla[pygame.K_UP] and direccion_tecla[pygame.K_LEFT]:
            self.angulo = 0
            self.velocidad_x = 0
            self.velocidad_y = -2
        if (direccion_tecla[pygame.K_DOWN] and direccion_tecla[pygame.K_RIGHT]
           or direccion_tecla[pygame.K_DOWN] and
           direccion_tecla[pygame.K_LEFT]):
            self.angulo = 180
            self.velocidad_x = 0
            self.velocidad_y = 2

        # velocidad del gusano actualizada
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        self.image = pygame.transform.rotate(self.gusano, self.angulo)
        # limites de movimiento con respecto a la ventana
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ancho:
            self.rect.right = ancho
        if self.rect.bottom > alto:
            self.rect.bottom = alto
        if self.rect.top < 0:
            self.rect.top = 0


class Planeta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        planeta1 = pygame.image.load("Imagenes/cabeza.png").convert()
        planeta2 = pygame.image.load("Imagenes/arriba.png").convert()
        self.planeta = random.choice([planeta1, planeta2])
        self.image = self.planeta
        self.rect = self.planeta.get_rect()
        self.rect.centerx = random.randint(0, ancho)
        self.rect.centery = 0
        self.velocidadplaneta_y = -50

    def update(self):
        self.velocidadplaneta_y += 2
        self.rect.y = self.velocidadplaneta_y


def space():

    pygame.init()
    fuente = "upheavtt.ttf"
    fuentepy = pygame.font.Font(fuente, 20)

    planetas_destruidos = -1

    fondo = pygame.image.load("Imagenes/fondojuego.png").convert()

    xfondo = 0
    yfondo = 0

    pygame.mixer.music.load("Sonidos_Musica/musicafondo.mp3")
    pygame.mixer.music.play(-1)

    sprite_jugador = pygame.sprite.GroupSingle()
    jugador = Gusano()
    sprite_jugador.add(jugador)

    sprite_planeta = pygame.sprite.GroupSingle()
    planeta = Planeta()
    sprite_planeta.add(planeta)

    while True:

        texto_puntos = fuentepy.render("Planetas destruidos:" +
                                       str(planetas_destruidos), True, blanco)

        # Para que el fondo se encuentre en movimiento
        yfondo2 = yfondo % 650
        ventana.blit(fondo, (0, yfondo2 - 650))
        if yfondo2 < ancho:
            ventana.blit(fondo, (xfondo, yfondo2))
        yfondo += 1
        reloj.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        ventana.blit(texto_puntos, (0, 530))
        sprite_jugador.update()
        sprite_planeta.update()
        sprite_jugador.draw(ventana)
        sprite_planeta.draw(ventana)
        pygame.display.update()
        if pygame.sprite.spritecollideany(jugador, sprite_planeta):
            sprite_planeta.empty()
            sprite_planeta.add(planeta)
            planeta = Planeta()
            planetas_destruidos += 1
    ventana.blit(texto_puntos, (0, 530))
    pygame.quit()


space()
