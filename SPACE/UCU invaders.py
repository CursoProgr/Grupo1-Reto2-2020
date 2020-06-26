#RETO 2 - SPACE INVADERS
#23 DE JUNIO DE 2020
#CREADO POR FACUNDO BALBUENA, FEDERICO ROCCA Y LORENZO BONINO
#https://pythonmania.wordpress.com/2010/04/07/tutorial-pygame-3-un-videojuego/

#IMPORTAMOS LIBRERIAS Y COSAS NECESARIAS COMO POR EJEMPLO PYGAME MIXER
import pygame
from pygame.locals import *
import os
import sys
import playsound
import random
pygame.init()
dispj = pygame.mixer.Sound("disparojugador.ogg")
dispe = pygame.mixer.Sound("disparoenemigo1.ogg")
wins = pygame.mixer.Sound("CRACK.ogg")
gots = pygame.mixer.Sound("BURRO.ogg")
kaboom = pygame.mixer.Sound("kaboom.wav")
fotos = ["joel.jpg","maria.jpg"]
clock = pygame.time.Clock()

#----------------------------------------------------
#           VENTANA Y DIRECCION DE IMAGENES
#----------------------------------------------------

SCREEN_WIDTH = 840
SCREEN_HEIGHT = 680
IMG_DIR = "imagenes"

#----------------------------------------------------
#      FUNCION PARA CARGAR IMAGENES Y RETRASO
#----------------------------------------------------
        
