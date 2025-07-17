"""
Monopoly Game Trade Menu Component Module

This module implements the property trading interface for the Monopoly game.
The TradeMenu class provides a user interface for initiating trades between
players, including player selection, property exchange management, and
trade negotiation controls with visual feedback and interactive buttons.

Author: Aidan Sabatini
"""

import pygame

from src.ui.components.Button import *
from src.config.colorAssets import *
from src.ui.components.Helper import *

pygame.init()

#TODO: Finish Trade Menu
class TradeMenu:
    def __init__(self, screen):
        self.screen = screen

        self.displayActivateBtn = True
        self.displayWin = False

        self.player1 = None
        self.player2 = None

        self.selectBtnList = []

        self.activateBtn = Button(self.screen, "🤝", GLYPHFONT, (TRADE_ACTIVATE_BTN_X, TRADE_ACTIVATE_BTN_Y, ACTIVATE_BTN_WIDTH, ACTIVATE_BTN_HEIGHT), GREEN)
        self.closeBtn = Button(self.screen, "Close", PIECEFONT, (CLOSE_BTN_X, CLOSE_BTN_Y, CLOSE_BTN_WIDTH, CLOSE_BTN_HEIGHT), RED)


    def display(self, players, player):

        self.update(players, player)
        
        if self.displayWin:
            self.displayWindow(players, player)
        self.drawActivateBtn()

    def displayWindow(self, players, player):
        #Window
        pygame.draw.rect(self.screen, BLACK, (START_WIN_X - 5, START_WIN_Y - 5, START_WIN_WIDTH + 10, START_WIN_HEIGHT + 10))
        pygame.draw.rect(self.screen, WHITE, (START_WIN_X, START_WIN_Y, START_WIN_WIDTH, START_WIN_HEIGHT))

        #Title
        if self.player2 == None:
            drawText(self.screen, f"Trade - {self.player1.name}", PROPNAMEFONT, BLACK, (START_WIN_TITLE_X, START_WIN_TITLE_Y))
        else:
            drawText(self.screen, f"Trade - {self.player1.name} to {self.player2.name}", PROPNAMEFONT, BLACK, (START_WIN_TITLE_X, START_WIN_TITLE_Y))
        pygame.draw.line(self.screen, BLACK, BUILD_NAME_LINE_START, BUILD_NAME_LINE_END, 2)

        #Trade Player Selection
        if self.player2 == None:
            self.drawSelection(players)

        #Close Button
        self.closeBtn.draw()

    def drawSelection(self, players):
        drawText(self.screen, "Select Player", PIECEFONT, BLACK, (TRADE_SELECT_X, TRADE_SELECT_Y))
        for btn in self.selectBtnList:
            btn[0].draw()

    def drawProperties(self, player):
        pass

    def drawActivateBtn(self):
        if self.displayActivateBtn:
            self.activateBtn.draw()
            drawText(self.screen, "Trade", PIECEFONT, WHITE, (TRADE_LABEL_X, TRADE_LABEL_Y))

    def checkBtnClicks(self, player, pos):
        for btn in self.selectBtnList:
            if btn[0].isClicked(pos):
                self.selectBtnAction(btn)

    def update(self, players, currTurnPlayer):
        self.player1 = currTurnPlayer
        self.selectBtnList = self.createButtons(players)

    def createButtons(self, players):
        btnList = []
        if self.player2 == None:
            for i, player in enumerate(players):
                if player != self.player1:
                    btnList.append((Button(self.screen, player.name, PIECEFONT, (PLAYER_SELECTION_BTN_X, PLAYER_SELECTION_BTN_Y + i * PLAYER_SELECTION_BTN_OFFSET, PLAYER_SELECTION_BTN_WIDTH, PLAYER_SELECTION_BTN_HEIGHT), player.color), player))
        
        return btnList

    def selectBtnAction(self, btn):
        self.player2 = btn[1]

    def activateBtnAction(self):
        self.displayWin = True

    def closeBtnAction(self):
        self.displayWin = False
        self.player2 = None