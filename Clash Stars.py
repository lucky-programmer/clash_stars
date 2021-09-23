from time import time
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
playerSpeed = 4
bulletSpeed=14
bulletDelay=20
playerHP=20
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

def updatePlayer1PositionWithKeyInput(pressed, playerX, playerY, frame, lastGunFiredTime, multishot):
    if (pressed[K_a] and playerX > 0) :
        playerX = playerX - playerSpeed

    if (pressed[K_d] and playerX < 600) :
        playerX = playerX + playerSpeed

    if (pressed[K_w] and playerY > 0) :
        playerY = playerY -  playerSpeed

    if (pressed[K_s] and playerY < 600) :
        playerY = playerY + playerSpeed

    gunFired=0

    if (pressed[K_1]) :
        multishot=1

    if (pressed[K_LSHIFT]) :
        if multishot > 0 and (frame - lastGunFiredTime) > bulletDelay:
            gunshotSound.play()
            gunFired=1
            lastGunFiredTime = frame
        elif (frame - lastGunFiredTime) > bulletDelay*5 or lastGunFiredTime == 0:
            gunshotSound.play()
            gunFired=1
            lastGunFiredTime = frame

    if (pressed[K_ESCAPE]):
        exit()

    return [playerX, playerY, gunFired, lastGunFiredTime, multishot]

def updatePlayer2PositionWithKeyInput(pressed, playerX, playerY, frame, lastGunFiredTime, multishot):
    if (pressed[K_LEFT] and playerX > 630) :
        playerX = playerX - playerSpeed

    if (pressed[K_RIGHT] and playerX < 1300) :
        playerX = playerX + playerSpeed

    if (pressed[K_UP] and playerY > 0) :
        playerY = playerY - playerSpeed

    if (pressed[K_DOWN] and playerY < 600) :
        playerY = playerY + playerSpeed


    gunFired=0

    if (pressed[K_RSHIFT]) :
        multishot=1

    if (pressed[K_SPACE]) :
        if multishot > 0 and (frame - lastGunFiredTime) > bulletDelay:
            gunshotSound.play()
            gunFired=1
            lastGunFiredTime = frame
        elif (frame - lastGunFiredTime) > bulletDelay*5 or lastGunFiredTime == 0:
            gunshotSound.play()
            gunFired=1
            lastGunFiredTime = frame

    return [playerX, playerY, gunFired, lastGunFiredTime, multishot]

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

    
    pygame.mixer.music.play(loops=-1, start=random.randint(4,120))

def display_fps(screen, clock, font, color):
    pass
    # text_to_show = font.render(str(int(clock.get_fps())), 0, color)
    # screen.blit(text_to_show, (0,0))


