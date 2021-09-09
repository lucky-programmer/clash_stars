import pygame
from pygame.cursors import thickarrow_strings
from pygame.locals import *
import pygame.mixer
import random

screen_width = 1400
screen_height = 700
minScreenWidth = -100
maxScreenWidth = screen_width
bulletStopValue = -10000

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
explosionSound = pygame.mixer.Sound("musics/laser1.wav")
gunshotSound = pygame.mixer.Sound("musics/gunshot1.mp3")

def showExplosionEffect(screen, explosionImage, fxFrame, bulletX, bulletY):
    if fxFrame == -1:
        return fxFrame

    explosionImage.set_clip(pygame.Rect(getFxX(int(fxFrame)), getFxY(int(fxFrame))+10, 256, 123 - 10)) #Locate the sprite you want
    selectedFx1 = explosionImage.subsurface(explosionImage.get_clip()) #Extract the sprite you want

    screen.blit(selectedFx1,(bulletX, bulletY+50))
    fxFrame = fxFrame + 0.25

    if fxFrame > 12:
        fxFrame = -1

    return fxFrame

def updatePlayer1PositionWithKeyInput(pressed, playerX, playerY, bulletX, bulletY):
    if (pressed[K_a] and playerX > 0) :
        playerX = playerX - 1

    if (pressed[K_d] and playerX < 600) :
        playerX = playerX + 1

    if (pressed[K_w] and playerY > 0) :
        playerY = playerY -  1

    if (pressed[K_s] and playerY < 600) :
        playerY = playerY + 1

    if (pressed[K_LSHIFT] and bulletX == bulletStopValue) :
        bulletY = playerY - 40
        bulletX = playerX
        gunshotSound.play()

    if (pressed[K_ESCAPE]):
        exit()

    if bulletX >= 0 and bulletX != bulletStopValue:
        bulletX = bulletX + 10

    if maxScreenWidth < bulletX:
        bulletX = bulletStopValue

    return [playerX, playerY, bulletX, bulletY]

def updatePlayer2PositionWithKeyInput(pressed, playerX, playerY, bulletX, bulletY, player2HP):
    if (pressed[K_LEFT] and playerX > 630) :
        playerX = playerX - 1

    if (pressed[K_RIGHT] and playerX < 1300) :
        playerX = playerX + 1

    if (pressed[K_UP] and playerY > 0) :
        playerY = playerY - 1

    if (pressed[K_DOWN] and playerY < 600) :
        playerY = playerY + 1


    if (pressed[K_SPACE] and bulletX == bulletStopValue) :
        bulletY = playerY - 40
        bulletX = playerX
        gunshotSound.play()

    if bulletX >= minScreenWidth and bulletX != bulletStopValue:
        bulletX = bulletX - 10  

    if bulletX < minScreenWidth:
        bulletX = bulletStopValue

    return [playerX, playerY, bulletX, bulletY, player2HP]

def drawBackground(screen, backgroundImage):
    screen.blit(backgroundImage, (0,0))    

def drawPlayer(screen, playerImage, x, y):
    screen.blit(playerImage, (x, y))

def drawBullet(screen, bulletImage, x, y):
    if minScreenWidth <= x and x < maxScreenWidth and x != bulletStopValue:
        screen.blit(bulletImage, (x, y))

def checkCollision(x1,y1, x2, y2):
    if x1 == -1 or x2 == -1:
        return False

    distance = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) 
    
    if (distance < 10000):
        explosionSound.play()
        return True
    else:
        return False
    

def randomMusicSelector():
    if random.randint(0,10) < 5:
        pygame.mixer.music.load("musics/bgm1.mp3")
    else:
        pygame.mixer.music.load("musics/bme.mp3")

    pygame.mixer.music.stop()
    pygame.mixer.music.play(loops=1, start =random.randint(5,120) )

potionX = {}
potionY = {}
def drawPotionsRandomly(screen, potionImage):
    x = random.randint(0,screen_width)
    y = random.randint(0,screen_height)

    if potionImage in potionX:
        x = potionX[potionImage]
    else:
        potionX[potionImage] = x
    
    if potionImage in potionY:
        y = potionY[potionImage]
    else:
        potionY[potionImage] = y

    screen.blit(potionImage, (x, y))  

