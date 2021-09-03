import pygame
from random import randrange
from math import sqrt
from math import pow
import os
from pygame import mixer

d = "happ_meter_frames"
paths_list = []
for path in os.listdir(d):
    full_path = os.path.join(d, path)  # string
    paths_list.append(full_path)

# Initializing pygame
pygame.init()

# creating a game window
WIDTH, HEIGHT = 800, 533
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and Icon
pygame.display.set_caption("Tiny Game no.01")
icon = pygame.image.load('frog.png')
pygame.display.set_icon(icon)

# Background
background_img = pygame.image.load('frog_background.png')

background_sound = mixer.Sound('swamp_ambience.wav')
background_sound.play()

# Game over screen
fully_happy_img = pygame.image.load('game_over_background.png')

# Player
playerImg = pygame.image.load('frog_char.png')  # Returns a surface
playerImg_fl = pygame.transform.flip(playerImg, True, False)  # Returns a surface

plr_posX = 400
plr_posY = 300
plr_posX_change = 0
plr_posY_change = 0

# Flower
flower_img = []
flr_posX = []
flr_posY = []
num_of_flowers = 1

for i in range(num_of_flowers):
    flower_img.append(pygame.image.load('flower.png'))
    flr_posX.append(randrange(160, 730))
    flr_posY.append(randrange(72, 465))

# Happiness meter
happiness_value = 0

font = pygame.font.Font('Pixel_Digivolve.otf', 24)  # font object
# font by 'Pixel Sagas' http://www.pixelsagas.com

FPS = 60
clock = pygame.time.Clock()


def player(x, y):
    window.blit(playerImg, (x, y))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            window.blit(playerImg_fl, (x, y))
            playerImg.set_alpha(0)  # 0 is fully transparent and 255 fully opaque.
        elif event.key == pygame.K_LEFT:
            playerImg.set_alpha(255)
            window.blit(playerImg, (x, y))
        elif event.key == pygame.K_UP:
            playerImg.set_alpha(255)
            window.blit(playerImg, (x, y))
        elif event.key == pygame.K_DOWN:
            playerImg.set_alpha(255)
            window.blit(playerImg, (x, y))
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            pass
        elif event.key == pygame.K_RIGHT:
            window.blit(playerImg_fl, (x, y))
        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            pass


def flower(x, y, i):
    window.blit(flower_img[i], (x, y))


def happiness_meter():
    current_frame = pygame.image.load(paths_list[happiness_value])
    window.blit(current_frame, (0, 0))


def is_collision(plr_x, plr_y, flr_x, flr_y):
    distance = sqrt(pow(plr_x - flr_x, 2) + pow(plr_y - flr_y, 2))
    if distance < 30:
        return True
    else:
        return False


# Game Loop
active = True
while active:
    clock.tick(FPS)
    window.fill((102, 0, 102))
    window.blit(background_img, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            active = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                plr_posX_change = 4
            elif event.key == pygame.K_LEFT:
                plr_posX_change = -4
            elif event.key == pygame.K_UP:
                plr_posY_change = -4
            elif event.key == pygame.K_DOWN:
                plr_posY_change = 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or \
                    event.key == pygame.K_DOWN:
                plr_posX_change = 0
                plr_posY_change = 0

    plr_posX += plr_posX_change
    plr_posY += plr_posY_change

    if plr_posX > 735:
        plr_posX = 735
    elif plr_posX < 0:
        plr_posX = 0
    elif plr_posY > 468:
        plr_posY = 468
    elif plr_posY < 0:
        plr_posY = 0

    for i in range(num_of_flowers):
        collision = is_collision(plr_posX, plr_posY, flr_posX[i], flr_posY[i])
        if collision:
            flower_sound = mixer.Sound('flower_sound.wav')
            flower_sound.play()
            if happiness_value < 9:
                flr_posX[i] = randrange(160, 730)
                flr_posY[i] = randrange(72, 465)
                happiness_value += 1
            else:
                num_of_flowers = 0
                happiness_value += 1

        flower(flr_posX[i], flr_posY[i], i)

    if happiness_value == 10:
        window.blit(fully_happy_img, (0, 0))
        game_over_text = font.render("The frog is now fully happy!", True, (51, 102, 0))  # surface
        window.blit(game_over_text, (200, 210))
        ending_music = mixer.Sound('endingtheme.wav')
        ending_music.play(-1)

    player(plr_posX, plr_posY)

    happiness_meter()

    pygame.display.update()
