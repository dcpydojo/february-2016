import random
import numpy
import pygame, sys, time
from pygame.locals import *

# set up pygame
pygame.mixer.pre_init(frequency=16000, size=8, channels=1)
pygame.init()

# set up the window
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

# set up direction variables
DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9
RANDOM = 11

# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (203, 85, 153)

class Item(object):
    def __init__(self, dimensions, color, direction, speed,
                 moves_randomly=False):
        self.rect = pygame.Rect(*dimensions)
        self.color = color
        self.direction = direction
        self.moves_randomly = moves_randomly
        self.speed = speed
        self.bouncing = False


frame_counter = 0
RANDOM_DIR = random.choice((DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT))

# set up the block data structure
b1 = Item((300, 80, 50, 100), RED, UPRIGHT, 14)
b2 = Item((200, 200, 20, 20), GREEN, UPLEFT, 26)
b3 = Item((100, 150, 60, 60), BLUE, DOWNLEFT, 7)
b4 = Item((75, 75, 57, 57), PINK, RANDOM_DIR, 17, True)
items = [b1, b2, b3, b4]

# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    for b in items:
        b.bouncing = False # default not to bouncing
        # move the block data structure
        if (frame_counter % 37) == 0:
            RANDOM_DIR = random.choice([DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT])
            if b.moves_randomly:
                b.direction = RANDOM_DIR
                b.speed = random.randint(11, 22)

        if b.direction == DOWNLEFT:
            b.rect.left -= b.speed
            b.rect.top += b.speed
        if b.direction == DOWNRIGHT:
            b.rect.left += b.speed
            b.rect.top += b.speed
        if b.direction == UPLEFT:
            b.rect.left -= b.speed
            b.rect.top -= b.speed
        if b.direction == UPRIGHT:
            b.rect.left += b.speed
            b.rect.top -= b.speed

        # check if the block has move out of the window
        if b.rect.top < 0:
            # block has moved past the top
            b.bouncing = True
            if b.direction == UPLEFT:
                b.direction = DOWNLEFT
            if b.direction == UPRIGHT:
                b.direction = DOWNRIGHT

        if b.rect.bottom > WINDOWHEIGHT:
            b.bouncing = True
            # block has moved past the bottom
            if b.direction == DOWNLEFT:
                b.direction = UPLEFT
            if b.direction == DOWNRIGHT:
                b.direction = UPRIGHT

        if b.rect.left < 0:
            b.bouncing = True
            # block has moved past the left side
            if b.direction == DOWNLEFT:
                b.direction = DOWNRIGHT
            if b.direction == UPLEFT:
                b.direction = UPRIGHT

        if b.rect.right > WINDOWWIDTH:
            b.bouncing = True
            # block has moved past the right side
            if b.direction == DOWNRIGHT:
                b.direction = DOWNLEFT
            if b.direction == UPRIGHT:
                b.direction = UPLEFT

        # draw the block onto the surface
        pygame.draw.rect(windowSurface, b.color, b.rect)
        # play a sound if necessary
        if b.bouncing:
            rgb = b.color
            rgbarray = numpy.array(rgb * 2500)
            sound = pygame.mixer.Sound(rgbarray)
            sound.play(fade_ms=50)
            sound.fadeout(100)


    # draw the window onto the screen
    frame_counter += 1
    pygame.display.update()
    time.sleep(0.02)