def run():
    pygame.init()


    screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE|pygame.DOUBLEBUF)
    pygame.display.set_caption("Clash Stars")

    player1Image = pygame.image.load("images/colt.png")
    player1Image = pygame.transform.scale(player1Image, (100,100))

    player2Image = pygame.image.load("images/colt.png")
    player2Image = pygame.transform.scale(player2Image, (100,100))
    player2Image = pygame.transform.flip(player2Image, True, False)

    background1 = pygame.image.load("images/background1.jpg")
    bullet1 = pygame.image.load("images/laser-bullet.png")
    bullet2 = pygame.image.load("images/laser-bullet.png")
    bullet2 = pygame.transform.flip(bullet2, True, False)
    explosionImage = pygame.image.load("images/explosion-effect.png")
    theDub = pygame.image.load("images/the_dub.png")


    redhealingpotion = pygame.image.load("images/redhealingpotion.png")
    yellowhealingpotion = pygame.image.load("images/yellowhealingpotion.webp")
    megahealingpotion = pygame.image.load("images/megahealingpotion.png")
    orangehealingpotion = pygame.image.load("images/orangehealingpotion.png")

    theDub = pygame.transform.scale(theDub, ((int)(800*0.8), (int)(268*0.8) ) )
    player1X=0
    player1Y=screen_height/2
    player2X=screen_width - 100
    player2Y=screen_height/2

    bullet1X = bulletStopValue
    bullet1Y = 50
    bullet2X = bulletStopValue
    bullet2Y = 50

    run = True
    fxFrame1 = -1
    fxFrame2 = -1

    player1HP = 5       
    player2HP = 5
    randomMusicSelector()
    
    while run:

        drawBackground(screen, background1)
        drawPotionsRandomly(screen, redhealingpotion)
        drawPotionsRandomly(screen, orangehealingpotion)
        drawPotionsRandomly(screen, megahealingpotion)
        drawPotionsRandomly(screen, yellowhealingpotion)

        pressed = pygame.key.get_pressed()

        if player1HP > 0:
            positions = updatePlayer1PositionWithKeyInput(pressed, player1X, player1Y, bullet1X, bullet1Y)
            player1X = positions[0]
            player1Y = positions[1]
            bullet1X = positions[2]
            bullet1Y = positions[3]

        if player2HP > 0:
            positions = updatePlayer2PositionWithKeyInput(pressed, player2X, player2Y, bullet2X, bullet2Y, player2HP)
            player2X = positions[0]
            player2Y = positions[1]
            bullet2X = positions[2]
            bullet2Y = positions[3]
            player2HP = positions[4]

        if areBothPlayersAlive(player1HP, player2HP)==False and pressed[K_l] :
            player1X=0
            player1Y=screen_height/2
            player2X=screen_width - 100
            player2Y=screen_height/2

            bullet1X = bulletStopValue
            bullet1Y = 50
            bullet2X = bulletStopValue
            bullet2Y = 50

            run = True
            fxFrame1 = -1
            fxFrame2 = -1

            player1HP = 5       
            player2HP =5
            
            randomMusicSelector()


        if player1HP > 0:
            drawPlayer(screen, player1Image, player1X, player1Y)

        if player2HP > 0:
            drawPlayer(screen, player2Image, player2X, player2Y)
        
        if player1HP > 0 and player2HP > 0:
            drawBullet(screen, bullet1, bullet1X, bullet1Y)
            drawBullet(screen, bullet2, bullet2X, bullet2Y)

        if areBothPlayersAlive(player1HP, player2HP) and fxFrame2 == -1 and checkCollision(player1X+50, player1Y+50, bullet2X+173, bullet2Y+112) == True:
            fxFrame2 = 0
            player1HP = player1HP - 1    
        
        if areBothPlayersAlive(player1HP, player2HP) and fxFrame1 == -1 and checkCollision(player2X+50, player2Y+50, bullet1X+173, bullet1Y+112) == True:
            fxFrame1 = 0
            player2HP = player2HP - 1

        if player1HP<=0 or player2HP<=0 :
            screen.blit(theDub, (500, 100))

        fxFrame1 = showExplosionEffect(screen, explosionImage, fxFrame1, player2X-100, player2Y)
        fxFrame2 = showExplosionEffect(screen, explosionImage, fxFrame2, player1X, player1Y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.draw.rect(screen, (0, 255, 0), (20, 20, 100*player1HP, 50) )
        pygame.draw.rect(screen, (0, 255, 0), (screen_width - (100*5+20), 20, 100*player2HP, 50) )

        pygame.display.flip()

    pygame.quit()

def areBothPlayersAlive(player1HP, player2HP):
    return player1HP > 0 and player2HP

def getFxX(frameNo):
    return (frameNo % 3) * 256
    
def getFxY(frameNo):
    return int(frameNo/3) * 123
    
run ()