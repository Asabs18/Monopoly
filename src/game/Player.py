"""
Monopoly Game Player System Module

This module implements the player management system for the Monopoly board game.
It handles player state, movement, property ownership, money management, building
construction, jail mechanics, and bankruptcy procedures.

Author: Aidan Sabatini
"""

# Standard library imports
from typing import List, Dict, Optional, Tuple, Union

# Third-party imports
import pygame
import pygame.gfxdraw

# Local application imports
from src.game.Properties import ColorSet
from src.config.displayAssets import (
    PROP_TAG_WIDTH, PROP_TAG_HEIGHT, NUM_CELLS, PIECE_WIDTH, PIECE_HEIGHT
)
from src.config.colorAssets import (
    RED, BLUE, LIGHT_GREEN, DARK_YELLOW, BROWN, LIGHT_BLUE, PURPLE, 
    ORANGE, YELLOW, GREEN, DARK_BLUE
)
from src.config.fontAssets import *
from src.config.gameAssets import PIECES
from src.config.boardAssets import TRACK, BOARDCOORDS
from src.config.imgAssets import PIECE_IMGS
from src.ui.components.PlayerBanner import PlayerBanner
from src.ui.components.Helper import draw_rounded_rect

# Initialize Pygame
pygame.init()


class Player:
    """
    Represents a player in the Monopoly game.
    
    This class manages all aspects of a player's game state including their position
    on the board, financial status, property ownership, building inventory, and
    special conditions like jail status. It handles movement, transactions, and
    interactions with the game board.
    
    Attributes:
        screen (pygame.Surface): The game display surface
        name (str): The player's display name
        player_id (int): Unique identifier for this player (0-3)
        color (tuple): RGB color tuple representing this player
        piece_name (str): Name of the game piece this player uses
        location (Tuple[str, int]): Current board position (space_name, index)
        money (int): Current amount of money the player has
        get_out_of_jail_cards (int): Number of "Get Out of Jail Free" cards owned
        properties (List): List of properties owned by this player
        buildings (Dict): Dictionary mapping properties to number of buildings
        is_current_turn (bool): Whether it's currently this player's turn
        is_in_jail (bool): Whether the player is currently in jail
        jail_turn_count (int): Number of turns spent in jail
        is_bankrupt (bool): Whether the player has gone bankrupt
        player_banner (PlayerBanner): UI component showing player info
        player_piece (PlayerPiece): Visual representation on the board
    """
    
    # Game constants
    STARTING_MONEY = 1500
    PASS_GO_BONUS = 200
    JAIL_POSITION = ("In Jail", 10)
    GO_POSITION = ("Go", 0)
    BAIL_AMOUNT = 50
    MAX_JAIL_TURNS = 2
    BOARD_SIZE = 40
    
    # Color assignments for players
    PLAYER_COLORS = {
        0: RED,
        1: BLUE, 
        2: LIGHT_GREEN,
        3: DARK_YELLOW
    }
    
    # Color set requirements for monopolies
    COLOR_SET_REQUIREMENTS = {
        BROWN: 2, LIGHT_BLUE: 3, PURPLE: 3, ORANGE: 3,
        RED: 3, YELLOW: 3, GREEN: 3, DARK_BLUE: 2
    }
    
    def __init__(self, screen: pygame.Surface, name: str, player_id: int, piece: int) -> None:
        """
        Initialize a new player with starting conditions.
        
        Args:
            screen: The pygame surface for rendering
            name: The player's display name
            player_id: Unique identifier (0-3)
            piece: Index of the piece type to use
        """
        self.screen = screen
        self.name = name
        self.player_id = player_id
        self.color = self._get_player_color()
        self.piece_name = PIECES[piece]
        
        # Initialize game state
        self.location = self.GO_POSITION
        self.money = self.STARTING_MONEY
        self.get_out_of_jail_cards = 0
        self.properties: List = []
        self.buildings: Dict = {}
        
        # Initialize status flags
        self.is_current_turn = False
        self.is_in_jail = False
        self.jail_turn_count = 0
        self.is_bankrupt = False
        
        # Initialize UI components
        self.player_banner = PlayerBanner(screen, self)
        self.player_piece = PlayerPiece(screen, self)
    
    def _get_player_color(self) -> Tuple[int, int, int]:
        """
        Get the color associated with this player's ID.
        
        Returns:
            RGB color tuple for this player
        """
        return self.PLAYER_COLORS.get(self.player_id, RED)
    
    def move_by_spaces(self, num_spaces: int) -> None:
        """
        Move the player a specified number of spaces forward.
        
        This method handles board wraparound and awards money for passing Go.
        It updates both the player's logical position and visual representation.
        
        Args:
            num_spaces: Number of spaces to move forward
        """
        self._update_board_position(num_spaces)
        self.player_piece.update_position()
    
    def move_to_space(self, target_position: int) -> None:
        """
        Move the player directly to a specific board position.
        
        This method calculates the shortest path to the target, handling
        board wraparound and Go bonuses appropriately.
        
        Args:
            target_position: Board index to move to (0-39)
        """
        current_position = self.location[1]
        
        if current_position > target_position:
            # Need to go around the board
            spaces_to_move = (self.BOARD_SIZE - current_position) + target_position
        else:
            # Direct movement forward
            spaces_to_move = target_position - current_position
        
        self.move_by_spaces(spaces_to_move)
    
    def _update_board_position(self, spaces: int) -> None:
        """
        Update the player's position on the board.
        
        Handles board wraparound and awards Go bonuses when appropriate.
        
        Args:
            spaces: Number of spaces to move
        """
        current_index = self.location[1]
        new_index = (current_index + spaces) % len(TRACK)
        
        # Award money for passing or landing on Go
        if spaces > 0 and (current_index + spaces >= len(TRACK) or new_index == 0):
            self.receive_money(self.PASS_GO_BONUS)
        
        # Update location
        new_space_name = TRACK[new_index]
        self.location = (new_space_name, new_index)
    
    def render_property_ownership(self) -> None:
        """
        Render visual indicators showing which properties this player owns.
        
        This method draws colored rectangles on the board to indicate
        property ownership, with different orientations for different
        sides of the board.
        """
        for property_obj in self.properties:
            if hasattr(property_obj, 'tagPos') and hasattr(property_obj, 'isTagHorz'):
                if property_obj.isTagHorz:
                    rect = (
                        property_obj.tagPos[0], property_obj.tagPos[1],
                        PROP_TAG_WIDTH, PROP_TAG_HEIGHT
                    )
                else:
                    rect = (
                        property_obj.tagPos[0], property_obj.tagPos[1],
                        PROP_TAG_HEIGHT, PROP_TAG_WIDTH
                    )
                
                draw_rounded_rect(self.screen, self.color, rect, 5)
    
    def send_to_jail(self) -> None:
        """
        Send this player to jail.
        
        Updates the player's position to the jail space and sets jail status.
        Resets any previous jail turn counting.
        """
        self.is_in_jail = True
        self.jail_turn_count = 0
        self.location = self.JAIL_POSITION
        self.player_piece.update_position()
    
    def handle_jail_turn(self, dice_set) -> None:
        """
        Process a turn while the player is in jail.
        
        The player can escape jail by rolling doubles, paying bail after
        maximum turns, or using a Get Out of Jail Free card.
        
        Args:
            dice_set: The dice set used for rolling
        """
        if not self.is_in_jail:
            return
        
        # Check for doubles - immediate escape
        if dice_set.is_double_roll():
            self._escape_jail()
            self.move_by_spaces(dice_set.get_total_value())
            return
        
        # Increment jail turns
        self.jail_turn_count += 1
        
        # Force payment of bail after maximum turns
        if self.jail_turn_count > self.MAX_JAIL_TURNS:
            self.pay_jail_bail()
            self.move_by_spaces(dice_set.get_total_value())
    
    def pay_jail_bail(self) -> None:
        """
        Pay bail to escape from jail.
        
        Deducts the bail amount and resets jail status. If the player
        cannot afford bail, bankruptcy procedures may be triggered.
        """
        self.deduct_money(self.BAIL_AMOUNT)
        self._escape_jail()
    
    def _escape_jail(self) -> None:
        """Reset jail status when the player escapes."""
        self.is_in_jail = False
        self.jail_turn_count = 0
    
    def start_turn(self) -> None:
        """Mark this player as having the current turn."""
        self.is_current_turn = True
    
    def end_turn(self) -> None:
        """Mark this player's turn as finished."""
        self.is_current_turn = False
    
    def receive_money(self, amount: int) -> None:
        """
        Add money to the player's account.
        
        Args:
            amount: Amount of money to add
        """
        self.money += amount
        print(f"{self.name} received ${amount}. New balance: ${self.money}")
    
    def deduct_money(self, amount: int) -> None:
        """
        Attempt to deduct money from the player's account.
        
        If the player has sufficient funds, the amount is deducted.
        Otherwise, bankruptcy procedures are initiated.
        
        Args:
            amount: Amount of money to deduct
        """
        print(f"Charging ${amount} to {self.name}. Current balance: ${self.money}")
        
        if self.money >= amount:
            self.money -= amount
            print(f"Payment successful. New balance: ${self.money}")
        else:
            print(f"Insufficient funds. Initiating bankruptcy procedures.")
            self._handle_bankruptcy(amount)
    
    def _handle_bankruptcy(self, required_amount: int) -> None:
        """
        Handle bankruptcy when the player cannot pay required amount.
        
        This method attempts to liquidate assets in order: buildings first,
        then mortgaging properties, and finally declaring bankruptcy.
        
        Args:
            required_amount: The amount of money needed
        """
        print(f"Bankruptcy handler: {self.name} needs ${required_amount}, has ${self.money}")
        
        # Try to raise funds through asset liquidation
        while self.money < required_amount and not self.is_bankrupt:
            funds_raised = False
            
            # First, try selling buildings
            if self._sell_available_building():
                funds_raised = True
                continue
            
            # Then, try mortgaging properties
            if self._mortgage_available_property():
                funds_raised = True
                continue
            
            # If no assets can be liquidated, declare bankruptcy
            if not funds_raised:
                self._declare_bankruptcy()
                break
        
        print(f"After liquidation: {self.name} has ${self.money}")
    
    def _sell_available_building(self) -> bool:
        """
        Attempt to sell one building to raise funds.
        
        Returns:
            True if a building was sold, False if none available
        """
        for property_obj, building_count in self.buildings.items():
            if building_count > 0:
                self.sell_building(property_obj)
                print(f"Sold building. New balance: ${self.money}")
                return True
        return False
    
    def _mortgage_available_property(self) -> bool:
        """
        Attempt to mortgage one unmortgaged property.
        
        Returns:
            True if a property was mortgaged, False if none available
        """
        for property_obj in self.properties:
            if hasattr(property_obj, 'isMortgaged') and not property_obj.isMortgaged:
                self.mortgage_property(property_obj)
                print(f"Mortgaged property. New balance: ${self.money}")
                return True
        return False
    
    def _declare_bankruptcy(self) -> None:
        """Declare the player bankrupt and reset their money to zero."""
        self.is_bankrupt = True
        self.money = 0
        print(f"{self.name} has declared bankruptcy.")
    
    def construct_building(self, property_obj) -> bool:
        """
        Attempt to build a house or hotel on a property.
        
        Validates that the player owns the property, has enough money,
        and follows even building rules before constructing.
        
        Args:
            property_obj: The property to build on
            
        Returns:
            True if building was successful, False otherwise
        """
        # Initialize building tracking if needed
        if property_obj not in self.buildings:
            self.buildings[property_obj] = 0
        
        # Check building constraints
        max_buildings = 5  # 4 houses + 1 hotel
        current_buildings = self.buildings[property_obj]
        
        if (current_buildings >= max_buildings or 
            self.money < property_obj.buildCost or
            not property_obj.builtEvenly(self)):
            return False
        
        # Construct the building
        self.buildings[property_obj] += 1
        property_obj.numHouses += 1
        self.deduct_money(property_obj.buildCost)
        
        return True
    
    def sell_building(self, property_obj) -> bool:
        """
        Sell a building from a property.
        
        Args:
            property_obj: The property to sell buildings from
            
        Returns:
            True if a building was sold, False if none available
        """
        if property_obj not in self.buildings or self.buildings[property_obj] <= 0:
            return False
        
        # Sell the building
        self.buildings[property_obj] -= 1
        property_obj.numHouses -= 1
        self.receive_money(property_obj.buildCost // 2)
        
        # Clean up empty entries
        if self.buildings[property_obj] == 0:
            del self.buildings[property_obj]
        
        return True
    
    def mortgage_property(self, property_obj) -> bool:
        """
        Mortgage a property to raise funds.
        
        Args:
            property_obj: The property to mortgage
            
        Returns:
            True if property was mortgaged, False if not owned or already mortgaged
        """
        if (property_obj not in self.properties or 
            getattr(property_obj, 'isMortgaged', True)):
            return False
        
        property_obj.isMortgaged = True
        self.receive_money(property_obj.mortgagePrice)
        return True
    
    def get_owned_color_sets(self) -> Optional[List]:
        """
        Determine which complete color sets this player owns.
        
        A complete color set allows the player to build houses and charge
        double rent. Brown and Dark Blue sets require 2 properties,
        all others require 3.
        
        Returns:
            List of color tuples for complete sets, or None if no complete sets
        """
        color_counts = {
            BROWN: 0, LIGHT_BLUE: 0, PURPLE: 0, ORANGE: 0,
            RED: 0, YELLOW: 0, GREEN: 0, DARK_BLUE: 0
        }
        
        # Count properties by color
        for property_obj in self.properties:
            if isinstance(property_obj, ColorSet) and hasattr(property_obj, 'color'):
                color_counts[property_obj.color] += 1
        
        # Determine complete sets
        complete_sets = []
        for color, count in color_counts.items():
            required = self.COLOR_SET_REQUIREMENTS[color]
            if count >= required:
                complete_sets.append(color)
        
        return complete_sets if complete_sets else None
    
    def render_buildings(self) -> None:
        """
        Render visual indicators for all buildings owned by this player.
        
        This method draws small rectangles representing houses and hotels
        on the properties where they have been built.
        """
        for property_obj, building_count in self.buildings.items():
            for i in range(building_count):
                self._render_single_building(property_obj, i)
    
    def _render_single_building(self, property_obj, building_index: int) -> None:
        """
        Render a single building indicator.
        
        Args:
            property_obj: The property the building is on
            building_index: Which building number this is (0-4)
        """
        if not hasattr(property_obj, 'tagPos') or not hasattr(property_obj, 'isTagHorz'):
            return
        
        base_x, base_y = property_obj.tagPos
        
        if property_obj.isTagHorz:
            building_rect = (
                base_x + (PROP_TAG_WIDTH * building_index), base_y,
                PROP_TAG_WIDTH, PROP_TAG_HEIGHT
            )
        else:
            building_rect = (
                base_x, base_y + (PROP_TAG_WIDTH * building_index),
                PROP_TAG_HEIGHT, PROP_TAG_WIDTH
            )
        
        draw_rounded_rect(self.screen, self.color, building_rect, 5)
    
    # Legacy method names for backward compatibility
    def move(self, spaces: int) -> None:
        """Legacy method name - use move_by_spaces() instead."""
        self.move_by_spaces(spaces)
    
    def moveTo(self, location: int) -> None:
        """Legacy method name - use move_to_space() instead."""
        self.move_to_space(location)
    
    def updateLocation(self, spaces: int) -> None:
        """Legacy method name - use _update_board_position() instead."""
        self._update_board_position(spaces)
    
    def displayProperties(self) -> None:
        """Legacy method name - use render_property_ownership() instead."""
        self.render_property_ownership()
    
    def sendToJail(self) -> None:
        """Legacy method name - use send_to_jail() instead."""
        self.send_to_jail()
    
    def jailTurn(self, dice_set) -> None:
        """Legacy method name - use handle_jail_turn() instead."""
        self.handle_jail_turn(dice_set)
    
    def payBail(self) -> None:
        """Legacy method name - use pay_jail_bail() instead."""
        self.pay_jail_bail()
    
    def giveTurn(self) -> None:
        """Legacy method name - use start_turn() instead."""
        self.start_turn()
    
    def removeTurn(self) -> None:
        """Legacy method name - use end_turn() instead."""
        self.end_turn()
    
    def charge(self, amount: int) -> None:
        """Legacy method name - use deduct_money() instead."""
        self.deduct_money(amount)
    
    def handleBankrupt(self, amount: int) -> None:
        """Legacy method name - use _handle_bankruptcy() instead."""
        self._handle_bankruptcy(amount)
    
    def build(self, property_obj) -> bool:
        """Legacy method name - use construct_building() instead."""
        return self.construct_building(property_obj)
    
    def sellHouse(self, property_obj) -> bool:
        """Legacy method name - use sell_building() instead."""
        return self.sell_building(property_obj)
    
    def mortgageProperty(self, property_obj) -> bool:
        """Legacy method name - use mortgage_property() instead."""
        return self.mortgage_property(property_obj)
    
    def getColorSets(self) -> Optional[List]:
        """Legacy method name - use get_owned_color_sets() instead."""
        return self.get_owned_color_sets()
    
    def drawHouses(self) -> None:
        """Legacy method name - use render_buildings() instead."""
        self.render_buildings()
    
    def drawHouse(self, building, index: int) -> None:
        """Legacy method name - use _render_single_building() instead."""
        self._render_single_building(building, index)
    
    # Legacy property names
    @property
    def id(self) -> int:
        """Legacy property name - use player_id instead."""
        return self.player_id
    
    @property
    def piece(self) -> str:
        """Legacy property name - use piece_name instead."""
        return self.piece_name
    
    @property
    def getOutOfJailFreeCards(self) -> int:
        """Legacy property name - use get_out_of_jail_cards instead."""
        return self.get_out_of_jail_cards
    
    @property
    def isTurn(self) -> bool:
        """Legacy property name - use is_current_turn instead."""
        return self.is_current_turn
    
    @property
    def inJail(self) -> bool:
        """Legacy property name - use is_in_jail instead."""
        return self.is_in_jail
    
    @property
    def jailTurns(self) -> int:
        """Legacy property name - use jail_turn_count instead."""
        return self.jail_turn_count
    
    @property
    def isBankrupt(self) -> bool:
        """Legacy property name - use is_bankrupt instead."""
        return self.is_bankrupt
    
    @property
    def playerBanner(self):
        """Legacy property name - use player_banner instead."""
        return self.player_banner
    
    @property
    def playerPiece(self):
        """Legacy property name - use player_piece instead."""
        return self.player_piece
    
    def getColor(self) -> Tuple[int, int, int]:
        """Legacy method name - use _get_player_color() instead."""
        return self._get_player_color()


class PlayerPiece:
    """
    Represents the visual game piece for a player on the board.
    
    This class manages the visual representation of a player's position
    on the game board, including the appropriate piece image and
    position calculation based on the player's current location.
    
    Attributes:
        screen (pygame.Surface): The game display surface
        player (Player): The player this piece represents
        current_position (Tuple[int, int]): Current pixel coordinates
        piece_image (pygame.Surface): The image to display for this piece
    """
    
    # Piece name to index mapping for image selection
    PIECE_IMAGE_INDICES = {
        "Boat": 0, "Car": 1, "Hat": 2,
        "Scope": 3, "Shoe": 4, "Wheelbarrow": 5
    }
    
    def __init__(self, screen: pygame.Surface, player: Player) -> None:
        """
        Initialize a player piece.
        
        Args:
            screen: The pygame surface for rendering
            player: The player this piece represents
        """
        self.screen = screen
        self.player = player
        self.current_position = self._calculate_position()
        self.piece_image = self._get_piece_image()
    
    def render(self) -> None:
        """
        Render the player piece to the screen.
        
        This method draws the piece image at its current position
        on the game board.
        """
        if self.piece_image:
            self.screen.blit(self.piece_image, self.current_position)
    
    def _get_piece_image(self) -> Optional[pygame.Surface]:
        """
        Get the appropriate image for this player's piece.
        
        Returns:
            The pygame Surface for the piece image, or None if not found
        """
        piece_index = self.PIECE_IMAGE_INDICES.get(self.player.piece_name)
        
        if piece_index is not None and piece_index < len(PIECE_IMGS):
            return PIECE_IMGS[piece_index]
        
        return None
    
    def _calculate_position(self) -> Tuple[int, int]:
        """
        Calculate the pixel position for this piece based on player location.
        
        Each board space has multiple positions to accommodate different players.
        This method selects the appropriate position based on the player's ID.
        
        Returns:
            Tuple of (x, y) pixel coordinates, or (0, 0) if invalid
        """
        location_name = self.player.location[0]
        
        if location_name not in BOARDCOORDS:
            return (0, 0)
        
        position_options = BOARDCOORDS[location_name]
        
        # Ensure player ID is within valid range
        if 0 <= self.player.player_id < len(position_options):
            return position_options[self.player.player_id]
        
        return (0, 0)
    
    def update_position(self) -> None:
        """
        Update the piece position based on the player's current location.
        
        This method should be called whenever the player moves to ensure
        the visual representation stays synchronized with the game state.
        """
        self.current_position = self._calculate_position()
    
    # Legacy method names for backward compatibility
    def draw(self) -> None:
        """Legacy method name - use render() instead."""
        self.render()
    
    def getImg(self) -> Optional[pygame.Surface]:
        """Legacy method name - use _get_piece_image() instead."""
        return self._get_piece_image()
    
    def getPos(self) -> Tuple[int, int]:
        """Legacy method name - use _calculate_position() instead."""
        return self._calculate_position()
    
    @property
    def pos(self) -> Tuple[int, int]:
        """Legacy property name - use current_position instead."""
        return self.current_position
    
    @pos.setter
    def pos(self, value: Tuple[int, int]) -> None:
        """Legacy property setter - use current_position instead."""
        self.current_position = value
    
    @property
    def img(self) -> Optional[pygame.Surface]:
        """Legacy property name - use piece_image instead."""
        return self.piece_image


# Legacy class name for backward compatibility
class playerPiece(PlayerPiece):
    """Legacy class name - use PlayerPiece instead."""
    pass