"""
Monopoly Game Card System Module

This module implements the card system for Chance and Community Chest spaces
in the Monopoly board game. It provides abstract base classes for cards and decks,
with concrete implementations for both card types and their associated actions.

Author: Aidan Sabatini
"""

# Standard library imports
import random
from abc import ABC, abstractmethod
from typing import List, Union

# Third-party imports
import pygame

# Local application imports
from src.config.boardAssets import CHANCE_CARDS, COM_CHEST_CARDS
from src.config.displayAssets import *
from src.ui.components.Button import Button
from src.ui.components.Helper import *
from src.ui.components.CardActions import ChanceActions, ComChestActions

# Initialize Pygame
pygame.init()


class Card(ABC):
    """
    Abstract base class for all game cards.
    
    This class defines the common interface that all card types must implement.
    Cards represent the various Chance and Community Chest cards that players
    can draw during gameplay, each with unique effects and descriptions.
    
    Attributes:
        screen (pygame.Surface): The game display surface
        card_id (int): Unique identifier for this specific card
        description (str): Text description of the card's effect
        actions: Object containing the logic for executing card effects
    """
    
    def __init__(self, screen: pygame.Surface, card_id: int) -> None:
        """
        Initialize a card with basic properties.
        
        Args:
            screen: The pygame surface for rendering
            card_id: Unique identifier for this card type
        """
        self.screen = screen
        self.card_id = card_id
        self.description: str = ""
        self.actions = None
    
    @abstractmethod
    def execute_action(self, players: List) -> None:
        """
        Execute the card's effect on the game state.
        
        This method must be implemented by all concrete card types to define
        their specific gameplay effects.
        
        Args:
            players: List of all players in the game
        """
        pass


class ChanceCard(Card):
    """
    Represents a Chance card with specific game effects.
    
    Chance cards typically involve movement, money transactions, or special
    actions that can significantly impact gameplay. These cards are drawn
    when a player lands on a Chance space.
    
    Attributes:
        description (str): The text displayed on the card
        actions (ChanceActions): Handler for executing chance card effects
    """
    
    def __init__(self, screen: pygame.Surface, card_id: int) -> None:
        """
        Initialize a Chance card with its description and action handler.
        
        Args:
            screen: The pygame surface for rendering
            card_id: Index into the CHANCE_CARDS list for this card's description
        """
        super().__init__(screen, card_id)
        self.description = CHANCE_CARDS[card_id]
        self.actions = ChanceActions()
    
    def execute_action(self, players: List) -> None:
        """
        Execute this Chance card's specific effect.
        
        Args:
            players: List of all players in the game
        """
        self.actions.doAction(players, self.card_id)
    
    # Legacy method name for backward compatibility
    def action(self, players: List) -> None:
        """Legacy method name - use execute_action() instead."""
        self.execute_action(players)


class CommunityChestCard(Card):
    """
    Represents a Community Chest card with specific game effects.
    
    Community Chest cards often involve community-based actions like
    collecting money from other players, paying fees, or receiving
    rewards. These cards are drawn when landing on Community Chest spaces.
    
    Attributes:
        description (str): The text displayed on the card
        actions (ComChestActions): Handler for executing community chest effects
    """
    
    def __init__(self, screen: pygame.Surface, card_id: int) -> None:
        """
        Initialize a Community Chest card with its description and action handler.
        
        Args:
            screen: The pygame surface for rendering
            card_id: Index into the COM_CHEST_CARDS list for this card's description
        """
        super().__init__(screen, card_id)
        self.description = COM_CHEST_CARDS[card_id]
        self.actions = ComChestActions()
    
    def execute_action(self, players: List) -> None:
        """
        Execute this Community Chest card's specific effect.
        
        Args:
            players: List of all players in the game
        """
        self.actions.doAction(players, self.card_id)
    
    # Legacy method name for backward compatibility
    def action(self, players: List) -> None:
        """Legacy method name - use execute_action() instead."""
        self.execute_action(players)


