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
colorfondo = (19, 22, 41)
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
        if self.rect.bottom > 530:
            self.rect.bottom = 530
        if self.rect.top < 0:
            self.rect.top = 0


class Planeta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        planeta1 = pygame.image.load("Imagenes/planeta1.png").convert()
        planeta2 = pygame.image.load("Imagenes/planeta2.png").convert()
        planeta3 = pygame.image.load("Imagenes/planeta3.png").convert()
        planeta4 = pygame.image.load("Imagenes/planeta4.png").convert()
        planeta5 = pygame.image.load("Imagenes/planeta5.png").convert()
        planeta6 = pygame.image.load("Imagenes/planeta6.png").convert()
        planeta7 = pygame.image.load("Imagenes/planeta7.png").convert()
        planeta8 = pygame.image.load("Imagenes/planeta8.png").convert()
        self.planeta = random.choice([planeta1, planeta2, planeta3, planeta4,
                                     planeta5, planeta6, planeta7, planeta8])
        self.image = self.planeta
        self.image.set_colorkey(colorfondo)
        self.rect = self.planeta.get_rect()
        self.rect.centerx = random.randint(0, 630)
        self.rect.centery = 0
        self.velocidadplaneta_y = -50

    def update(self):
        self.velocidadplaneta_y += 2
        self.rect.y = self.velocidadplaneta_y


class Borde(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.borde = pygame.image.load("Imagenes/borde2.png").convert()
        self.image = self.borde
        self.rect = self.borde.get_rect()
        self.rect.centerx = ancho/2
        self.rect.centery = 555

    def update(self):
        pass


class Asteroide1(pygame.sprite.Sprite):
    def __init__(self, velocidad):

        pygame.sprite.Sprite.__init__(self)
        self.asteroide1 = (
            pygame.image.load("Imagenes/asteroide1.png").convert_alpha()
                          )
        self.angulo = 0
        self.image = pygame.transform.rotate(self.asteroide1, self.angulo)
        self.rect = self.asteroide1.get_rect()
        self.rect.centerx = random.randint(0, 630)
        self.rect.centery = 0
        self.velocidad_asteroide1_y = -50

    def update(self, velocidad):
        self.angulo += 1
        self.velocidad_asteroide1_y += velocidad
        self.rect.y = self.velocidad_asteroide1_y
        self.image = pygame.transform.rotate(self.asteroide1, self.angulo)


class Cometa(pygame.sprite.Sprite):
    def __init__(self, velocidad):

        pygame.sprite.Sprite.__init__(self)
        self.cometa = (
            pygame.image.load("Imagenes/cometa.png").convert_alpha()
                          )
        self.image = self.cometa
        self.rect = self.cometa.get_rect()
        self.rect.centerx = ancho/2
        self.rect.centerx = random.randint(0, 630)
        self.rect.centery = 0
        self.velocidad_cometa_y = -5000

    def update(self, velocidad):
        self.velocidad_cometa_y += velocidad
        self.rect.y = self.velocidad_cometa_y


def space():

    pygame.init()
    fuente = "upheavtt.ttf"
    fuentepy = pygame.font.Font(fuente, 20)

    planetas_destruidos = 0

    fondo = pygame.image.load("Imagenes/fondojuego.png").convert()

    xfondo = 0
    yfondo = 0

    pygame.mixer.music.load("Sonidos_Musica/musicafondo.mp3")
    pygame.mixer.music.play(-1)
    destruccion_planeta = pygame.mixer.Sound("Sonidos_Musica/destruccion.mp3")
    pygame.mixer.Sound.set_volume(destruccion_planeta, 0.5)

    sprite_jugador = pygame.sprite.GroupSingle()
    jugador = Gusano()
    sprite_jugador.add(jugador)

    sprite_planeta = pygame.sprite.GroupSingle()
    planeta = Planeta()
    sprite_planeta.add(planeta)

    sprite_borde = pygame.sprite.GroupSingle()
    borde = Borde()
    sprite_borde.add(borde)

    sprite_asteroides = pygame.sprite.Group()
    velocidad_asteroide = 1.5
    asteroide1 = Asteroide1(velocidad_asteroide)
    sprite_asteroides.add(asteroide1)

    velocidad_cometa = 4.75
    sprite_cometa = pygame.sprite.GroupSingle()
    cometa = Cometa(velocidad_cometa)
    sprite_cometa.add(cometa)

    while True:

        texto_puntos = fuentepy.render("Planetas destruidos: " +
                                       str(planetas_destruidos), True, blanco)
        puntos_rect = texto_puntos.get_rect()
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
        sprite_borde.update()
        sprite_asteroides.update(velocidad_asteroide)
        sprite_cometa.update(velocidad_cometa)
        sprite_jugador.draw(ventana)
        sprite_planeta.draw(ventana)
        sprite_borde.draw(ventana)
        sprite_asteroides.draw(ventana)
        sprite_cometa.draw(ventana)
        pygame.display.update()

        if pygame.sprite.spritecollideany(jugador, sprite_planeta):
            pygame.mixer.Sound.play(destruccion_planeta)
            sprite_planeta.empty()
            sprite_planeta.add(planeta)
            planeta = Planeta()
            planetas_destruidos += 1
            velocidad_asteroide += 0.25
            velocidad_cometa += 0.25

        elif pygame.sprite.spritecollideany(borde, sprite_planeta):
            sprite_planeta.empty()
            sprite_planeta.add(planeta)
            planeta = Planeta()

        elif pygame.sprite.spritecollideany(borde, sprite_asteroides):
            sprite_asteroides.empty()
            sprite_asteroides.add(asteroide1)
            asteroide1 = Asteroide1(velocidad_asteroide)
            sprite_asteroides.update(velocidad_asteroide)

        elif pygame.sprite.spritecollideany(borde, sprite_cometa):
            sprite_cometa.empty()
            sprite_cometa.add(cometa)
            cometa = Cometa(velocidad_cometa)
            sprite_cometa.update(velocidad_cometa)

        elif pygame.sprite.spritecollideany(jugador, sprite_asteroides):
            pygame.quit()
            sys.exit()

        elif pygame.sprite.spritecollideany(jugador, sprite_cometa):
            pygame.quit()
            sys.exit()

    ventana.blit(puntos_rect, (0, 530))
    pygame.quit()


space()
