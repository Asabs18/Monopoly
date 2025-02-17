import pygame

from Assets.uiAssets.Button import *

pygame.init()

#TODO: Finish Trade Menu
class TradeMenu:
    def __init__(self, screen):
        self.screen = screen

        self.displayActivateBtn = False
        self.displayWin = False

        #TODO: Create activate and close button information in displayAssets
        #self.activateBtn = Button(self.screen, "🏠", GLYPHFONT, (ACTIVATE_BTN_X, ACTIVATE_BTN_Y, ACTIVATE_BTN_WIDTH, ACTIVATE_BTN_HEIGHT), GREEN)
        #self.closeBtn = Button(self.screen, "Close", PIECEFONT, (CLOSE_BTN_X, CLOSE_BTN_Y, CLOSE_BTN_WIDTH, CLOSE_BTN_HEIGHT), RED)