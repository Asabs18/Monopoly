import pygame
import pygame.gfxdraw

from Properties import *

from Assets.numAssets.displayAssets import *
from Assets.numAssets.colorAssets import *
from Assets.numAssets.fontAssets import *
from Assets.numAssets.gameAssets import *
from Assets.numAssets.boardAssets import *
from Assets.numAssets.imgAssets import *
from Assets.uiAssets.PlayerBanner import *
from Assets.uiAssets.Helper import *

pygame.init()

#TODO: Implement bankruptcy
class Player:
    def __init__(self, screen, name, id, piece):
        self.screen = screen

        self.name = name
        self.id = id
        self.color = self.getColor()
        self.piece = PIECES[piece]

        self.location = ("Go", 0)

        self.money = 1500
        self.getOutOfJailFreeCards = 0
        self.properties = []
        self.buildings = {}

        self.isTurn = False
        self.inJail = False

        self.jailTurns = 0

        self.playerBanner = PlayerBanner(screen, self)
        self.playerPiece = playerPiece(screen, self)
    
    def getColor(self):
        match self.id:
            case 0:
                return RED
            case 1:
                return BLUE
            case 2:
                return LIGHT_GREEN
            case 3:
                return DARK_YELLOW

    def move(self, spaces):
        self.updateLocation(spaces)
        self.playerPiece.pos = self.playerPiece.getPos()

    #TODO: not tested
    def moveTo(self, location):
        if self.location[1] > location:
            self.move((NUM_CELLS - self.location[1]) + location)
        else:
            self.move(location - self.location[1])
        self.playerPiece.pos = self.playerPiece.getPos()

    def updateLocation(self, spaces):
        if self.location[1] + spaces < len(TRACK) and self.location[1] + spaces > 0:
            self.location = (self.location[0], self.location[1] + spaces)
        elif self.location[1] + spaces >= len(TRACK):
            self.location = (self.location[0], (self.location[1] + spaces) - len(TRACK))
            self.money += 200
        self.location = (TRACK[self.location[1]], self.location[1])
        if self.location[0] == "Go":
            self.money += 200

    def displayProperties(self):
        for prop in self.properties:
            if prop.isTagHorz:
                draw_rounded_rect(self.screen, self.color, (prop.tagPos[0], prop.tagPos[1], PROP_TAG_WIDTH, PROP_TAG_HEIGHT), 5)
            else:
                draw_rounded_rect(self.screen, self.color, (prop.tagPos[0], prop.tagPos[1], PROP_TAG_HEIGHT, PROP_TAG_WIDTH), 5)

    def sendToJail(self):
        self.inJail = True
        self.location = ("In Jail", 10)
        self.playerPiece.pos = self.playerPiece.getPos()

    def jailTurn(self, diceSet):
        if self.inJail:
            if diceSet.isDouble():
                self.jailTurns = 0
                self.inJail = False
                self.move(diceSet.getValue())
            if self.jailTurns >= 2:
                self.jailTurns = 0
                #TODO: special case bankruptcy
                if self.money >= 50:
                    self.money -= 50
                    self.inJail = False
                    self.move(diceSet.getValue())
            else:
                self.jailTurns += 1

    def payBail(self):
        if self.money >= 50:
            self.money -= 50
            self.inJail = False
            self.jailTurns = 0

    def giveTurn(self):
        self.isTurn = True

    def removeTurn(self):
        self.isTurn = False

    def charge(self, amount):
        if self.money >= amount:
            self.money -= amount
        else:
            self.money = 0
            #TODO: special case bankruptcy

    def build(self, prop):
        if prop not in self.buildings.keys():
            self.buildings[prop] = 0
        if self.buildings[prop] < 5 and self.money >= prop.buildCost:
            self.buildings[prop] += 1
            prop.numHouses += 1
            self.charge(prop.buildCost)

    def getColorSets(self):
        colorSets = []

        count = { BROWN: 0, LIGHT_BLUE: 0, PURPLE: 0, ORANGE: 0, RED: 0, YELLOW: 0, GREEN: 0, DARK_BLUE: 0 }

        for prop in self.properties:
            if isinstance(prop, ColorSet):
                count[prop.color] += 1

        for colorSet in count.keys():
            if count[colorSet] >= 3:
                colorSets.append(colorSet)
            elif colorSet == BROWN or colorSet == DARK_BLUE:
                if count[colorSet] >= 2:
                    colorSets.append(colorSet)

        if colorSets == []:
            return None
        return colorSets

    def drawHouses(self):
        for building in self.buildings.keys():
            for i in range(self.buildings[building]):
                self.drawHouse(building, i)

    def drawHouse(self, building, index):
        if building.isTagHorz:
            draw_rounded_rect(self.screen, self.color, (building.tagPos[0] + (PROP_TAG_WIDTH * index), building.tagPos[1], PROP_TAG_WIDTH, PROP_TAG_HEIGHT), 5)
        else:
            draw_rounded_rect(self.screen, self.color, (building.tagPos[0], building.tagPos[1] + (PROP_TAG_WIDTH * index), PROP_TAG_HEIGHT, PROP_TAG_WIDTH), 5)
            

    



class playerPiece:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.pos = self.getPos()

        self.img = self.getImg()

    def draw(self):
        self.screen.blit(self.img, (self.pos[0], self.pos[1]))

    def getImg(self):
        match self.player.piece:
            case "Boat":
                return PIECE_IMGS[0]
            case "Car":
                return PIECE_IMGS[1]
            case "Hat":
                return PIECE_IMGS[2]
            case "Scope":
                return PIECE_IMGS[3]
            case "Shoe":
                return PIECE_IMGS[4]
            case "Wheelbarrow":
                return PIECE_IMGS[5]
            case _:
                return None

    def getPos(self):
        match self.player.id:
            case 0:
                return BOARDCOORDS[self.player.location[0]][0]
            case 1:
                return BOARDCOORDS[self.player.location[0]][1]
            case 2:
                return BOARDCOORDS[self.player.location[0]][2]
            case 3:
                return BOARDCOORDS[self.player.location[0]][3]
            case _: 
                return None
    