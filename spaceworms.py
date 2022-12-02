import pygame
import sys


# Variables para creacion de la ventana de juego
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
        gusano = pygame.image.load("Imagenes/gusano.png").convert()
        self.gusano = gusano
        self.angulo = 0
        self.image = pygame.transform.rotate(self.gusano, self.angulo)
        self.rect = self.gusano.get_rect(center =(12.5,74))
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

        # Esto bloquea el moviemiento en diagonal
        if direccion_tecla[pygame.K_UP] and direccion_tecla[pygame.K_RIGHT] \
           or direccion_tecla[pygame.K_UP] and direccion_tecla[pygame.K_LEFT]:
            self.velocidad_x = 0
            self.velocidad_y = -2
        if (direccion_tecla[pygame.K_DOWN] and direccion_tecla[pygame.K_RIGHT]
           or direccion_tecla[pygame.K_DOWN] and
           direccion_tecla[pygame.K_LEFT]):
            self.velocidad_x = 0
            self.velocidad_y = 2

        # velocidad del gusano actualizada
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        self.image = pygame.transform.rotate(self.gusano, self.angulo)
        # limites de movimiento con respecto a la ventana
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.right > ancho:
            self.rect.right = ancho
        if self.rect.bottom > alto:
            self.rect.bottom = alto
        if self.rect.top < 0:
            self.rect.top = 0



def space():

    pygame.init()
    fondo = pygame.image.load("Imagenes/fondojuego.png").convert()
    xfondo = 0
    yfondo = 0
    ventana.blit(fondo, (xfondo, yfondo))
    sprites = pygame.sprite.Group()
    jugador = Gusano()
    sprites.add(jugador)
    while True:
        # Para que el fondo se encuentre en movimiento
        yfondo_relativa = yfondo % fondo.get_rect().width
        ventana.blit(fondo, (xfondo, yfondo_relativa - fondo.get_rect().width))
        if yfondo_relativa < ancho:
            ventana.blit(fondo, (0, yfondo_relativa))
        yfondo += 1
        reloj.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        sprites.update()
        sprites.draw(ventana)
        pygame.display.update()

    pygame.quit()


space()
