"""
Monopoly Game Auction System Module

This module implements the property auction system for the Monopoly board game.
When a player lands on an unowned property and chooses not to buy it, or when
bankruptcy requires asset liquidation, properties go to auction where all players
can bid competitively.

Author: Aidan Sabatini
"""

# Standard library imports
from typing import List, Tuple, Optional, Union, Any

# Third-party imports
import pygame

# Local application imports
from src.config.colorAssets import BLACK, WHITE, GREEN, RED, LIGHT_GREEN
from src.config.displayAssets import (
    START_WIN_X, START_WIN_Y, START_WIN_WIDTH, START_WIN_HEIGHT,
    START_WIN_TITLE_X, START_WIN_TITLE_Y, BID_BTN_X, BID_BTN_Y,
    WITHDRAW_BTN_X, WITHDRAW_BTN_Y, AUC_BTN_WIDTH, AUC_BTN_HEIGHT,
    PLAYER_BID_X, PLAYER_BID_Y, ASKING_BID_X, ASKING_BID_Y,
    AUC_CARD_X, AUC_CARD_Y, AUC_CARD_WIDTH, AUC_CARD_HEIGHT,
    AUC_NAME_LINE_START, AUC_NAME_LINE_END, AUC_TURN_IND_OFFSET,
    AUC_TURN_IND_RAD, AUC_TURN_IND_WIDTH
)
from src.config.fontAssets import PROPNAMEFONT, PIECEFONT
from src.ui.components.Button import Button
from src.ui.components.Helper import drawText

# Initialize Pygame
pygame.init()


