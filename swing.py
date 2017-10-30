from itertools import cycle
import random
import sys
import math

import pygame
from pygame.locals import *


FPS = 30
SCREENWIDTH  = 432
SCREENHEIGHT = 700
# amount by which base can maximum shift to left
BARGAPSIZE  = 100 # gap between left and right part of bar
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # green bear
    (
        'assets/img/bear_0_0_0.png',
        'assets/img/bear_0_0_1.png',
        'assets/img/bear_0_0_2.png',
        'assets/img/bear_0_1_0.png',
        'assets/img/bear_0_1_1.png',
        'assets/img/bear_0_1_2.png',
    ),
    # white bear
    (
        'assets/img/bear_1_0_0.png',
        'assets/img/bear_1_0_1.png',
        'assets/img/bear_1_0_2.png',
        'assets/img/bear_1_1_0.png',
        'assets/img/bear_1_1_1.png',
        'assets/img/bear_1_1_2.png',
    ),
    # red bear
    (
        'assets/img/bear_2_0_0.png',
        'assets/img/bear_2_0_1.png',
        'assets/img/bear_2_0_2.png',
        'assets/img/bear_2_1_0.png',
        'assets/img/bear_2_1_1.png',
        'assets/img/bear_2_1_2.png',
    ),
    # pink bear
    (
        'assets/img/bear_3_0_0.png',
        'assets/img/bear_3_0_1.png',
        'assets/img/bear_3_0_2.png',
        'assets/img/bear_3_1_0.png',
        'assets/img/bear_3_1_1.png',
        'assets/img/bear_3_1_2.png',
    ),
    # yellow bear
    (
        'assets/img/bear_4_0_0.png',
        'assets/img/bear_4_0_1.png',
        'assets/img/bear_4_0_2.png',
        'assets/img/bear_4_1_0.png',
        'assets/img/bear_4_1_1.png',
        'assets/img/bear_4_1_2.png',
    ),
    # brown bear
    (
        'assets/img/bear_5_0_0.png',
        'assets/img/bear_5_0_1.png',
        'assets/img/bear_5_0_2.png',
        'assets/img/bear_5_1_0.png',
        'assets/img/bear_5_1_1.png',
        'assets/img/bear_5_1_2.png',
    ),
    # astro bear
    (
        'assets/img/bear_6_0_0.png',
        'assets/img/bear_6_0_1.png',
        'assets/img/bear_6_0_2.png',
        'assets/img/bear_6_1_0.png',
        'assets/img/bear_6_1_1.png',
        'assets/img/bear_6_1_2.png',
    ),
    # ninja bear
    (
        'assets/img/bear_7_0_0.png',
        'assets/img/bear_7_0_1.png',
        'assets/img/bear_7_0_2.png',
        'assets/img/bear_7_1_0.png',
        'assets/img/bear_7_1_1.png',
        'assets/img/bear_7_1_2.png',
    ),
)

WHEELS_LIST = (
    'assets/img/wheels_0.png',
    'assets/img/wheels_1.png',
    'assets/img/wheels_2.png',
    'assets/img/wheels_3.png',
    'assets/img/wheels_4.png',
    'assets/img/wheels_4.png',
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/img/bg_0.png',
    'assets/img/bg_1.png',
    'assets/img/bg_2.png',
)

CLOUDS_LIST = (
    'assets/img/cloud_0.png',
    'assets/img/cloud_1.png',
    'assets/img/cloud_2.png',
)

# list of pipes
HAMMER = (
    'assets/img/hammer.png',
)
BAR = (
    'assets/img/crane.png',
)
PLAY = (
    'assets/img/button_start.png',
)
try:
    xrange
