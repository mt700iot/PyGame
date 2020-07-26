# main.py
import pygame
import math
import random

# initial pygame
pygame.init()

WIDTH = 1000
HEIGHT = 600

# screen setting
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Covid-19 Fighter')  # set Window Title
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load('background.jpg')

# ===== Player =====
# 1 - player - boy.png
pSize = 128
pImg = pygame.image.load('boy.png')
px = 100  # startPoint x-axis
py = HEIGHT-pSize  # startPoint y-axis
pxChange = 0

# ===== Enemy =====
# 1 - virus - virus.png
eSize = 64
eImg = pygame.image.load('virus.png')
ex = 50
ey = 0
eyChange = 1

# ===== Mask =====
# 1 - mask - mask.png
mSize = 32
mImg = pygame.image.load('mask.png')
mx = 100
my = HEIGHT-pSize
myChange = 20
mState = 'ready'


def Player(x, y):
    screen.blit(pImg, (x, y))  # วางภาพในหน้าจอ


def Enemy(x, y):
    screen.blit(eImg, (x, y))


def fire_mask(x, y):
    global mState
    mState = 'fire'
    screen.blit(mImg, (x, y))


def isCollision(ecx, ecy, mcx, mcy):
    distance = math.sqrt(math.pow(ecx-mcx, 2)+math.pow(ecy-mcy, 2))
    print(distance)
    if distance < (eSize/2+mSize/2):
        return True
    else:
        return False


# ===== Game Loop =====
running = True  # set running state
clock = pygame.time.Clock()
FPS = 60
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # run loop check ว่ามีการกดปิด pygame [x]
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pxChange = -10
            if event.key == pygame.K_RIGHT:
                pxChange = 10
            if event.key == pygame.K_SPACE:
                if mState == 'ready':
                    mx = px + 50  # ขยับออกมาด้านขวา
                    fire_mask(mx, my)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pxChange = 0

            # print(event)

    # ===== run player =====
    Player(px, py)  # start px,py
    # ===== player move =====
    if px <= 0:
        px = 0
        px = px + pxChange
    elif px >= WIDTH - pSize:
        px = WIDTH - pSize
        px = px + pxChange
    else:
        px = px + pxChange

    # ===== run enemy =====

    Enemy(ex, ey)
    ey = ey + eyChange

    # ===== fire mask =====
    if mState == 'fire':
        fire_mask(mx, my)
        my = my-myChange
    if my <= 0:  # check mask is top and set ready state
        my = HEIGHT - pSize
        mState = 'ready'

    collision = isCollision(ex, ey, mx, my)
    if collision:
        my = HEIGHT - pSize
        mState = 'ready'
        ey = 0
        ex = random.randint(0, WIDTH-eSize)  # random virus position

    print(px, pxChange)
    pygame.display.update()
    clock.tick(FPS)
    screen.fill((0, 0, 0))  # clear blit image
    # pygame.display.flip()
