import pygame, random

from abc import ABC, abstractmethod

from Assets.numAssets.boardAssets import *
from Assets.numAssets.displayAssets import *
from Assets.uiAssets.Button import *
from Assets.uiAssets.Helper import *
from Assets.uiAssets.CardActions import *

pygame.init()

class Card(ABC):
    def __init__(self, screen, id):
        self.screen = screen

        self.id = id

class ChanceCard(Card):
    def __init__(self, screen, id):
        super().__init__(screen, id)

        self.description = CHANCE_CARDS[id]
        self.actions = ChanceActions()

    def action(self, players):
        self.actions.doAction(players, self.id)

class ComChestCard(Card):
    def __init__(self, screen, id):
        super().__init__(screen, id)

        self.description = COM_CHEST_CARDS[id]
        self.actions = ComChestActions()

    def action(self, players):
        self.actions.doAction(players, self.id)



class Deck(ABC):
    def __init__(self, screen):
        self.screen = screen

        self.deck = []

    @abstractmethod
    def initDeck(self):
        pass

    def shuffle(self):
        random.shuffle(self.deck)

    def getNewCard(self):
        if len(self.deck) == 0:
            self.deck = self.createDeck()

        return self.deck.pop()

    def deal(self):
        self.currCard = self.getNewCard()
        return self.currCard

class ChanceDeck(Deck):
    def __init__(self, screen):
        super().__init__(screen)

        self.initDeck()

        self.currCard = self.getNewCard()

    def initDeck(self):
        for i in range(len(CHANCE_CARDS)):
            self.deck.append(ChanceCard(self.screen, i))

        self.shuffle()

class ComChestDeck(Deck):
    def __init__(self, screen):
        super().__init__(screen)

        self.initDeck()

        self.currCard = self.getNewCard()

    def initDeck(self):
        for i in range(len(COM_CHEST_CARDS)):
            self.deck.append(ComChestCard(self.screen, i))

        self.shuffle()