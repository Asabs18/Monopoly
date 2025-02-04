import pygame

from  Assets.numAssets.displayAssets import *

pygame.init()


#Default TODO: MAKE FONTS SCALE BY SCREEN SIZE

try:
    name_font = pygame.font.Font("Assets\\fontAssets\\QueensidesMedium-x30zV.ttf", 60)  # Specify the path to the .ttf file and font size
    money_font = pygame.font.Font("Assets\\fontAssets\\Nasa21-l23X.ttf", 30)  # Specify the path to the .ttf file and font size
    piece_font = pygame.font.Font("Assets\\fontAssets\\QueensidesMedium-x30zV.ttf", 30)  # Specify the path to the .ttf file and font size
    startup_win_font = pygame.font.Font("Assets\\fontAssets\\QueensidesMedium-x30zV.ttf", 40)  # Specify the path to the .ttf file and font size
    button_font = piece_font # Specify the path to the .ttf file and font size
    inbox_font = pygame.font.Font(None, 38) # Specify the path to the .ttf file and font size
    name_label_font = money_font
    prop_name_font = pygame.font.Font("Assets\\fontAssets\\QueensidesMedium-x30zV.ttf", 34)
    prop_txt_font = pygame.font.Font("Assets\\fontAssets\\Nasa21-l23X.ttf", 26)
except FileNotFoundError:
    name_font = pygame.font.Font(None, 60)
    money_font = pygame.font.Font(None, 30)
    piece_font = pygame.font.Font(None, 30)
    startup_win_font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 32)
    inbox_font = pygame.font.Font(None, 38)
    name_label_font = pygame.font.Font(None, 30)
    prop_name_font = pygame.font.Font(None, 34)
    prop_txt_font = pygame.font.Font(None, 26)
    print("Font file not found. Using default font.")

NAMEFONT = name_font
MONEYFONT = money_font
PIECEFONT = piece_font
STARTUPFONT = startup_win_font
BTNFONT = button_font
INBOXFONT = inbox_font
NAMELABELFONT = name_label_font
PROPNAMEFONT = prop_name_font
PROPTXTFONT = prop_txt_font
