import sys, pygame
import os
from paths import BASE, ASSETS, PICS, FONTS

pygame.init()

size = width, height = 1000, 1000
speed = [2, 2]
background = pygame.image.load(PICS / "wooden-texture.jpg")
background = pygame.transform.scale(background, (1000, 1000))


gameboard = pygame.image.load(PICS / "board_pattern.png")

screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(background, (0, 0))
    screen.blit(gameboard, (75, 100))
    pygame.display.flip()
