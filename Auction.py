import pygame

from Assets.numAssets.colorAssets import *
from Assets.numAssets.displayAssets import *
from Assets.numAssets.fontAssets import *
from Assets.uiAssets.Button import *
from Assets.uiAssets.Helper import *

pygame.init()


class Auction:
    def __init__(self, screen, players, property):
        self.screen = screen

        self.isRunning = False

        self.players = [(player, 0) for player in players]

        self.property = property

        self.currPrice = 10 #starting price for any auction is $10

        self.smlBidBtn = Button(self.screen, "Small Bid", (SML_BID_BTN_X, SML_BID_BTN_Y, AUC_BTN_WIDTH, AUC_BTN_HEIGHT), GREEN)
        self.bigBidBtn = Button(self.screen, "Big Bid", (BIG_BID_BTN_X, BIG_BID_BTN_Y, AUC_BTN_WIDTH, AUC_BTN_HEIGHT), YELLOW)
        self.withdrawBtn = Button(self.screen, "Withdraw", (WITHDRAW_BTN_X, WITHDRAW_BTN_Y, AUC_BTN_WIDTH, AUC_BTN_HEIGHT), RED)

    def start(self):
        self.isRunning = True

    def display(self):
        #Window
        pygame.draw.rect(self.screen, BLACK, (START_WIN_X - 5, START_WIN_Y - 5, START_WIN_WIDTH + 10, START_WIN_HEIGHT + 10))
        pygame.draw.rect(self.screen, WHITE, (START_WIN_X, START_WIN_Y, START_WIN_WIDTH, START_WIN_HEIGHT))

        #Title
        drawText(self.screen, f"{self.property.name} Auction", PROPNAMEFONT, BLACK, (START_WIN_TITLE_X, START_WIN_TITLE_Y))

        #Buttons
        self.smlBidBtn.draw()
        self.bigBidBtn.draw()
        self.withdrawBtn.draw()