class Auction:
    """
    Manages property auctions in the Monopoly game.
    
    This class handles the auction process when properties go up for competitive
    bidding. It manages player turns, bid tracking, UI display, and determines
    the winning bidder. The auction continues until only one active bidder remains.
    
    Attributes:
        screen (pygame.Surface): The game display surface
        is_running (bool): Whether the auction is currently active
        players (List[Tuple[Any, Optional[int]]]): Players and their current bids
        property (Property): The property being auctioned
        current_price (int): The current highest bid amount
        next_bid (int): The minimum next bid amount
        current_turn (Tuple[Player, Optional[int]]): The player whose turn it is to bid
        bid_button (Button): Button for placing bids
        withdraw_button (Button): Button for withdrawing from auction
    """
    
    # Auction constants
    MINIMUM_BID_INCREMENT = 10  # Minimum amount to increase bid by
    PLAYER_DISPLAY_SPACING = 80  # Vertical spacing between player displays
    TURN_INDICATOR_BORDER = 2    # Border width for turn indicator
    
    def __init__(self, screen: pygame.Surface, players: List[Any], property_obj: Any) -> None:
        """
        Initialize a new auction.
        
        Args:
            screen: The pygame surface to render the auction on
            players: List of all players who can participate in the auction
            property_obj: The property being auctioned
        """
        self.screen = screen
        self.is_running = False
        
        # Initialize player bid tracking - all players start with no bid (None)
        self.players: List[Tuple[Any, Optional[int]]] = [(player, None) for player in players]
        
        self.property = property_obj
        self.current_price = 0
        self.next_bid = self.current_price + self.MINIMUM_BID_INCREMENT
        
        # Auctions always start with the first player
        self.current_turn = self.players[0]
        
        # Initialize UI components
        self._initialize_buttons()
    
    def _initialize_buttons(self) -> None:
        """Initialize the auction interface buttons."""
        bid_button_rect = (BID_BTN_X, BID_BTN_Y, AUC_BTN_WIDTH, AUC_BTN_HEIGHT)
        withdraw_button_rect = (WITHDRAW_BTN_X, WITHDRAW_BTN_Y, AUC_BTN_WIDTH, AUC_BTN_HEIGHT)
        
        self.bid_button = Button(
            self.screen, "Bid", PIECEFONT, bid_button_rect, GREEN
        )
        self.withdraw_button = Button(
            self.screen, "Withdraw", PIECEFONT, withdraw_button_rect, RED
        )
    
    def start_auction(self) -> None:
        """
        Begin the auction process.
        
        This method activates the auction, making it visible and interactive.
        All eligible players can now participate in the bidding process.
        """
        self.is_running = True
    
    def display(self) -> None:
        """
        Render the auction interface to the screen.
        
        This method draws all auction elements including the window background,
        title, property card, player bids, current asking price, and action buttons.
        Only renders when the auction is active.
        """
        if not self.is_running:
            return
        
        self._draw_auction_window()
        self._draw_title_and_divider()
        self._draw_action_buttons()
        self._draw_player_bids()
        self._draw_asking_price()
        self._draw_property_card()
    
    def _draw_auction_window(self) -> None:
        """Draw the main auction window background."""
        # Draw border
        border_rect = (
            START_WIN_X - 5, START_WIN_Y - 5,
            START_WIN_WIDTH + 10, START_WIN_HEIGHT + 10
        )
        pygame.draw.rect(self.screen, BLACK, border_rect)
        
        # Draw main window
        main_rect = (START_WIN_X, START_WIN_Y, START_WIN_WIDTH, START_WIN_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, main_rect)
    
    def _draw_title_and_divider(self) -> None:
        """Draw the auction title and decorative line."""
        drawText(
            self.screen, "Auction", PROPNAMEFONT, BLACK,
            (START_WIN_TITLE_X, START_WIN_TITLE_Y)
        )
        pygame.draw.line(
            self.screen, BLACK, AUC_NAME_LINE_START, AUC_NAME_LINE_END, 2
        )
    
    def _draw_action_buttons(self) -> None:
        """Draw the bid and withdraw buttons."""
        self.bid_button.draw()
        self.withdraw_button.draw()
    
    def _draw_player_bids(self) -> None:
        """
        Draw all player bids and indicate whose turn it is.
        
        Only shows players who are still active in the auction (haven't withdrawn).
        The current player's turn is indicated with a colored circle.
        """
        for i, (player, bid) in enumerate(self.players):
            if bid is not None:  # Only show active players
                bid_text = f"{player.name}'s bid: ${bid}"
                bid_position = (
                    PLAYER_BID_X, 
                    PLAYER_BID_Y + (i * self.PLAYER_DISPLAY_SPACING)
                )
                
                drawText(self.screen, bid_text, PIECEFONT, BLACK, bid_position)
                
                # Draw turn indicator for current player
                if self.current_turn == (player, bid):
                    self._draw_turn_indicator(bid_position)
    
    def _draw_turn_indicator(self, position: Tuple[int, int]) -> None:
        """
        Draw a circular indicator showing whose turn it is.
        
        Args:
            position: The (x, y) position where the indicator should be drawn
        """
        indicator_center = (
            position[0] - AUC_TURN_IND_OFFSET, 
            position[1]
        )
        
        # Draw border circle
        pygame.draw.circle(
            self.screen, BLACK, indicator_center,
            round(AUC_TURN_IND_RAD + self.TURN_INDICATOR_BORDER),
            round(AUC_TURN_IND_WIDTH + self.TURN_INDICATOR_BORDER)
        )
        
        # Draw main indicator circle
        pygame.draw.circle(
            self.screen, LIGHT_GREEN, indicator_center,
            round(AUC_TURN_IND_RAD), round(AUC_TURN_IND_WIDTH)
        )
    
    def _draw_asking_price(self) -> None:
        """Draw the current asking bid amount."""
        asking_text = f"Asking: ${self.next_bid}"
        drawText(
            self.screen, asking_text, PROPNAMEFONT, BLACK,
            (ASKING_BID_X, ASKING_BID_Y)
        )
    
    def _draw_property_card(self) -> None:
        """Draw the property card being auctioned."""
        self.property.smallCard(
            AUC_CARD_X, AUC_CARD_Y, AUC_CARD_WIDTH, AUC_CARD_HEIGHT
        )
    
    def place_bid(self) -> None:
        """
        Handle a bid placement by the current player.
        
        This method records the current player's bid at the asking price,
        increases the minimum next bid, and advances to the next player's turn.
        """
        # Update the current player's bid
        player = self.current_turn[0]
        self.players[player.id] = (player, self.next_bid)
        
        # Update price tracking
        self.current_price = self.next_bid
        self.next_bid += self.MINIMUM_BID_INCREMENT
        
        # Move to next player
        self._advance_turn()
    
    def withdraw_from_auction(self) -> None:
        """
        Handle a player withdrawing from the auction.
        
        This method removes the current player from active bidding by setting
        their bid to None, then advances to the next active player.
        """
        # Mark current player as withdrawn
        player = self.current_turn[0]
        self.players[player.id] = (player, None)
        
        # Move to next player
        self._advance_turn()
    
    def _advance_turn(self) -> None:
        """
        Advance to the next active player's turn.
        
        If only one or fewer players remain active, the auction ends.
        Otherwise, cycles through players until finding the next active bidder.
        """
        # Check if auction should end
        if self._get_active_player_count() <= 1:
            self._end_auction()
            return
        
        # Find next active player
        self._find_next_active_player()
    
    def _find_next_active_player(self) -> None:
        """
        Find and set the next active player as the current turn.
        
        Cycles through all players until finding one who hasn't withdrawn.
        """
        player_found = False
        
        while not player_found:
            # Move to next player (with wraparound)
            current_player_id = self.current_turn[0].id
            next_player_id = (current_player_id + 1) % len(self.players)
            self.current_turn = self.players[next_player_id]
            
            # Check if this player is still active
            if self.current_turn[1] is not None:
                player_found = True
    
    def _end_auction(self) -> None:
        """
        End the auction and sell the property to the highest bidder.
        
        This method stops the auction, determines the winner, and processes
        the property sale at the winning bid amount.
        """
        self.is_running = False
        self._sell_property_to_winner()
    
    def _sell_property_to_winner(self) -> None:
        """Sell the property to the auction winner at their bid price."""
        winning_bidder = self._get_highest_bidder()
        if winning_bidder[0] is not None:  # Ensure there is a winner
            self.property.buyAuc(winning_bidder[0], winning_bidder[1])
    
    def _get_highest_bidder(self) -> Tuple[Optional[Any], int]:
        """
        Determine the player with the highest bid.
        
        Returns:
            Tuple containing the winning player and their bid amount.
            Returns (None, -1) if no valid bids exist.
        """
        highest_bidder = (None, -1)
        
        for player, bid in self.players:
            if bid is not None and bid > highest_bidder[1]:
                highest_bidder = (player, bid)
        
        return highest_bidder
    
    def _get_active_player_count(self) -> int:
        """
        Count the number of players still active in the auction.
        
        Returns:
            int: The number of players who haven't withdrawn (bid is not None)
        """
        return sum(1 for _, bid in self.players if bid is not None)
    
    # Public methods for external access (used by button click handlers)
    def bidBtnAction(self) -> None:
        """Public interface for bid button clicks."""
        self.place_bid()
    
    def withdrawBtnAction(self) -> None:
        """Public interface for withdraw button clicks."""
        self.withdraw_from_auction()
    
    # Legacy method names for backward compatibility
    def start(self) -> None:
        """Legacy method name - use start_auction() instead."""
        self.start_auction()
    
    def updateTurn(self) -> None:
        """Legacy method name - use _advance_turn() instead."""
        self._advance_turn()
    
    def sellProperty(self) -> None:
        """Legacy method name - use _sell_property_to_winner() instead."""
        self._sell_property_to_winner()
    
    def getHighestBidder(self) -> Tuple[Optional[Any], int]:
        """Legacy method name - use _get_highest_bidder() instead."""
        return self._get_highest_bidder()
    
    def getNumActivePlayers(self) -> int:
        """Legacy method name - use _get_active_player_count() instead."""
        return self._get_active_player_count()
