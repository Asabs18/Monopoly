import pygame

from Properties import *

from Assets.uiAssets.Button import *
from Assets.numAssets.colorAssets import *
from Assets.numAssets.fontAssets import *
from Assets.numAssets.displayAssets import *
from Assets.uiAssets.Helper import *

pygame.init()


class BuildMenu:
    def __init__(self, screen):
        self.screen = screen

        self.displayActivateBtn = False
        self.displayWin = False

        self.activateBtn = Button(self.screen, "🏠", GLYPHFONT, (ACTIVATE_BTN_X, ACTIVATE_BTN_Y, ACTIVATE_BTN_WIDTH, ACTIVATE_BTN_HEIGHT), GREEN)
        self.closeBtn = Button(self.screen, "Close", PIECEFONT, (CLOSE_BTN_X, CLOSE_BTN_Y, CLOSE_BTN_WIDTH, CLOSE_BTN_HEIGHT), RED)
        self.buildBtns = {}

    def display(self, players, player):

        self.update(player)

        self.drawHouses(players)
        
        if self.displayWin:
            self.displayWindow(player)
        self.drawActivateBtn()

    def displayWindow(self, player):
        #Window
        pygame.draw.rect(self.screen, BLACK, (START_WIN_X - 5, START_WIN_Y - 5, START_WIN_WIDTH + 10, START_WIN_HEIGHT + 10))
        pygame.draw.rect(self.screen, WHITE, (START_WIN_X, START_WIN_Y, START_WIN_WIDTH, START_WIN_HEIGHT))

        #Title
        drawText(self.screen, f"Build Property - {player.name}", PROPNAMEFONT, BLACK, (START_WIN_TITLE_X, START_WIN_TITLE_Y))
        pygame.draw.line(self.screen, BLACK, BUILD_NAME_LINE_START, BUILD_NAME_LINE_END, 2)

        #Close Button
        self.closeBtn.draw()

        #List properties
        self.drawProperties(player)

    def drawProperties(self, player):
        if len(player.getColorSets()) <= 16:
            for i, prop in enumerate(player.properties):
                if prop in self.buildBtns.keys():
                    if i <= 8:
                        pygame.draw.rect(self.screen, BLACK, (COLOR_BACKGROUND_X1 - 2, COLOR_BACKGROUND_Y + i * COLOR_BACKGROUND_OFFSET - 2, COLOR_BACKGROUND_WIDTH + 4, COLOR_BACKGROUND_HEIGHT + 4))
                        pygame.draw.rect(self.screen, prop.color, (COLOR_BACKGROUND_X1, COLOR_BACKGROUND_Y + i * COLOR_BACKGROUND_OFFSET, COLOR_BACKGROUND_WIDTH, COLOR_BACKGROUND_HEIGHT))
                        drawText(self.screen, f"{prop.name}", PROPTXTFONT, BLACK, (BUILD_PROP_X1, BUILD_PROP_Y + i * BUILD_PROP_OFFSET))
                    else:
                        pygame.draw.rect(self.screen, BLACK, (COLOR_BACKGROUND_X2 - 2, COLOR_BACKGROUND_Y + (i - 9) * COLOR_BACKGROUND_OFFSET - 2, COLOR_BACKGROUND_WIDTH + 4, COLOR_BACKGROUND_HEIGHT + 4))
                        pygame.draw.rect(self.screen, prop.color, (COLOR_BACKGROUND_X2, COLOR_BACKGROUND_Y + (i - 9) * COLOR_BACKGROUND_OFFSET, COLOR_BACKGROUND_WIDTH, COLOR_BACKGROUND_HEIGHT))
                        drawText(self.screen, f"{prop.name}", PROPTXTFONT, BLACK, (BUILD_PROP_X2, BUILD_PROP_Y + (i - 9) * BUILD_PROP_OFFSET))
                    self.drawBuildBtnTuple(self.buildBtns[prop])

    def drawActivateBtn(self):
        if self.displayActivateBtn:
            self.activateBtn.draw()
            drawText(self.screen, "Build", PIECEFONT, WHITE, (BUILD_LABEL_X, BUILD_LABEL_Y))


    #TODO: NEXT: fix house coords memberdata (include horz Bool) and fix rect prints to correct coords and colors etc
    def drawHouses(self, players):
        for player in players:
            for prop in player.properties:
                if prop in player.buildings.keys():
                    if prop.numHouses < 5:
                        for i in range(prop.numHouses):
                            if prop.houseCoords[1] == True:
                                self.drawHouse(GREEN, prop.houseCoords[0][0] + i * BUILD_HOUSE_OFFSET, prop.houseCoords[0][1], BUILD_HOUSE_WIDTH, BUILD_HOUSE_HEIGHT)
                            else:
                                self.drawHouse(GREEN, prop.houseCoords[0][0], prop.houseCoords[0][1] + i * BUILD_HOUSE_OFFSET, BUILD_HOUSE_WIDTH, BUILD_HOUSE_HEIGHT)
                    else:
                        if prop.houseCoords[1] == True:
                            self.drawHouse(RED, prop.houseCoords[0][0] + BUILD_HOTEL_OFFSET, prop.houseCoords[0][1], BUILD_HOTEL_WIDTH, BUILD_HOTEL_HEIGHT, True)
                        else:
                            self.drawHouse(RED, prop.houseCoords[0][0], prop.houseCoords[0][1] + BUILD_HOTEL_OFFSET, BUILD_HOTEL_HEIGHT, BUILD_HOTEL_WIDTH, True)

    def drawHouse(self, color, x, y, w, h, isHotel=False):
        if isHotel:
            pygame.draw.rect(self.screen, BLACK, (x - 1, y - 1, w + 2, h + 2))
            pygame.draw.rect(self.screen, color, (x, y, w, h))
        else:
            pygame.draw.rect(self.screen, BLACK, (x - 1, y - 1, w + 2, h + 2))
            pygame.draw.rect(self.screen, color, (x, y, w, h))

    def drawBuildBtnTuple(self, btns):
        btns[0].draw()
        btns[1].draw()

    def update(self, player):
        self.updateActivateOption(player)
        self.updateBuildBtns(player)

    def updateActivateOption(self, player):
        if player.getColorSets() != None:
            self.displayActivateBtn = True
        else:
            self.displayActivateBtn = False

    def updateBuildBtns(self, player):
        self.buildBtns = {}

        colorSets = player.getColorSets()
        for i, prop in enumerate(player.properties):
            if colorSets != None and isinstance(prop, ColorSet):
                if prop.color in colorSets:
                    if i <= 8:
                        self.buildBtns[prop] = (Button(self.screen, f"➕", PLUSMINFONT, (BUILD_BTN_X1, BUILD_BTN_Y + i * BUILD_PROP_OFFSET, BUILD_BTN_WIDTH, BUILD_BTN_HEIGHT), GREEN),
                                            Button(self.screen, f"➖", PLUSMINFONT, (BUILD_BTN_X1 + MIN_BTN_OFFSET, BUILD_BTN_Y + i * BUILD_PROP_OFFSET, BUILD_BTN_WIDTH, BUILD_BTN_HEIGHT), RED))
                    else:
                        self.buildBtns[prop] = (Button(self.screen, f"➕", PLUSMINFONT, (BUILD_BTN_X2, BUILD_BTN_Y + (i - 9) * BUILD_PROP_OFFSET, BUILD_BTN_WIDTH, BUILD_BTN_HEIGHT), GREEN), 
                                            Button(self.screen, f"➖", PLUSMINFONT, (BUILD_BTN_X2 + MIN_BTN_OFFSET, BUILD_BTN_Y + (i - 9) * BUILD_PROP_OFFSET, BUILD_BTN_WIDTH, BUILD_BTN_HEIGHT), RED))

    def getPropFromBtn(self, btn):
        for prop, btns in self.buildBtns.items():
            if btn in btns:
                return prop

    def activateBtnAction(self):
        self.displayWin = True

    def closeBtnAction(self):
        self.displayWin = False

    def checkBtnClicks(self, player, pos):
        for btns in self.buildBtns.values():
            if btns[0].isClicked(pos):
                self.plusBtnAction(player, btns[0])
            if btns[1].isClicked(pos):
                self.minusBtnAction(player, btns[0])

    def plusBtnAction(self, player, btn):
        prop = self.getPropFromBtn(btn)
        player.build(prop)

    def minusBtnAction(self, player, btn):
        pass