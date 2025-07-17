"""
Monopoly Game Player Banner Component Module

This module implements a player information banner component for the Monopoly game UI.
The PlayerBanner class displays player details including name, money, and game piece
in a colored banner with turn highlighting and position-based coordinate mapping for
multi-player layouts.

Author: Aidan Sabatini
"""

import pygame

from src.config.displayAssets import *
from src.config.colorAssets import *
from src.config.fontAssets import *
from src.config.gameAssets import *
from src.config.boardAssets import *
from src.config.imgAssets import *
from src.ui.components.Helper import *

pygame.init()


class PlayerBanner:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.pos = (self.getCoords()[3][0], self.getCoords()[3][1], BANNER_WIDTH, BANNER_HEIGHT)
        self.namePos = self.getCoords()[0]
        self.moneyPos = self.getCoords()[1]
        self.piecePos = self.getCoords()[2]

    #Get Coords for player banner assets returned as tuple of all coords in order [NAME, MONEY, PIECE, BANNER]
    def getCoords(self):
        match self.player.id:
            case 0:
                return [(P1_NAME_X, P1_NAME_Y), (P1_MON_X, P1_MON_Y), (P1_PIECE_X, P1_PIECE_Y), (P1_BANNER_X, P1_BANNER_Y)]
            case 1:
                return [(P2_NAME_X, P2_NAME_Y), (P2_MON_X, P2_MON_Y), (P2_PIECE_X, P2_PIECE_Y), (P2_BANNER_X, P2_BANNER_Y)]
            case 2:
                return [(P3_NAME_X, P3_NAME_Y), (P3_MON_X, P3_MON_Y), (P3_PIECE_X, P3_PIECE_Y), (P3_BANNER_X, P3_BANNER_Y)]
            case 3:
                return [(P4_NAME_X, P4_NAME_Y), (P4_MON_X, P4_MON_Y), (P4_PIECE_X, P4_PIECE_Y), (P4_BANNER_X, P4_BANNER_Y)]
            case _:
                return None


    def draw(self):
        #Turn Highlight
        if self.player.isTurn:
            draw_rounded_rect(self.screen, WHITE, (self.pos[0] - 5, self.pos[1] - 5, self.pos[2] + 10, self.pos[3] + 10), 10)


        #Background
        draw_rounded_rect(self.screen, self.player.color, self.pos, 10)
        #pygame.draw.rect(self.screen, self.player.color, self.pos)

        #Name
        textSurface = NAMEFONT.render(self.player.name, True, WHITE)
        textRect = textSurface.get_rect()
        textRect.center = (self.namePos[0] - ((textRect.width // 2) + DIE_GAP), self.namePos[1])
        self.screen.blit(textSurface, textRect)

        #Money 
        textSurface = MONEYFONT.render("$" + str(self.player.money), True, WHITE)
        textRect = textSurface.get_rect()
        textRect.center = (self.moneyPos[0] - ((textRect.width // 2) + DIE_GAP), self.moneyPos[1])
        self.screen.blit(textSurface, textRect)

        #Piece
        textSurface = PIECEFONT.render(str(self.player.piece), True, WHITE)
        textRect = textSurface.get_rect()
        textRect.bottomleft = (self.piecePos[0] + PIECE_OFFSET, self.piecePos[1])
        self.screen.blit(textSurface, textRect)