def run():
    pygame.init()

    clock = pygame.time.Clock()
    # font = pygame.font.SysFont("Arial", 18)
    # color = pygame.Color("White")

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE|pygame.DOUBLEBUF)
    pygame.display.set_caption("Clash Stars")

    player1Image = pygame.image.load("images/colt.png")
    player1Image = pygame.transform.scale(player1Image, (100,100)).convert_alpha()

    player2Image = pygame.image.load("images/colt.png")
    player2Image = pygame.transform.scale(player2Image, (100,100))
    player2Image = pygame.transform.flip(player2Image, True, False).convert_alpha()

    background1 = pygame.image.load("images/background1.jpg")
    background1 = pygame.transform.scale(background1, (screen_width, screen_height) ).convert()
    bullet1 = pygame.image.load("images/laser-bullet.png").convert_alpha()
    bullet2 = pygame.image.load("images/laser-bullet.png")
    bullet2 = pygame.transform.flip(bullet2, True, False).convert_alpha()
    explosionImage = pygame.image.load("images/explosion-effect.png").convert_alpha()
    theDub = pygame.image.load("images/the_dub.png")
    theDub = pygame.transform.scale(theDub, ((int)(800*0.8), (int)(268*0.8) ) ).convert_alpha()
    player1X=0
    player1Y=screen_height/2
    player2X=screen_width - 100
    player2Y=screen_height/2

    bullet1X = [bulletStopValue] * 100
    bullet1Y = [50] * 100
    bullet2X = [bulletStopValue]*100
    bullet2Y = [50]*100

    bullet1Idx=0
    bullet2Idx=0

    run = True
    fxFrame1 = -1
    fxFrame2 = -1

    player1HP = playerHP
    player2HP = playerHP
    randomMusicSelector()
    
    frame=0
    lastGunFiredTime=0
    multishot=0
    lastGunFiredTime2=0
    multishot2=0

    while run:
        frame=frame+1
        drawBackground(screen, background1)
        pressed = pygame.key.get_pressed()

        if player1HP > 0:
            positions = updatePlayer1PositionWithKeyInput(pressed, player1X, player1Y, frame, lastGunFiredTime, multishot)
            player1X = positions[0]
            player1Y = positions[1]
            isGunFired = positions[2]
            lastGunFiredTime = positions[3]
            multishot = multishot + positions[4]
            
            if isGunFired == 1:
                bullet1X[bullet1Idx] = player1X
                bullet1Y[bullet1Idx] = player1Y - 40
                
                bullet1Idx = bullet1Idx + 1
                if bullet1Idx > 99:
                    bullet1Idx = 0
            
            for i in range(0, 100):
                if bullet1X[i] >= minScreenWidth and bullet1X[i] != bulletStopValue:
                    bullet1X[i] = bullet1X[i] + bulletSpeed

                if bullet1X[i] < minScreenWidth:
                    bullet1X[i] = bulletStopValue


        if player2HP > 0:
            positions = updatePlayer2PositionWithKeyInput(pressed, player2X, player2Y, frame, lastGunFiredTime2, multishot2)
            player2X = positions[0]
            player2Y = positions[1]
            isGunFired = positions[2]
            lastGunFiredTime2 = positions[3]
            multishot2 = multishot2 + positions[4]
            
            if isGunFired == 1:
                bullet2X[bullet2Idx] = player2X-150
                bullet2Y[bullet2Idx] = player2Y - 40
                
                bullet2Idx = bullet2Idx + 1
                if bullet2Idx > 99:
                    bullet2Idx = 0
            
            for i in range(0, 100):
                if bullet2X[i] >= minScreenWidth and bullet2X[i] != bulletStopValue:
                    bullet2X[i] = bullet2X[i] - bulletSpeed

                if bullet2X[i] < minScreenWidth:
                    bullet2X[i] = bulletStopValue

        if areBothPlayersAlive(player1HP, player2HP)==False and pressed[K_l] :
            player1X=0
            player1Y=screen_height/2
            player2X=screen_width - 100
            player2Y=screen_height/2

            bullet1X = [bulletStopValue]*100
            bullet1Y = [50]*100
            bullet2X = [bulletStopValue]*100
            bullet2Y = [50]*100

            fxFrame1 = -1
            fxFrame2 = -1

            player1HP = playerHP    
            player2HP = playerHP
            
            randomMusicSelector()


        if player1HP > 0:
            drawPlayer(screen, player1Image, player1X, player1Y)

        if player2HP > 0:
            drawPlayer(screen, player2Image, player2X, player2Y)
        
        if player1HP > 0 and player2HP > 0:

            for i in range(0, 100):
                drawBullet(screen, bullet1, bullet1X[i], bullet1Y[i])
                drawBullet(screen, bullet2, bullet2X[i], bullet2Y[i])
      
        
        for i in range(0, 100):
            if areBothPlayersAlive(player1HP, player2HP) and fxFrame2 == -1 and checkCollision(player1X+50, player1Y+50, bullet2X[i]+173, bullet2Y[i]+112) == True:
                fxFrame2 = 0
                player1HP = player1HP - 1  

            if areBothPlayersAlive(player1HP, player2HP) and fxFrame1 == -1 and checkCollision(player2X+50, player2Y+50, bullet1X[i]+173, bullet1Y[i]+112) == True:
                fxFrame1 = 0
                player2HP = player2HP - 1

        if player1HP<=0 or player2HP<=0 :
            screen.blit(theDub, (500, 100))

        fxFrame1 = showExplosionEffect(screen, explosionImage, fxFrame1, player2X-100, player2Y)
        fxFrame2 = showExplosionEffect(screen, explosionImage, fxFrame2, player1X, player1Y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.draw.rect(screen, (0, 255, 0), (20, 20, (500/playerHP)*player1HP, 50) )
        pygame.draw.rect(screen, (0, 255, 0), (screen_width - (100*5+20), 20, (500/playerHP)*player2HP, 50) )

        #display_fps(screen, clock, font, color)

        clock.tick(60)
        pygame.display.update()
        #pygame.display.flip()
        #pygame.display.update()

    pygame.quit()

def areBothPlayersAlive(player1HP, player2HP):
    return player1HP > 0 and player2HP

def getFxX(frameNo):
    return (frameNo % 3) * 256
    
def getFxY(frameNo):
    return int(frameNo/3) * 123
    
run ()