except NameError:
    xrange = range


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Swing Copters')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/img/0.png').convert_alpha(),
        pygame.image.load('assets/img/1.png').convert_alpha(),
        pygame.image.load('assets/img/2.png').convert_alpha(),
        pygame.image.load('assets/img/3.png').convert_alpha(),
        pygame.image.load('assets/img/4.png').convert_alpha(),
        pygame.image.load('assets/img/5.png').convert_alpha(),
        pygame.image.load('assets/img/6.png').convert_alpha(),
        pygame.image.load('assets/img/7.png').convert_alpha(),
        pygame.image.load('assets/img/8.png').convert_alpha(),
        pygame.image.load('assets/img/9.png').convert_alpha()
    )

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/img/text_gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['messages'] = (
        pygame.image.load('assets/img/title_00.png').convert_alpha(),
        pygame.image.load('assets/img/title_01.png').convert_alpha(),
        pygame.image.load('assets/img/title_02.png').convert_alpha(),
        pygame.image.load('assets/img/title_03.png').convert_alpha(),
    )

    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/img/land.png').convert_alpha()
    IMAGES['tree'] = pygame.image.load('assets/img/tree.png').convert_alpha()

    # # sounds
    # if 'win' in sys.platform:
    #     soundExt = '.wav'
    # else:
    #     soundExt = '.ogg'

    # SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    # SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    # SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    # SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    # SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()
        IMAGES['cloud'] = pygame.image.load(CLOUDS_LIST[randBg]).convert_alpha()
        IMAGES['play'] = pygame.image.load(PLAY[0]).convert_alpha()

        # select random player sprites
        randPlayerl = random.randint(0, len(PLAYERS_LIST) - 4)
        randPlayerr = random.randint(len(PLAYERS_LIST) - 3, len(PLAYERS_LIST) - 1)
        IMAGES['playerl'] = (
            pygame.image.load(PLAYERS_LIST[randPlayerl][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayerl][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayerl][2]).convert_alpha(),
        )
        IMAGES['playerr'] = (
            pygame.image.load(PLAYERS_LIST[randPlayerr][3]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayerr][4]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayerr][5]).convert_alpha(),
        )

        # select random pipe sprites
        barindex = 0
        IMAGES['bar'] = pygame.image.load(BAR[0]).convert_alpha()
        IMAGES['hammer'] = pygame.image.load(HAMMER[0]).convert_alpha()

        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)

def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    # index of player to blit on screen
    msgIndex = 0
    msgIndexGen = cycle([0, 1, 2, 3])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0
    swingIter = 0

    messagex = int((SCREENWIDTH - IMAGES['messages'][0].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.22)

    hammers, bars = [], []
    hammer, bar = getRandomBar(100)
    hammers.append(hammer)
    bars.append(bar)

    baseHeight = IMAGES['base'].get_height()
    basex = 0

    # player shm for up-down motion on welcome screen
    messageShmVals = {'val': 0, 'dir': 1}

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                # make first flap sound and return values for mainGame
                # SOUNDS['wing'].play()
                return {
                    'hammers': hammers,
                    'bars': bars,
                }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 3 == 0:
            msgIndex = next(msgIndexGen)
        swingIter = (swingIter + 1) % 60
        loopIter = (loopIter + 1) % 30
        nextShm(messageShmVals)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['cloud'], (30,150))
        SCREEN.blit(IMAGES['tree'], (basex, BASEY - baseHeight * 0.4))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        SCREEN.blit(IMAGES['bar'], (bars[0][0]['x'], bars[0][0]['y']))
        SCREEN.blit(IMAGES['bar'], (bars[0][1]['x'], bars[0][1]['y']))
        rotated_img, x, y = rot_img(IMAGES['hammer'], theta(swingIter, hammers[0][0]['t']), hammers[0][0]['x'], hammers[0][0]['y'])
        SCREEN.blit(rotated_img, (x, y))
        rotated_img, x, y = rot_img(IMAGES['hammer'], theta(swingIter, hammers[0][1]['t']), hammers[0][1]['x'], hammers[0][1]['y'])
        SCREEN.blit(rotated_img, (x, y))
        SCREEN.blit(IMAGES['messages'][msgIndex], (messagex, messagey + messageShmVals['val']))
        SCREEN.blit(IMAGES['play'], (int((SCREENWIDTH - IMAGES['play'].get_width()) / 2), SCREENHEIGHT * 0.6))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def theta(t, offset):
    return 30*math.sin(3.14159*(t-30)/30 + offset*3.14159/180)

