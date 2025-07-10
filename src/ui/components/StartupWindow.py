import pygame

from src.config.displayAssets import *
from src.config.colorAssets import *
from src.config.imgAssets import *
from src.config.fontAssets import *
from src.config.gameAssets import *
from src.ui.components.Button import Button
from src.ui.components.InputBox import TextBox


pygame.init()

class StartupWindow:
    def __init__(self, screen, pieces):
        self.screen = screen
        
        #Display startup window at start
        self.isStartup = True

        #Define ui components
        self.closeBtn = Button(self.screen, "Close", BTNFONT, (CLOSE_BTN_X, CLOSE_BTN_Y, CLOSE_BTN_WIDTH, CLOSE_BTN_HEIGHT), RED)
        self.addBtn = Button(self.screen, "Add", BTNFONT, (ADD_PLAYER_BTN_X, ADD_PLAYER_BTN_Y, ADD_PLAYER_BTN_WIDTH, ADD_PLAYER_BTN_HEIGHT), GREEN)
        self.nameInputBox = TextBox((NAME_INPUT_X, NAME_INPUT_Y, NAME_INPUT_WIDTH, NAME_INPUT_HEIGHT))
        
        #Define Piece array
        self.PieceImages = pieces

        self.selectedPiece = None

    #Display entire startup window
    def display(self):          
        #Startup Window
        pygame.draw.rect(self.screen, BLACK, (START_WIN_X - 5, START_WIN_Y - 5, START_WIN_WIDTH + 10, START_WIN_HEIGHT + 10))
        pygame.draw.rect(self.screen, DARK_GRAY, (START_WIN_X, START_WIN_Y, START_WIN_WIDTH, START_WIN_HEIGHT))

        #Window Title
        textSurface = STARTUPFONT.render("Add Players", True, WHITE)
        textRect = textSurface.get_rect()
        textRect.center = (START_WIN_TITLE_X, START_WIN_TITLE_Y)
        self.screen.blit(textSurface, textRect)

        #Name Label
        textSurface = NAMELABELFONT.render("Name:", True, WHITE)
        textRect = textSurface.get_rect()
        textRect.center = (NAME_LABEL_X, NAME_LABEL_Y)
        self.screen.blit(textSurface, textRect)

        #Name Input Box
        self.nameInputBox.update()
        self.nameInputBox.draw(self.screen)

        #Pieces
        self.drawPieces()

        #Add Player Button
        self.addBtn.draw()

        #Close Button
        self.closeBtn.draw()

    #Draw all pieces left in Piece array 
    def drawPieces(self):
        for i, img in enumerate(self.PieceImages):
            if img != None:
                #Calculate current piece x coord
                currX = (ST_PIECE_X + (i * (ST_PIECE_WIDTH + ST_PIECE_OFFSET))) - (len(self.PieceImages) * (ST_PIECE_WIDTH + ST_PIECE_OFFSET) // 2) + ST_PIECE_OFFSET
                
                #Draw highlight if piece selected
                if self.selectedPiece == i:
                    pygame.draw.rect(self.screen, BLACK, (currX - 10, ST_PIECE_Y - 10, ST_PIECE_WIDTH + 20, ST_PIECE_HEIGHT + 20))
                    pygame.draw.rect(self.screen, WHITE, (currX - 5, ST_PIECE_Y - 5, ST_PIECE_WIDTH + 10, ST_PIECE_HEIGHT + 10))
                
                #Draw image to screen
                self.screen.blit(img, (currX, ST_PIECE_Y))

    #Handles piece click event for startup window 
    def isPieceClicked(self, pos):
        for i, img in enumerate(self.PieceImages):
            if img != None: 
                #Calculates current piece x Coord
                currX = (ST_PIECE_X + (i * (ST_PIECE_WIDTH + ST_PIECE_OFFSET))) - (len(self.PieceImages) * (ST_PIECE_WIDTH + ST_PIECE_OFFSET) // 2) + ST_PIECE_OFFSET
                
                #If click on current piece rect return its index
                if pygame.Rect(currX, ST_PIECE_Y, ST_PIECE_WIDTH, ST_PIECE_HEIGHT).collidepoint(pos):
                    return i
        #If no piece is clicked keep current selected piece
        return self.selectedPiece

