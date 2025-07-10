import pygame, random

from time import sleep

from src.game.Player import *
from src.game.Dice import *
from src.game.Cards import *
from src.game.Properties import *
from src.ui.menus.BuildMenu import *
from src.ui.menus.TradeMenu import *

from src.config.colorAssets import *
from src.config.displayAssets import *
from src.config.fontAssets import *
from src.config.imgAssets import *
from src.ui.components.Button import *
from src.ui.components.StartupWindow import *
from src.ui.components.Board import *


pygame.init()


#TODO: Fix dice double not repeating (and add three doubles send to jail)
#TODO: Fix jail, nothing works lmai
#TODO: Figure out why chance and com chest sometimes dont display/action
#TODO: Implement bankruptcy and trading
#TODO: Fix style errors like order of build house names, colors etc make everything look goooood

#Main Game loop class
class Game:
    def __init__(self, screen):
        self.screen = screen

        #Create board, dice set, and startup window
        self.board = Board(screen)
        self.diceSet = DiceSet(screen)
        self.startupWindow = StartupWindow(self.screen, ST_PIECE_IMGS)
        self.boardSpaces = Cells(self.screen)

        #Home Building
        self.buildMenu = BuildMenu(self.screen)

        #Trading
        self.tradeMenu = TradeMenu(self.screen)

        #List of all players and current turn player
        self.players = []
        self.currTurn = None
        self.currTurnLoc = None

        #Dice status
        self.displayDice = False
        self.diceRolled = False

        #Jail window
        #self.jailWindow = InJailWindow(self.screen)

        #UI Assets
        self.nxtTurnBtn = Button(self.screen, "End Turn", BTNFONT, (NXT_TURN_BTN_X, NXT_TURN_BTN_Y, NXT_TURN_BTN_WIDTH, NXT_TURN_BTN_HEIGHT), RED)

        #Window Title
        pygame.display.set_caption("Monopoly")

    #Controls overall loop for game
    def loop(self):
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if self.isQuit(event):
                    running = False
                self.handleKeydown(event)
                self.handleClick(event)

            self.handleDice()

            #TODO: Move outside loop
            if not self.currTurn == None:
                self.currTurnLoc = self.boardSpaces.properties[self.currTurn.location[0]]

            self.update()

            # Update game state
            self.display()

            pygame.display.flip()

    #Controls overall loop for game
    def testLoop(self):
        self.addPlayer("Aidan", 0, 2)
        self.addPlayer("Piv", 1, 3)

        #self.players[0].move(0)
        #self.diceRolled = True
        self.boardSpaces.properties["Connecticut Avenue"].buy(self.players[0])
        self.boardSpaces.properties["Vermont Avenue"].buy(self.players[0])
        self.boardSpaces.properties["Oriental Avenue"].buy(self.players[0])

        self.boardSpaces.properties["Marvin Gardens"].buy(self.players[0])
        self.boardSpaces.properties["Pennsylvania Railroad"].buy(self.players[0])

        self.boardSpaces.properties["States Avenue"].buy(self.players[1])
        self.boardSpaces.properties["St. Charles Place"].buy(self.players[1])
        self.boardSpaces.properties["Virginia Avenue"].buy(self.players[1])

        self.boardSpaces.properties["Boardwalk"].buy(self.players[1])



        self.start()

        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if self.isQuit(event):
                    running = False
                self.handleKeydown(event)
                self.handleClick(event)

            self.handleDice()

            #TODO: Move outside loop
            if not self.currTurn == None:
                self.currTurnLoc = self.boardSpaces.properties[self.currTurn.location[0]]

            self.update()

            # Update game state
            self.display()

            pygame.display.flip()

    #Helper function to handle keydown events
    def handleKeydown(self, event):
        if event.type == pygame.KEYDOWN:
            #Handle typing for names in startup window
            if self.startupWindow.isStartup:
                self.startupWindow.nameInputBox.handle_event(event)
            else:
                #Controls die rolls
                if event.key == pygame.K_SPACE and self.diceSet.isDisplayed and not self.currTurnLoc.show:
                    if not self.currTurn.inJail:
                        self.currTurn.move(self.diceSet.roll())
                        sleep(1)
                        self.diceRolled = True
                    else:
                        self.diceSet.roll()
                        self.currTurn.jailTurn(self.diceSet)
                        sleep(1)
                        self.diceRolled = True


    #Helper function to handle click events
    def handleClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handleStartupWinInput()
            if self.nxtTurnBtn.isClicked(pygame.mouse.get_pos()):
                self.updateTurn()
            if not self.currTurnLoc == None:
                if self.buildMenu.activateBtn.isClicked(pygame.mouse.get_pos()):
                    self.buildMenu.activateBtnAction()
                if self.buildMenu.displayWin:
                    if self.buildMenu.closeBtn.isClicked(pygame.mouse.get_pos()):
                        self.buildMenu.closeBtnAction()
                    self.buildMenu.checkBtnClicks(self.currTurn, pygame.mouse.get_pos())
                if self.tradeMenu.activateBtn.isClicked(pygame.mouse.get_pos()):
                    self.tradeMenu.activateBtnAction()
                if self.tradeMenu.displayWin:
                    if self.tradeMenu.closeBtn.isClicked(pygame.mouse.get_pos()):
                        self.tradeMenu.closeBtnAction()
                    self.tradeMenu.checkBtnClicks(self.currTurn, pygame.mouse.get_pos())
                if isinstance(self.currTurnLoc, Property):
                    if self.currTurnLoc.auction != None:
                        if self.currTurnLoc.auction.bidBtn.isClicked(pygame.mouse.get_pos()):
                            self.currTurnLoc.auction.bidBtnAction()
                        elif self.currTurnLoc.auction.withdrawBtn.isClicked(pygame.mouse.get_pos()):
                            self.currTurnLoc.auction.withdrawBtnAction()
                    if self.currTurnLoc.buyBtn.isClicked(pygame.mouse.get_pos()):
                        if self.currTurnLoc.canBuy(self.currTurn):
                            self.currTurnLoc.buyBtnAction(self.currTurn)
                    elif self.currTurnLoc.auctionBtn.isClicked(pygame.mouse.get_pos()):
                        self.currTurnLoc.auctionBtnAction(self.players)
                if isinstance(self.currTurnLoc, FreeParking) or isinstance(self.currTurnLoc, GoToJail):
                    if self.currTurnLoc.okBtn.isClicked(pygame.mouse.get_pos()):
                        self.currTurnLoc.okBtnAction(self.currTurn)
                elif isinstance(self.currTurnLoc, Card):
                    if self.currTurnLoc.okBtn.isClicked(pygame.mouse.get_pos()):
                        self.currTurnLoc.okBtnAction(self.players)
                elif isinstance(self.currTurnLoc, Tax):
                    if self.currTurnLoc.okBtn.isClicked(pygame.mouse.get_pos()):
                        self.boardSpaces.properties["Free Parking"].deposit(self.currTurnLoc.okBtnAction(self.currTurn))
                elif isinstance(self.currTurnLoc, Jail):
                    if self.currTurnLoc.payBtn.isClicked(pygame.mouse.get_pos()):
                        self.currTurnLoc.payBtnAction(self.currTurn)
                else:
                    pass

    def update(self):
        if isinstance(self.currTurnLoc, Property):
            self.currTurnLoc.update(self.players)
            if self.currTurnLoc.show:
                if self.currTurnLoc.canCharge(self.currTurn):
                    self.currTurnLoc.charge(self.currTurn)
                    self.currTurnLoc.show = False
                elif self.currTurnLoc in self.currTurn.properties:
                    self.currTurnLoc.show = False
    
    #Startup window UI input handling
    def handleStartupWinInput(self):
        #Handles close button click and invalid cases
        if self.startupWindow.isStartup:
            if self.startupWindow.closeBtn.isClicked(pygame.mouse.get_pos()):
                if len(self.players) >= 2:
                    self.start()

            #Handles add button click and invalid cases
            if self.startupWindow.addBtn.isClicked(pygame.mouse.get_pos()):
                if self.startupWindow.nameInputBox.text != "" and self.startupWindow.selectedPiece != None and len(self.players) <= 4:
                    self.addPlayer(self.startupWindow.nameInputBox.text, len(self.players), self.startupWindow.selectedPiece)
                    self.startupWindow.PieceImages[self.startupWindow.selectedPiece] = None
                    self.startupWindow = StartupWindow(self.screen,self.startupWindow.PieceImages)
            
            #Handles input box and piece click events and updates accordingly
            self.startupWindow.nameInputBox.isClicked(pygame.mouse.get_pos())
            self.startupWindow.selectedPiece = self.startupWindow.isPieceClicked(pygame.mouse.get_pos())

    #Handle Dice
    def handleDice(self):
        self.displayDice = self.doDisplayDice()

        if self.displayDice and not self.diceSet.isDisplayed: 
            self.diceSet.toggle()

        if self.diceRolled:
            self.displayDice = False
            if self.diceSet.isDisplayed:
                if self.currTurn.inJail:
                    self.diceSet.toggle()
                elif not self.currTurnLoc.show:
                    self.diceSet.toggle()
    
    def displayWin(self):
        displayWin = True
        if self.currTurn == None or not self.diceRolled:
            displayWin = False
        if displayWin:
            self.currTurnLoc.display()


    #Helper function to define quit events
    def isQuit(self, event):
        return event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)

    #Adds player to list of players
    def addPlayer(self, name, id, piece):
        self.players.append(Player(self.screen, name, id, piece))

    def pickStartTurn(self):
        player = random.choice(self.players)
        player.giveTurn()
        self.currTurn = player

    def updateTurn(self):
        if self.currTurnLoc.name not in FREESPACES:
            self.currTurnLoc.show = True

        self.currTurn.removeTurn()
        
        if self.currTurn.id < len(self.players) - 1:
            self.currTurn = self.players[self.currTurn.id + 1]
        else: 
            self.currTurn = self.players[0]
        
        self.currTurn.giveTurn()

        self.currTurnLoc = self.boardSpaces.properties[self.currTurn.location[0]]

        self.currTurnLoc.show = False
        
        self.diceRolled = False
        self.displayDice = self.doDisplayDice()

        if self.currTurn.isBankrupt:
            self.updateTurn(self)

    def start(self):
        self.startupWindow.isStartup = False
        self.pickStartTurn()
        self.currTurnLoc = self.boardSpaces.properties[self.currTurn.location[0]]

    def doDisplayDice(self):
        if self.currTurn != None:
            if self.diceRolled:
                return False
            elif self.currTurn.inJail or self.currTurn.location[0] == "Go":
                return True
            elif self.currTurnLoc.show:
                return False
            else:
                return True

    def sendToJail(self, player):
        player.sendToJail()
        self.diceRolled = True
        self.currTurnLoc.show = False

    #Controls all displays to screen
    def display(self):
        #Fill background color
        self.screen.fill(GREEN)

        #Display each players properties
        for player in self.players:
            player.displayProperties()

        #Display the board and dice
        self.board.display()
        self.diceSet.display()

        #Display each player
        for player in self.players:
            player.playerBanner.draw()
            player.playerPiece.draw()

        #Display startup window if needed 
        if self.startupWindow.isStartup:
            self.startupWindow.display()

        if self.currTurn != None:
            self.buildMenu.display(self.players, self.currTurn)
            self.tradeMenu.display(self.players, self.currTurn)

        #Display auction if running
        for prop in self.boardSpaces.properties.values():
            if isinstance(prop, Property):
                if prop.auction != None and prop.auction.isRunning:
                    prop.auction.display()

        #Next Turn Button
        if self.diceRolled and not self.currTurnLoc.show:
            self.nxtTurnBtn.draw()

        #Buy Property Window (Only displays when certain conditions met)
        self.displayWin()
        
        #Update pygame display
        pygame.display.flip()