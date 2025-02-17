import pygame

from Controller import Game

from Assets.numAssets.displayAssets import *

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize Game Object
game = Game(screen)

# Run Game
game.loop()

# Quit Pygame
pygame.quit()