def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print ("Error, no se puede cargar la imagen: ", ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

def retraso(fb):
    i=0
    while 0<=i<=fb:
        print("retraso")
        i=i+1
        if i==fb:
            break
#----------------------------------------------------
#           CLASES PARA OBJETOS
#----------------------------------------------------

class jugador(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("shooter.jpg", IMG_DIR, alpha=False)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT - 75
        self.speed = [0,13]
        
    #CONTROLAMOS QUE EL JUGADOR NO SALGA DE LA PANTALLA
    def control(self):
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0
            
class bala(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("brad pitt.jpg",IMG_DIR,alpha=False)
        self.rect = self.image.get_rect()
        self.rect.centerx = 10000
        self.rect.centery = 10000
        self.speed = [0,0]

    #ARGUMENTO MOTOR DE LA BALA 
    def salida(self):
        self.rect.move_ip((self.speed[0], self.speed[1]))

    #ARGUMENTO PARA QUE LA BALA MATE AL ENEMIGO  
    def colision(self,tirador,objetivo):
        if self.rect.colliderect(objetivo.rect): # con eso mira si choco con el objetivo
            self.__init__()
            kaboom.play()
            objetivo.rect.centery = 100000
            objetivo.speed = [0,0]
                    
        if self.rect.centery <= 0:
            self.__init__()
            
    #ARGUMENTO PARA QUE LA BALA MATE AL JUGADOR
    def muerte(self,objetivo):
        if self.rect.colliderect(objetivo.rect): # con eso mira si choco con el objetivo
            objetivo.image = load_image("explosion.png", IMG_DIR, alpha=True)
            kaboom.play()
            objetivo.speed = [0,0]
        if self.rect.centery <= 0:
            self.__init__()
            
class villanos(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        f=random.choice(fotos)
        self.image = load_image(f,IMG_DIR,alpha=False)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = [2,0]
        
    #ARGUMENTO MOTOR DEL VILLANO   
    def mov(self):
        if self.rect.left < 0:
            self.speed = [0,0]
            self.rect.centerx = 20
            self.rect.centery = self.rect.centery + 50
            self.speed = [2,0]
                   
        elif self.rect.right > SCREEN_WIDTH:
            self.speed = [0,0]
            self.rect.centerx = SCREEN_WIDTH - 20
            self.rect.centery = self.rect.centery + 50
            self.speed = [-2,0]    
        self.rect.move_ip((self.speed[0], self.speed[1]))
        
    #ARGUMENTO PARA QUE LA BALA MATE AL VILLANO  
    def muerte(self,objetivo):
        if self.rect.colliderect(objetivo.rect): # con eso mira si choco con el objetivo
            objetivo.image = load_image("explosion.png", IMG_DIR, alpha=True)
            kaboom.play()
            objetivo.speed = [0,0]
        if self.rect.centery <= 0:
            self.__init__()
                  
#----------------------------------------------------
#           FUNCION PRINCIPAL DEL JUEGO
#----------------------------------------------------

def space():
    #INICIAMOS PYGAME
    pygame.init()
    
    #SE CREA LA VENTANA
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     #dimensionamos la ventana
    pygame.display.set_caption("SPACE INVADERS")                        #titulamos la ventana
    
    #CREAMOS OBJETOS Y VECTORES
    fondo = load_image("fondo.jpg",IMG_DIR,alpha=False)                 #cargamos fondo de espacio
    player = jugador()                                                  
    joel = villanos(84,50)
    joel1 = villanos(168,50)
    joel2 = villanos(256,50)
    joel3 = villanos(336,50)
    joel4 = villanos(420,50)
    joel5 = villanos(42,150)
    joel6 = villanos(126,150)
    joel7 = villanos(210,150)
    joel8 = villanos(294,150)
    joel9 = villanos(378,150)
    tiro = bala()
    tiro1 = bala()
    tiro2 = bala()
    tiroe = bala()
    reloj = pygame.time.Clock()                                         
    pygame.key.set_repeat(200,15)                                       #le damos la velocidad cuando dejamos apretada una tecla
    enemigos = [joel,joel1,joel2,joel3,joel4,joel5,joel6,joel7,joel8,joel9]
    
    #CREAMOS TEXTOS GAME OVER Y WIN, ADEMAS DE TOPEAR LOS CONTADORES
    go = pygame.font.SysFont("Consolas",80)
    got = go.render("GAME OVER",0,(200,60,80))
    win = pygame.font.SysFont("Consolas",80)
    ganaste = win.render("GANASTE CRACK",0,(60,200,80))
    lb=0
    contador=100
    balas = 0
    while True:
        reloj.tick(60)                                                  #topeamos a 60 cuadros por milisegundo
        
        #DAMOS ATRIBUTOS A LOS OBJETOS
        player.control()
        joel.mov()
        joel.muerte(player)
        joel1.mov()
        joel1.muerte(player)
        joel2.mov()
        joel2.muerte(player)
        joel3.mov()
        joel3.muerte(player)
        joel4.mov()
        joel4.muerte(player)
        joel5.mov()
        joel5.muerte(player)
        joel6.mov()
        joel6.muerte(player)
        joel7.mov()
        joel7.muerte(player)
        joel8.mov()
        joel8.muerte(player)
        joel9.mov()
        joel9.muerte(player)
        tiro.colision(player,joel)
        tiro.colision(player,joel1)
        tiro.colision(player,joel2)
        tiro.colision(player,joel3)
        tiro.colision(player,joel4)
        tiro.colision(player,joel5)
        tiro.colision(player,joel6)
        tiro.colision(player,joel7)
        tiro.colision(player,joel8)
        tiro.colision(player,joel9)
        tiro.salida()
        tiro1.colision(player,joel)
        tiro1.colision(player,joel1)
        tiro1.colision(player,joel2)
        tiro1.colision(player,joel3)
        tiro1.colision(player,joel4)
        tiro1.colision(player,joel5)
        tiro1.colision(player,joel6)
        tiro1.colision(player,joel7)
        tiro1.colision(player,joel8)
        tiro1.colision(player,joel9)
        tiro1.salida()
        tiro2.colision(player,joel)
        tiro2.colision(player,joel1)
        tiro2.colision(player,joel2)
        tiro2.colision(player,joel3)
        tiro2.colision(player,joel4)
        tiro2.colision(player,joel5)
        tiro2.colision(player,joel6)
        tiro2.colision(player,joel7)
        tiro2.colision(player,joel8)
        tiro2.colision(player,joel9)
        tiro2.salida()
        tiroe.colision(joel,player)
        tiroe.colision(joel1,player)
        tiroe.colision(joel2,player)
        tiroe.colision(joel3,player)
        tiroe.colision(joel4,player)
        tiroe.colision(joel5,player)
        tiroe.colision(joel6,player)
        tiroe.colision(joel7,player)
        tiroe.colision(joel8,player)
        tiroe.colision(joel9,player)
        tiroe.salida()
        tiroe.muerte(player)
        
        #CONFIGURAMOS MOVIMIENTO POR TECLADO 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                #APRETAR FLECHA IZQ MUEVE A LA IZQ
                if event.key == K_LEFT:
                    player.rect.centerx -= 5
                #APRETAR FLECHA DER MUEVE A LA DER
                elif event.key == K_RIGHT:
                    player.rect.centerx += 5
                #APRETAR ESCAPE CIERRA EL JUEGO
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                #APRETAR BARRA ESPACIO DISPARA
                elif event.key == K_SPACE:
                    balas = balas + 1
                    reloj.tick(60)
                    #USAMOS CONTADOR "BALAS" PARA PODER DISPARAR HASTA 3 BALAS
                    if balas == 1:
                        tiro.rect.centery = player.rect.centery
                        tiro.rect.centerx = player.rect.centerx
                        tiro.speed = [0,-10]
                        dispj.play()
                    elif balas == 2:
                        tiro1.rect.centery = player.rect.centery
                        tiro1.rect.centerx = player.rect.centerx
                        tiro1.speed = [0,-10]
                        dispj.play()
                    elif balas == 3:
                        tiro2.rect.centery = player.rect.centery
                        tiro2.rect.centerx = player.rect.centerx
                        tiro2.speed = [0,-10]
                        dispj.play()
                        balas = 0
            elif event.type == pygame.KEYUP:
                #SOLATAR FLECHA IZQ DEJA DE MOVERSE
                if event.key == K_LEFT:
                    player.rect.centerx += 0
                #SOLTAR FLECHA DER DEJA DE MOVERSE
                elif event.key == K_RIGHT:
                    player.rect.centerx += 0
                    
        #CUANDO TODOS LOS ENEMIGOS ESTAN EN LA MISMA POSICION EN Y SE GANA LA PARTIDA, APARECE MENSAJE Y MUSICA DE VICTORIA
        if joel.rect.centery == joel1.rect.centery == joel2.rect.centery == joel3.rect.centery == joel4.rect.centery == joel5.rect.centery == joel6.rect.centery == joel7.rect.centery == joel8.rect.centery == joel9.rect.centery:
            screen.blit(fondo,(0,0))
            screen.blit(ganaste,(SCREEN_WIDTH/2-275,SCREEN_HEIGHT/2-50))
            wins.play()
            pygame.display.flip()
            retraso(1500)
            pygame.quit()
            sys.exit()
            break
        
        #CUANDO EL JUGADOR ES GOLPEADO CAMBIA SU IMAGEN A LA EXPLOSION Y DESAPARECE
        if player.speed == [0,0]:
            screen.blit(player.image,player.rect)
            pygame.display.flip()
            retraso(75)
            lb = lb + 1
            player.rect.centery = 10000
        #UNA VEZ QUE DESAPARECIO APARECE GAME OVER Y MUSICA FINAL
        if lb==1:
            player.rect.centery == 10000
            screen.blit(fondo,(0,0))
            screen.blit(got,(SCREEN_WIDTH/2-200,SCREEN_HEIGHT/2-50))
            gots.play()
            pygame.display.flip()
            retraso(1150)
            pygame.quit()
            sys.exit()
            break
        
        #CADA VEZ QUE "CONTADOR" LLEGUE A CERO UN ENEMIGO RANDOM DISPARA
        while contador == 0:
            m = random.choice(enemigos)
            if m.speed != [0,0]:
                tiroe.rect.centery = m.rect.centery
                tiroe.rect.centerx = m.rect.centerx
                dispe.play()
                tiroe.speed = [0,15]
                contador = 100
                break
            #SI EL ENEMIGO RANDOM ELEGIDO YA ESTA MUERTO(SPEED=0), VUELVE A ELEGIR OTRO HASTA QUE ELIJA UNO VIVO
            else:
                enemigos.remove(m)
        #ACTUALIZAMOS PANTALLAS            
        screen.blit(fondo, (0, 0))
        screen.blit(tiro.image, tiro.rect)
        screen.blit(tiro1.image, tiro1.rect)
        screen.blit(tiro2.image, tiro2.rect)
        screen.blit(player.image, player.rect)
        screen.blit(joel.image, joel.rect)
        screen.blit(joel1.image, joel1.rect)
        screen.blit(joel2.image, joel2.rect)
        screen.blit(joel3.image, joel3.rect)
        screen.blit(joel4.image, joel4.rect)
        screen.blit(joel5.image, joel5.rect)
        screen.blit(joel6.image, joel6.rect)
        screen.blit(joel7.image, joel7.rect)
        screen.blit(joel8.image, joel8.rect)
        screen.blit(joel9.image, joel9.rect)
        screen.blit(tiroe.image, tiroe.rect)
        pygame.display.flip()
        #COLOCAMOS UN CONTADOR PARA REGULAR EL TIEMPO QUE DISPARAN LOS ENEMIGOS
        contador = contador-1
        
#LLAMAMOS AL JUEGO
space()