class Deck(ABC):
    """
    Abstract base class for card decks.
    
    This class defines the common behavior for managing collections of cards,
    including shuffling, dealing, and deck management. When a deck runs out,
    it automatically recreates and reshuffles itself.
    
    Attributes:
        screen (pygame.Surface): The game display surface
        deck (List[Card]): The current collection of cards in the deck
        current_card (Card): The most recently dealt card
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize an empty deck.
        
        Args:
            screen: The pygame surface for rendering
        """
        self.screen = screen
        self.deck: List[Card] = []
        self.current_card: Union[Card, None] = None
    
    @abstractmethod
    def _initialize_deck(self) -> None:
        """
        Create and populate the deck with appropriate cards.
        
        This method must be implemented by concrete deck classes to define
        what types of cards belong in the deck.
        """
        pass
    
    @abstractmethod
    def _create_fresh_deck(self) -> List[Card]:
        """
        Create a new full deck of cards.
        
        Returns:
            A new list containing all cards for this deck type
        """
        pass
    
    def shuffle_deck(self) -> None:
        """
        Randomly shuffle the current deck.
        
        This method uses Python's random.shuffle to randomize the order
        of cards in the deck, ensuring unpredictable card draws.
        """
        random.shuffle(self.deck)
    
    def _draw_card(self) -> Card:
        """
        Draw a single card from the deck.
        
        If the deck is empty, it automatically creates a new shuffled deck
        before drawing. This ensures the deck never truly runs out of cards.
        
        Returns:
            The card drawn from the top of the deck
        """
        if len(self.deck) == 0:
            self.deck = self._create_fresh_deck()
            self.shuffle_deck()
        
        return self.deck.pop()
    
    def deal_card(self) -> Card:
        """
        Deal a card and set it as the current card.
        
        This method draws a new card from the deck and stores it as the
        current card for easy access by the game system.
        
        Returns:
            The newly dealt card
        """
        self.current_card = self._draw_card()
        return self.current_card
    
    # Legacy method names for backward compatibility
    def shuffle(self) -> None:
        """Legacy method name - use shuffle_deck() instead."""
        self.shuffle_deck()
    
    def getNewCard(self) -> Card:
        """Legacy method name - use _draw_card() instead."""
        return self._draw_card()
    
    def deal(self) -> Card:
        """Legacy method name - use deal_card() instead."""
        return self.deal_card()


class ChanceDeck(Deck):
    """
    Manages the deck of Chance cards.
    
    This deck contains all available Chance cards and handles their distribution
    during gameplay. The deck automatically reshuffles when empty to ensure
    continuous availability of cards.
    
    Attributes:
        deck (List[ChanceCard]): Collection of Chance cards
        current_card (ChanceCard): The most recently dealt Chance card
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize the Chance deck with all available cards.
        
        Args:
            screen: The pygame surface for rendering
        """
        super().__init__(screen)
        self._initialize_deck()
        self.current_card = self.deal_card()
    
    def _initialize_deck(self) -> None:
        """Create and shuffle the initial Chance deck."""
        self.deck = self._create_fresh_deck()
        self.shuffle_deck()
    
    def _create_fresh_deck(self) -> List[ChanceCard]:
        """
        Create a complete set of Chance cards.
        
        Returns:
            List containing one of each available Chance card
        """
        fresh_deck = []
        for i in range(len(CHANCE_CARDS)):
            fresh_deck.append(ChanceCard(self.screen, i))
        return fresh_deck
    
    # Legacy method name for backward compatibility
    def initDeck(self) -> None:
        """Legacy method name - use _initialize_deck() instead."""
        self._initialize_deck()


class CommunityChestDeck(Deck):
    """
    Manages the deck of Community Chest cards.
    
    This deck contains all available Community Chest cards and handles their
    distribution during gameplay. Like the Chance deck, it automatically
    reshuffles when empty to maintain card availability.
    
    Attributes:
        deck (List[CommunityChestCard]): Collection of Community Chest cards  
        current_card (CommunityChestCard): The most recently dealt Community Chest card
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize the Community Chest deck with all available cards.
        
        Args:
            screen: The pygame surface for rendering
        """
        super().__init__(screen)
        self._initialize_deck()
        self.current_card = self.deal_card()
    
    def _initialize_deck(self) -> None:
        """Create and shuffle the initial Community Chest deck."""
        self.deck = self._create_fresh_deck()
        self.shuffle_deck()
    
    def _create_fresh_deck(self) -> List[CommunityChestCard]:
        """
        Create a complete set of Community Chest cards.
        
        Returns:
            List containing one of each available Community Chest card
        """
        fresh_deck = []
        for i in range(len(COM_CHEST_CARDS)):
            fresh_deck.append(CommunityChestCard(self.screen, i))
        return fresh_deck
    
    # Legacy method name for backward compatibility
    def initDeck(self) -> None:
        """Legacy method name - use _initialize_deck() instead."""
        self._initialize_deck()


# Legacy class name for backward compatibility
class ComChestCard(CommunityChestCard):
    """Legacy class name - use CommunityChestCard instead."""
    pass


class ComChestDeck(CommunityChestDeck):
    """Legacy class name - use CommunityChestDeck instead."""
    pass