def rot_img(image, angle, x, y):
    rect = image.get_rect()
    # print rect.center
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    # print rect.center
    h = image.get_height()*math.sin(angle*3.14159/180)
    w = image.get_width()*math.sin(angle*3.14159/180)/4
    if angle < 0:
        return rot_image, x + h - w, y + w*2
    else:
        return rot_image, x + w, y - w*2

def mainGame(movementInfo):
    score = playerIndex = swingIter = 0
    # playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.5), int(SCREENHEIGHT * 0.6)

    hammer, bar = getRandomBar(-250)
    hammers, bars = movementInfo['hammers'], movementInfo['bars']
    hammers.append(hammer)
    bars.append(bar)

    craneVelY = 4
    playerVelX = 0
    # player velocity, max velocity, downward accleration, accleration on flap
    playerVelY = 1   # player's velocity along Y, default same as playerFlapped
    # playerMaxVelY = 10   # max vel along Y, max descend speed
    # playerMinVelY = -8   # min vel along Y, max ascend speed
    playerAccX = 1   # players right accleration
    # playerFlapAcc = -9   # players speed on flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                # if playery > -2 * IMAGES['player'][0].get_height():
                # playerVelY = playerFlapAcc
                playerAccX = -playerAccX
                # SOUNDS['wing'].play()


        if playerx + IMAGES['playerl'][0].get_width()/2 < 0 or playerx + IMAGES['playerl'][0].get_width()/2 > SCREENWIDTH:
            return {
                'x': playerx,
                'y': playery,
                'hammers': hammers,
                'bars': bars,
                'score': score,
                'swingIter': swingIter,
            }


        if bars[0][0]['y'] - 1 < playery + IMAGES['playerl'][0].get_height()/2 < bars[0][0]['y'] + 3:
            score += 1

        # player's movement
        playerVelX += playerAccX
        playerx += playerVelX

        # move pipes to left
        for hammer in hammers:
            hammer[0]['y'] += craneVelY
            hammer[1]['y'] += craneVelY

        for bar in bars:
            bar[0]['y'] += craneVelY
            bar[1]['y'] += craneVelY

        swingIter = (swingIter + 1) % 60

        if bars[0][0]['y'] > SCREENHEIGHT:
            bars = bars[1:]
            hammers = hammers[1:]

        if 97 < bars[-1][0]['y'] < 101:
            hammer, bar = getRandomBar(-250)
            hammers.append(hammer)
            bars.append(bar)

        SCREEN.blit(IMAGES['background'], (0,0))

        for i, bar in enumerate(bars):
            SCREEN.blit(IMAGES['bar'], (bar[0]['x'], bar[0]['y']))
            if i == 0:
                if pygame.sprite.collide_mask(MakeSprite(IMAGES['bar'], bar[0]['x'], bar[0]['y']), MakeSprite(IMAGES['playerl'][0], playerx, playery)):
                    return {
                        'x': playerx,
                        'y': playery,
                        'hammers': hammers,
                        'bars': bars,
                        'score': score,
                        'swingIter': swingIter,
                    }
            SCREEN.blit(IMAGES['bar'], (bar[1]['x'], bar[1]['y']))
            if i == 0:
                if pygame.sprite.collide_mask(MakeSprite(IMAGES['bar'], bar[1]['x'], bar[1]['y']), MakeSprite(IMAGES['playerl'][0], playerx, playery)):
                    return {
                        'x': playerx,
                        'y': playery,
                        'hammers': hammers,
                        'bars': bars,
                        'score': score,
                        'swingIter': swingIter,
                    }

        for i, hammer in enumerate(hammers):
            rotated_img, x, y = rot_img(IMAGES['hammer'], theta(swingIter, hammer[0]['t']), hammer[0]['x'], hammer[0]['y'])
            SCREEN.blit(rotated_img, (x, y))
            if i == 0:
                if pygame.sprite.collide_mask(MakeSprite(rotated_img, x, y), MakeSprite(IMAGES['playerl'][0], playerx, playery)):
                    return {
                        'x': playerx,
                        'y': playery,
                        'hammers': hammers,
                        'bars': bars,
                        'score': score,
                        'swingIter': swingIter,
                    }
            rotated_img, x, y = rot_img(IMAGES['hammer'], theta(swingIter, hammer[1]['t']), hammer[1]['x'], hammer[1]['y'])
            SCREEN.blit(rotated_img, (x, y))
            if i == 0:
                if pygame.sprite.collide_mask(MakeSprite(rotated_img, x, y), MakeSprite(IMAGES['playerl'][0], playerx, playery)):
                    return {
                        'x': playerx,
                        'y': playery,
                        'hammers': hammers,
                        'bars': bars,
                        'score': score,
                        'swingIter': swingIter,
                    }

        # print score so player overlaps the score
        
        showScore(score)
        SCREEN.blit(IMAGES['playerl'][0], (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

class MakeSprite(pygame.sprite.Sprite):

    def __init__(self, inp_image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = inp_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def showGameOverScreen(crashInfo):
    """crashes the player down and shows gameover image"""
    score = crashInfo['score']
    playerx = crashInfo['x']
    playery = crashInfo['y']
    swingIter = crashInfo['swingIter']
    hammers, bars = crashInfo['hammers'], crashInfo['bars']

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
        
        swingIter = (swingIter + 1) % 60
        
        SCREEN.blit(IMAGES['background'], (0,0))

        for bar in bars:
            SCREEN.blit(IMAGES['bar'], (bar[0]['x'], bar[0]['y']))
            SCREEN.blit(IMAGES['bar'], (bar[1]['x'], bar[1]['y']))

        for hammer in hammers:
            rotated_img, x, y = rot_img(IMAGES['hammer'], theta(swingIter, hammer[0]['t']), hammer[0]['x'], hammer[0]['y'])
            SCREEN.blit(rotated_img, (x, y))
            rotated_img, x, y = rot_img(IMAGES['hammer'], theta(swingIter, hammer[1]['t']), hammer[1]['x'], hammer[1]['y'])
            SCREEN.blit(rotated_img, (x, y))

        showScore(score)
        SCREEN.blit(IMAGES['playerl'][0], (playerx, playery))

        SCREEN.blit(IMAGES['gameover'], ((SCREENWIDTH - IMAGES['gameover'].get_width())/2, (SCREENHEIGHT - IMAGES['gameover'].get_height())/2))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def nextShm(ShmVals):
    """oscillates the value of messageShm['val'] between 8 and -8"""
    if abs(ShmVals['val']) == 8:
        ShmVals['dir'] *= -1

    if ShmVals['dir'] == 1:
         ShmVals['val'] += 1
    else:
        ShmVals['val'] -= 1

def getRandomBar(y):
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    x = random.randrange(SCREENWIDTH/10, SCREENWIDTH*2/5)
    gapX = SCREENWIDTH * 0.4
    barWidth = IMAGES['bar'].get_width()
    offset = random.randint(-180, 180)
    # t = 30*cos(2*3.14159*random.uniform(0, 30)/180)

    return [
        {'x': x - 60, 'y': y + 10, 't': offset},
        {'x': x + gapX - 10, 'y': y + 10, 't': offset}
    ],[
        {'x': x - barWidth, 'y': y},
        {'x': x + gapX, 'y': y}
    ]

def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


if __name__ == '__main__':
    main()
