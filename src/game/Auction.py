"""
Monopoly Game Auction System Module

This module implements the property auction system for the Monopoly board game.
When a player lands on an unowned property and chooses not to buy it, or when
bankruptcy requires asset liquidation, properties go to auction where all players
can bid competitively.

Author: Aidan Sabatini
"""

import pygame

from src.config.colorAssets import *
from src.config.displayAssets import *
from src.config.fontAssets import *
from src.ui.components.Button import *
from src.ui.components.Helper import *

pygame.init()


class Auction:
    def __init__(self, screen, players, property):
        self.screen = screen

        self.isRunning = False

        self.players = [(player, 0) for player in players]

        self.property = property

        self.currPrice = 0
        self.nextBid = self.currPrice + 10

        self.currTurn = self.players[0] #Auctions always start with player 1

        self.bidBtn = Button(self.screen, "Bid", PIECEFONT, (BID_BTN_X, BID_BTN_Y, AUC_BTN_WIDTH, AUC_BTN_HEIGHT), GREEN)
        self.withdrawBtn = Button(self.screen, "Withdraw", PIECEFONT, (WITHDRAW_BTN_X, WITHDRAW_BTN_Y, AUC_BTN_WIDTH, AUC_BTN_HEIGHT), RED)

    def start(self):
        self.isRunning = True

    def display(self):
        if self.isRunning:
            #Window
            pygame.draw.rect(self.screen, BLACK, (START_WIN_X - 5, START_WIN_Y - 5, START_WIN_WIDTH + 10, START_WIN_HEIGHT + 10))
            pygame.draw.rect(self.screen, WHITE, (START_WIN_X, START_WIN_Y, START_WIN_WIDTH, START_WIN_HEIGHT))

            #Title
            drawText(self.screen, "Auction", PROPNAMEFONT, BLACK, (START_WIN_TITLE_X, START_WIN_TITLE_Y))
            pygame.draw.line(self.screen, BLACK, AUC_NAME_LINE_START, AUC_NAME_LINE_END, 2)

            #Buttons
            self.bidBtn.draw()
            self.withdrawBtn.draw()

            #Player Bids
            self.drawPlayers()

            #Asking Bid
            drawText(self.screen, f"Asking: ${self.nextBid}", PROPNAMEFONT, BLACK, (ASKING_BID_X, ASKING_BID_Y))
                
            #Property Card
            self.property.smallCard(AUC_CARD_X, AUC_CARD_Y, AUC_CARD_WIDTH, AUC_CARD_HEIGHT)

    def drawPlayers(self):
        for i, player in enumerate(self.players):
            if player[1] != None:
                #Player Name
                drawText(self.screen, f"{player[0].name}'s bid: ${player[1]}", PIECEFONT, BLACK, (PLAYER_BID_X, PLAYER_BID_Y + (i * 80)))

                if self.currTurn == player:
                    pygame.draw.circle(self.screen, BLACK, (PLAYER_BID_X - AUC_TURN_IND_OFFSET, PLAYER_BID_Y + (i * 80)), round(AUC_TURN_IND_RAD + 2), round(AUC_TURN_IND_WIDTH + 2))
                    pygame.draw.circle(self.screen, LIGHT_GREEN, (PLAYER_BID_X - AUC_TURN_IND_OFFSET, PLAYER_BID_Y + (i * 80)), round(AUC_TURN_IND_RAD), round(AUC_TURN_IND_WIDTH))

    def bidBtnAction(self):
        self.players[self.currTurn[0].id] = (self.currTurn[0], self.nextBid)
        self.currPrice = self.nextBid
        self.nextBid += 10
        self.updateTurn()

    def withdrawBtnAction(self):
        for player in self.players:
            if player == self.currTurn:
                self.players[self.currTurn[0].id] = (self.currTurn[0], None)
                break
        self.updateTurn()

    def updateTurn(self):
        if self.getNumActivePlayers() <= 1:
            self.isRunning = False
            self.sellProperty()
            return

        playerFound = False
        while not playerFound:
            if self.currTurn[0].id == len(self.players) - 1 and self.currTurn[1] != None:
                self.currTurn = self.players[0]
            else:
                self.currTurn = self.players[self.currTurn[0].id + 1]
            if self.currTurn[1] != None:
                playerFound = True


    def sellProperty(self):
        auctionWinner = self.getHighestBidder()
        self.property.buyAuc(auctionWinner[0], auctionWinner[1])

    def getHighestBidder(self):
        bidder = (None, -1)
        for player in self.players:
            if player[1] != None:
                if player[1] > bidder[1]:
                    bidder = player
        return bidder

    def getNumActivePlayers(self):
        totalActivePlayers = 0
        for player in self.players:
            if player[1] != None:
                totalActivePlayers += 1

        return totalActivePlayers