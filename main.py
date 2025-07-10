import pygame

from src.game.Controller import Game

from src.config.displayAssets import *

#Refactor/comment notes (Claude): 
# src/game: complete
# src/ui/components: Board.py & Button.py complete
# rest: incomplete


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
