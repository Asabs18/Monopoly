import pygame

from src.config.displayAssets import *
from src.config.imgAssets import *

from enum import Enum
from random import randint
from time import sleep

pygame.init()

#Enum to define each die side as num
class Side(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SiX = 6

#Class to represent one Die
class Dice:
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y

        self.screen = screen

        self.side = self.getRandomSide()
        
        self.die_images = DIEIMGS
        self.image = self.getImage()

    #Get random side of die (1-6)
    def getRandomSide(self):
        return Side(randint(1, 6))

    def getValue(self):
        return self.side.value

    #Display proper image of die to screen
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    #Get correct image of die based on side
    def getImage(self):
        return self.die_images[self.side.value - 1]

    #Update die by getting new random side and corresponding image
    def update(self):
        self.side = self.getRandomSide()
        self.image = self.getImage()


#Class to hold two Dice() and display them
class DiceSet:
    #Creates two Dice() and sets displayed to false
    def __init__(self, screen):
        self.dice = [Dice(screen, DICE_X1, DICE_Y1), Dice(screen, DICE_X2, DICE_Y2)]
        self.screen = screen
        self.isDisplayed = False

    #If dice set should be displayed draw each die to the screen
    def display(self):
        if self.isDisplayed:
            for die in self.dice:
                die.display()
    
    #Roll both Dice a certain amount of times if dice are displayed and
    #updates display each time to make animation 
    #(SLEEPS PROGRAM UNTIL DONE!!!)
    def roll(self):
        if self.isDisplayed:
            for _ in range(randint(ROLL_RANGEL, ROLL_RANGEH)):
                for die in self.dice:
                    self.update()
                    self.display()
                    pygame.display.flip()
                    sleep(0.01)
        
        return sum([die.side.value for die in self.dice])

    def getValue(self):
        return sum([die.side.value for die in self.dice])

    def isDouble(self):
        return self.dice[0].side == self.dice[1].side

    #updates each die to a new side
    def update(self):
        for die in self.dice:
            die.update()

    #Turns on and off display of dice
    def on(self):
        self.isDisplayed = True

    def off(self):
        self.isDisplayed = False
    
    def toggle(self):
        self.isDisplayed = not self.isDisplayed