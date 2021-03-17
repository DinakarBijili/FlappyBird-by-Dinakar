import random #For generating random numbers
import sys # sys.exit to exit the program
import pygame
from pygame.locals import * #Basic pygame imports

#Globle Variables from game 
#Frames per Seconds (images rendering)
FPS = 32
SCREENWIDTH =289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH ,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_AUDIO = {}
PLAYER = 'Gallery/Sprites/bird.png'
BACKGROUND = 'Gallery/Sprites/background.png'
PIPE = 'Gallery/Sprites/pipe.png'

def welcomeScreen():
    """Shows Welcome Images in Screen"""
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #if user clicks on cross button, quit
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #If the user Pressed Space or up key, Start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery ))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey ))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY ))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0 
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    #Create 2 pipes for blitting(set) on the Screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #List of Upper Pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    #List of Lower Pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    #Velocity of x pipe 
    pipeVelx = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1


    playerFlapAccv = -8 #velocity (speed of the bird while flapping)
    playerFlapped = False #it is True only when the bird is flapping 

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0 :
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_AUDIO['wing'].play()

        crashTest = isCollide(playerx, playery ,upperPipes ,lowerPipes) #this function will return true if player crash
        if crashTest:
            return


        #Check for Score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipMidPos<=playerMidPos<pipMidPos +4:
                score += 1
                print("Your Score is ",score)
                GAME_AUDIO['point'].play()

        if playerMinVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)


        #Move pipes to Left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx

        #ADD a new pipe when the first pipe is about to go to the left
        if 0 < upperPipes[0]['x']<5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])


        #if the pipes is out of the screen, remove it 
        if upperPipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets Blit the Sprits
        SCREEN.blit(GAME_SPRITES['background'],(0, 0))
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'], lowerPipe['y']))
            
        SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery ,upperPipes ,lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_AUDIO['hit'].play()
        return True


    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x'])< GAME_SPRITES['pipe'][0].get_width()):
            GAME_AUDIO['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_AUDIO['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generating position of two pipes(one Bottom Stright and one Top rotated) for bitting on the Screec
    """
    pipHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipX =SCREENWIDTH + 10
    y1 = pipHeight - y2 + offset
    pipe = [
        {'x':pipX , 'y':-y1}, #upper pipe
        {'x':pipX , 'y': y2} #lower pipe
    ]
    return pipe

if __name__ == "__main__":
    #Game Start
    pygame.init() #Initialize all pygame modules
    FPSCLOCK = pygame.time.Clock() # Control FPS
    pygame.display.set_caption('Flappy Bird by Dinakar')#HEading
    GAME_SPRITES['numbers'] = (
        pygame.image.load('Gallery/Sprites/0.png').convert_alpha(), #Convert images faster
        pygame.image.load('Gallery/Sprites/1.png').convert_alpha(), #Convert images faster
        pygame.image.load('Gallery/Sprites/2.png').convert_alpha(), #Convert images faster
        pygame.image.load('Gallery/Sprites/3.png').convert_alpha(),#Convert images faster
        pygame.image.load('Gallery/Sprites/4.png').convert_alpha(),#Convert images faster
        pygame.image.load('Gallery/Sprites/5.png').convert_alpha(),#Convert images faster
        pygame.image.load('Gallery/Sprites/6.png').convert_alpha(),#Convert images faster
        pygame.image.load('Gallery/Sprites/7.png').convert_alpha(),#Convert images faster
        pygame.image.load('Gallery/Sprites/8.png').convert_alpha(),#Convert images faster
        pygame.image.load('Gallery/Sprites/9.png').convert_alpha(),#Convert images faster
    )

    GAME_SPRITES['message'] = pygame.image.load('Gallery/Sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('Gallery/Sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )

    #GAME SOUNDS
    GAME_AUDIO['die'] = pygame.mixer.Sound('Gallery/audio/die.wav')
    GAME_AUDIO['hit'] = pygame.mixer.Sound('Gallery/audio/hit.wav')
    GAME_AUDIO['point'] = pygame.mixer.Sound('Gallery/audio/point.wav')
    GAME_AUDIO['swoosh'] = pygame.mixer.Sound('Gallery/audio/swoosh.wav')
    GAME_AUDIO['wing'] = pygame.mixer.Sound('Gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() #Shows Welcome screen to the user until he presses a button
        mainGame() #This is the main game function
    