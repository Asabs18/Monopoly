import pygame

from Assets.numAssets.displayAssets import *
from Assets.numAssets.colorAssets import *
from Assets.numAssets.imgAssets import *

pygame.init()

class Board:
    def __init__(self, screen):
        #Store const width and height for board
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        
        self.screen = screen
        
        self.x, self.y = self.findBoardCoord()

        self.image = BOARDIMG

    #Returns center of screen
    def findCenter(self):
        return (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    #Finds (x, y) for the top left of the board
    def findBoardCoord(self):
        center = self.findCenter()
        return (center[0] - self.width // 2, center[1] - self.height // 2)

    #Draws the board on the screen on top of a black rectangle
    def display(self):
        pygame.draw.rect(self.screen, BLACK, (self.x-5, self.y-5, self.width+10, self.height+10))
        self.screen.blit(self.image, (self.x, self.y))
    
