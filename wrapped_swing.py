import pygame
from pygame.locals import *
import os
import sys
import random
import pygame.surfarray as surfarray
from itertools import cycle
import math

FPS = 30
SCREENWIDTH  = 432
SCREENHEIGHT = 700
# amount by which base can maximum shift to left
BARGAPSIZE  = 100 # gap between left and right part of self.bar
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
global SCREEN, FPSCLOCK
pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Swing Copters')

# numbers sprites for self.score display
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
# self.barindex = 0
IMAGES['bar'] = pygame.image.load(BAR[0]).convert_alpha()
IMAGES['hammer'] = pygame.image.load(HAMMER[0]).convert_alpha()

PLAYERWIDTH = IMAGES['playerl'][0].get_width()
PLAYERHEIGHT = IMAGES['playerl'][0].get_height()

class GameState:
    def __init__(self):
        self.score = self.playerIndex = self.swingIter = 0
        # self.playerIndexGen = movementInfo['self.playerIndexGen']
        self.playerx, self.playery = int(SCREENWIDTH * 0.5), int(SCREENHEIGHT * 0.7)

        self.hammers, self.bars = [],[]
        self.hammer, self.bar = getRandomBar(100)
        self.hammers.append(self.hammer)
        self.bars.append(self.bar)
        self.hammer, self.bar = getRandomBar(-200)
        self.hammers.append(self.hammer)
        self.bars.append(self.bar)

        self.craneVelY = 4
        self.playerVelX = 0
        # playerMaxVelY = 10    # max vel along Y, max descend speed
        # playerMinVelY = -8    # min vel along Y, max ascend speed
        self.playerAccX = 0.4          # players right accleration

    def frame_step(self, input_actions):
        pygame.event.pump()

        reward = 0
        terminal = False

        isCrash = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        if input_actions[1] == 1:
            self.playerAccX = -self.playerAccX
        else:
            pass

        if self.bars[0][0]['y'] - 1 < self.playery + IMAGES['playerl'][0].get_height()/2 < self.bars[0][0]['y'] + 3:
            self.score += 1
            reward = math.exp(-5*abs(self.bars[1][1]['x'] - SCREENWIDTH * 0.2 - self.playerx - PLAYERWIDTH/2)/\
                (SCREENWIDTH*1.2 - self.bars[1][1]['x'] - PLAYERWIDTH/2))
        else:
            reward = math.exp(-5*abs(self.bars[0][1]['x'] - SCREENWIDTH * 0.2 - self.playerx - PLAYERWIDTH/2)/\
                (SCREENWIDTH*1.2 - self.bars[0][1]['x'] - PLAYERWIDTH/2))

        # player's movement
        self.playerVelX += self.playerAccX
        self.playerx += self.playerVelX

        # move pipes to left
        for self.hammer in self.hammers:
            self.hammer[0]['y'] += self.craneVelY
            self.hammer[1]['y'] += self.craneVelY

        for self.bar in self.bars:
            self.bar[0]['y'] += self.craneVelY
            self.bar[1]['y'] += self.craneVelY

        self.swingIter = (self.swingIter + 1) % 60

        if self.bars[0][0]['y'] > SCREENHEIGHT:
            self.bars = self.bars[1:]
            self.hammers = self.hammers[1:]

        if 97 < self.bars[-1][0]['y'] < 101:
            self.hammer, self.bar = getRandomBar(-200)
            self.hammers.append(self.hammer)
            self.bars.append(self.bar)

        SCREEN.blit(IMAGES['background'], (0,0))

        for i, self.bar in enumerate(self.bars):
            SCREEN.blit(IMAGES['bar'], (self.bar[0]['x'], self.bar[0]['y']))
            if i == 0:
                if pygame.sprite.collide_mask(MakeSprite(IMAGES['bar'], self.bar[0]['x'], self.bar[0]['y']), MakeSprite(IMAGES['playerl'][0], self.playerx, self.playery)):
                    isCrash = True

            SCREEN.blit(IMAGES['bar'], (self.bar[1]['x'], self.bar[1]['y']))
            if i == 0:
                if pygame.sprite.collide_mask(MakeSprite(IMAGES['bar'], self.bar[1]['x'], self.bar[1]['y']), MakeSprite(IMAGES['playerl'][0], self.playerx, self.playery)):
                    isCrash = True

        for i, self.hammer in enumerate(self.hammers):
            rotated_img, x, y = rot_img(IMAGES['hammer'], theta(self.swingIter, self.hammer[0]['t']), self.hammer[0]['x'], self.hammer[0]['y'])
            SCREEN.blit(rotated_img, (x, y))
            if i == 0:
                if pygame.sprite.collide_mask(MakeSprite(rotated_img, x, y), MakeSprite(IMAGES['playerl'][0], self.playerx, self.playery)):
                    isCrash = True

            rotated_img, x, y = rot_img(IMAGES['hammer'], theta(self.swingIter, self.hammer[1]['t']), self.hammer[1]['x'], self.hammer[1]['y'])
            SCREEN.blit(rotated_img, (x, y))
            if i == 0:
                if pygame.sprite.collide_mask(MakeSprite(rotated_img, x, y), MakeSprite(IMAGES['playerl'][0], self.playerx, self.playery)):
                    isCrash = True

        if self.playerx + PLAYERWIDTH/2 < 0 or self.playerx + PLAYERWIDTH/2 > SCREENWIDTH:
            isCrash = True

        # print self.score so player overlaps the self.score
        
        if isCrash:
            self.__init__()
            terminal = True
            reward = -1

        # showScore(self.score)
        SCREEN.blit(IMAGES['playerl'][0], (self.playerx, self.playery))

        pygame.display.update()

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        FPSCLOCK.tick(FPS)
        return image_data[:,:self.playery+PLAYERHEIGHT].copy(), reward, terminal

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
    gapX = SCREENWIDTH * 0.5
    barWidth = IMAGES['bar'].get_width()
    offset = random.randint(-180, 220)
    # t = 30*cos(2*3.14159*random.uniform(0, 30)/180)

    return [
        {'x': x - 60, 'y': y + 10, 't': offset},
        {'x': x + gapX - 10, 'y': y + 10, 't': offset}
    ],[
        {'x': x - barWidth, 'y': y},
        {'x': x + gapX, 'y': y}
    ]

def showScore(score):
    """displays self.score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()

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

class MakeSprite(pygame.sprite.Sprite):

    def __init__(self, inp_image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = inp_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
