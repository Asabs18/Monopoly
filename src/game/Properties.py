"""
Monopoly Game Property System Module

This module implements the complete property and board space system for the Monopoly
board game. It includes all property types (color sets, railroads, utilities), special
spaces (jail, free parking, taxes), and card spaces (chance, community chest).

The system uses abstract base classes to define common interfaces while allowing
each property type to implement its own specific behaviors for rent calculation,
building mechanics, and player interactions.

Author: Aidan Sabatini
"""

# Standard library imports
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union, Any

# Third-party imports
import pygame

# Local application imports
from src.config.boardAssets import (
    PROPPRICES, MORTGAGEPRICES, UNMORTGAGEPRICES, PROPCOLORS, BUILDINGCOSTS,
    RENTPRICES, RAILROADRENT, UTILRENT, TAXPRICES, PROPERTIES, RAILROADS,
    UTILS, TAXES, CARDSPACES, FREESPACES, BOARDCOORDS, TAGCOORDS, HOUSECOORDS,
    PROPLEVELS, PROPLEVELS_SMALL, RAILROADLEVELS, RAILROADLEVELS_SMALL,
    UTILLEVELS, UTILLEVELS_SMALL
)
from src.config.colorAssets import WHITE, BLACK, GREEN, RED
from src.config.fontAssets import (
    BTNFONT, PROPNAMEFONT, PROPTXTFONT, AUCCARDFONT, AUCCARDRENTFONT
)
from src.config.imgAssets import (
    RAILROADIMG, RAILROADIMGSML, UTILIMGS, UTILIMGSSML, TAXIMGS,
    FREEPARKINGIMG, GOTOJAILIMG
)
from src.config.displayAssets import (
    BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT, PROP_NAME_X, PROP_NAME_Y,
    NAME_LN_START, NAME_LN_END, BUY_PRICE_X, BUY_PRICE_Y, BUY_BTN_X, BUY_BTN_Y,
    BUY_BTN_WIDTH, BUY_BTN_HEIGHT, AUCT_BTN_X, AUCT_BTN_Y, AUCT_BTN_WIDTH,
    AUCT_BTN_HEIGHT, RAIL_IMG_X, RAIL_IMG_Y, RAIL_BUY_PRICE_X, RAIL_BUY_PRICE_Y,
    RAIL_IMG_SML_X, RAIL_IMG_SML_Y, UTIL_IMG_X, UTIL_IMG_Y, UTIL_IMG_SML_X,
    UTIL_IMG_SML_Y, FREE_PARKING_X, FREE_PARKING_Y, GO_TO_JAIL_X, GO_TO_JAIL_Y,
    TAX_TXT_X, TAX_TXT_Y, INCOME_TAX_X, INCOME_TAX_Y, OK_BTN_X, OK_BTN_Y,
    OK_BTN_WIDTH, OK_BTN_HEIGHT, IN_JAIL_WIN_X, IN_JAIL_WIN_Y, IN_JAIL_WIN_WIDTH,
    IN_JAIL_WIN_HEIGHT, JAIL_TXT_X, JAIL_TXT_Y, PAY_BTN_WIDTH, PAY_BTN_HEIGHT,
    AUC_CARD_NAME_X, AUC_CARD_NAME_Y, AUC_CARD_PRICE_X, AUC_CARD_PRICE_Y,
    SMALL_CARD_LINE_START, SMALL_CARD_LINE_END
)
from src.ui.components.Button import Button
from src.ui.components.Helper import drawText, drawTextMultiLines
from src.game.Cards import ChanceCard, CommunityChestCard, ChanceDeck, CommunityChestDeck
from src.game.Auction import Auction

# Initialize pygame
pygame.init()


class BoardSpace(ABC):
    """
    Abstract base class for all spaces on the Monopoly board.
    
    This class defines the common interface that all board spaces must implement,
    including properties, special spaces, and action spaces. Each space has a name,
    position coordinates for up to 4 players, and display functionality.
    
    Attributes:
        screen (pygame.Surface): The game display surface
        name (str): The name of this board space
        should_show_ui (bool): Whether to display the space's interaction UI
        player_positions (Tuple): Coordinate positions for up to 4 players
    """
    
    def __init__(self, name: str, screen: pygame.Surface) -> None:
        """
        Initialize a board space with basic properties.
        
        Args:
            name: The display name of this board space
            screen: The pygame surface for rendering
        """
        self.screen = screen
        self.name = name
        self.should_show_ui = True
        
        # Get player position coordinates for this space
        self.player_positions = self._get_player_coordinates()
    
    def __str__(self) -> str:
        """Return string representation of the board space."""
        return f"{self.name}: UI Visible={self.should_show_ui}"
    
    def _get_player_coordinates(self) -> Tuple:
        """
        Get the coordinate positions for players on this space.
        
        Returns:
            Tuple containing (x, y) coordinates for up to 4 players
        """
        return BOARDCOORDS.get(self.name, ((0, 0), (0, 0), (0, 0), (0, 0)))
    
    def can_be_purchased(self, player) -> bool:
        """
        Check if this space can be purchased by the given player.
        
        Args:
            player: The player attempting to purchase
            
        Returns:
            False by default (most spaces cannot be purchased)
        """
        return False
    
    def can_charge_rent(self, player) -> bool:
        """
        Check if this space can charge rent to the given player.
        
        Args:
            player: The player to potentially charge
            
        Returns:
            False by default (most spaces don't charge rent)
        """
        return False
    
    @abstractmethod
    def handle_player_landing(self, player) -> None:
        """
        Handle the effects when a player lands on this space.
        
        Args:
            player: The player who landed on this space
        """
        pass
    
    @abstractmethod
    def render_ui(self) -> None:
        """Render the user interface for this space when appropriate."""
        pass
    
    # Legacy method names for backward compatibility
    def landedOn(self, player) -> None:
        """Legacy method name - use handle_player_landing() instead."""
        self.handle_player_landing(player)
    
    def display(self) -> None:
        """Legacy method name - use render_ui() instead."""
        self.render_ui()
    
    def canBuy(self, player) -> bool:
        """Legacy method name - use can_be_purchased() instead."""
        return self.can_be_purchased(player)
    
    def canCharge(self, player) -> bool:
        """Legacy method name - use can_charge_rent() instead."""
        return self.can_charge_rent(player)
    
    @property
    def show(self) -> bool:
        """Legacy property name - use should_show_ui instead."""
        return self.should_show_ui
    
    @show.setter
    def show(self, value: bool) -> None:
        """Legacy property setter - use should_show_ui instead."""
        self.should_show_ui = value
    
    def getCoords(self) -> Tuple:
        """Legacy method name - use _get_player_coordinates() instead."""
        return self._get_player_coordinates()


class Property(BoardSpace):
    """
    Abstract base class for all purchasable properties.
    
    This class implements the common functionality for properties that can be
    bought, sold, mortgaged, and potentially developed with buildings. It handles
    ownership, pricing, auction mechanics, and basic rent collection.
    
    Attributes:
        is_owned (bool): Whether the property is currently owned
        purchase_price (int): Cost to buy the property
        mortgage_value (int): Amount received when mortgaging
        unmortgage_cost (int): Cost to unmortgage the property
        is_mortgaged (bool): Whether the property is currently mortgaged
        tag_position (Tuple[int, int]): Screen coordinates for ownership indicator
        is_tag_horizontal (bool): Orientation of the ownership tag
        auction (Optional[Auction]): Current auction if property is being auctioned
        buy_button (Button): UI button for purchasing
        auction_button (Button): UI button for starting auction
    """
    
    # UI constants
    WINDOW_BORDER_WIDTH = 10
    WINDOW_FRAME_WIDTH = 2
    
    def __init__(self, name: str, screen: pygame.Surface) -> None:
        """
        Initialize a property with pricing and UI components.
        
        Args:
            name: The name of the property
            screen: The pygame surface for rendering
        """
        super().__init__(name, screen)
        
        # Property ownership and financial data
        self.is_owned = False
        self.purchase_price = PROPPRICES[self.name]
        self.mortgage_value = MORTGAGEPRICES[self.name]
        self.unmortgage_cost = UNMORTGAGEPRICES[self.name]
        self.is_mortgaged = False
        
        # Visual positioning for ownership indicators
        tag_data = TAGCOORDS[self.name]
        self.tag_position = tag_data[0]
        self.is_tag_horizontal = tag_data[1]
        
        # Auction system
        self.auction: Optional[Auction] = None
        
        # Initialize UI components
        self._initialize_ui_buttons()
    
    def _initialize_ui_buttons(self) -> None:
        """Initialize the buy and auction buttons for property interaction."""
        buy_button_rect = (BUY_BTN_X, BUY_BTN_Y, BUY_BTN_WIDTH, BUY_BTN_HEIGHT)
        auction_button_rect = (AUCT_BTN_X, AUCT_BTN_Y, AUCT_BTN_WIDTH, AUCT_BTN_HEIGHT)
        
        self.buy_button = Button(
            self.screen, "Buy", BTNFONT, buy_button_rect, GREEN
        )
        self.auction_button = Button(
            self.screen, "Auction", BTNFONT, auction_button_rect, RED
        )
    
    def can_be_purchased(self, player) -> bool:
        """
        Check if the property can be purchased by the given player.
        
        Args:
            player: The player attempting to purchase
            
        Returns:
            True if unowned and player has sufficient funds
        """
        return not self.is_owned and player.money >= self.purchase_price
    
    def handle_player_landing(self, player) -> None:
        """
        Handle a player landing on this property.
        
        Args:
            player: The player who landed on the property
        """
        if self.can_be_purchased(player):
            self.should_show_ui = True
        elif self.can_charge_rent(player):
            self.charge_rent(player)
        else:
            # Handle bankruptcy or other edge cases
            print(f"Player cannot afford {self.name}")
    
    def purchase_property(self, player) -> bool:
        """
        Execute the purchase of this property by a player.
        
        Args:
            player: The player purchasing the property
            
        Returns:
            True if purchase was successful, False otherwise
        """
        if not self.can_be_purchased(player):
            return False
        
        # Execute the transaction
        self.is_owned = True
        player.deduct_money(self.purchase_price)
        player.properties.append(self)
        
        return True
    
    def purchase_at_auction(self, player, bid_amount: int) -> bool:
        """
        Execute the purchase of this property at auction.
        
        Args:
            player: The winning bidder
            bid_amount: The winning bid amount
            
        Returns:
            True if purchase was successful, False otherwise
        """
        self.is_owned = True
        player.deduct_money(bid_amount)
        player.properties.append(self)
        return True
    
    def charge_rent(self, player) -> None:
        """
        Charge rent to a player landing on this property.
        
        Args:
            player: The player to charge rent
        """
        if not self.is_mortgaged:
            rent_amount = self.calculate_rent()
            player.deduct_money(rent_amount)
    
    def handle_buy_button_click(self, player) -> None:
        """
        Handle the buy button being clicked.
        
        Args:
            player: The player attempting to buy
        """
        if self.purchase_property(player):
            self.should_show_ui = False
    
    def handle_auction_button_click(self, players: List) -> None:
        """
        Handle the auction button being clicked.
        
        Args:
            players: List of all players who can participate in the auction
        """
        self.should_show_ui = False
        self.auction = Auction(self.screen, players, self)
        self.auction.start_auction()
    
    def _draw_property_window(self) -> None:
        """Draw the standard property information window."""
        # Draw window border
        border_rect = (
            BUY_WIN_X - self.WINDOW_BORDER_WIDTH,
            BUY_WIN_Y - self.WINDOW_BORDER_WIDTH,
            BUY_WIN_WIDTH + (2 * self.WINDOW_BORDER_WIDTH),
            BUY_WIN_HEIGHT + (2 * self.WINDOW_BORDER_WIDTH)
        )
        pygame.draw.rect(self.screen, WHITE, border_rect)
        
        # Draw window frame
        frame_rect = (
            BUY_WIN_X - self.WINDOW_FRAME_WIDTH,
            BUY_WIN_Y - self.WINDOW_FRAME_WIDTH,
            BUY_WIN_WIDTH + (2 * self.WINDOW_FRAME_WIDTH),
            BUY_WIN_HEIGHT + (2 * self.WINDOW_FRAME_WIDTH)
        )
        pygame.draw.rect(self.screen, BLACK, frame_rect)
        
        # Draw main window
        main_rect = (BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, main_rect)
    
    def _draw_property_header(self) -> None:
        """Draw the property name and underline."""
        drawText(
            self.screen, self.name, PROPNAMEFONT, BLACK,
            (PROP_NAME_X, PROP_NAME_Y)
        )
        pygame.draw.line(
            self.screen, BLACK, NAME_LN_START, NAME_LN_END, 2
        )
    
    def _draw_property_price(self) -> None:
        """Draw the property purchase price."""
        price_text = f"Price: ${self.purchase_price}"
        drawText(
            self.screen, price_text, PROPTXTFONT, BLACK,
            (BUY_PRICE_X, BUY_PRICE_Y)
        )
    
    def _draw_action_buttons(self) -> None:
        """Draw the buy and auction buttons."""
        self.buy_button.draw()
        self.auction_button.draw()
    
    @abstractmethod
    def can_build_improvements(self) -> bool:
        """
        Check if buildings can be constructed on this property.
        
        Returns:
            True if buildings are allowed, False otherwise
        """
        pass
    
    @abstractmethod
    def calculate_rent(self) -> int:
        """
        Calculate the current rent for this property.
        
        Returns:
            The amount of rent to charge
        """
        pass
    
    @abstractmethod
    def render_small_card(self, x: int, y: int, width: int, height: int) -> None:
        """
        Render a small version of the property card for auctions.
        
        Args:
            x: X coordinate for the card
            y: Y coordinate for the card
            width: Width of the card
            height: Height of the card
        """
        pass
    
    @abstractmethod
    def update_rent_level(self, players: List) -> None:
        """
        Update the rent calculation based on current game state.
        
        Args:
            players: List of all players in the game
        """
        pass
    
    # Legacy method names for backward compatibility
    def buy(self, player) -> bool:
        """Legacy method name - use purchase_property() instead."""
        return self.purchase_property(player)
    
    def buyAuc(self, player, price: int) -> bool:
        """Legacy method name - use purchase_at_auction() instead."""
        return self.purchase_at_auction(player, price)
    
    def charge(self, player) -> None:
        """Legacy method name - use charge_rent() instead."""
        self.charge_rent(player)
    
    def buyBtnAction(self, player) -> None:
        """Legacy method name - use handle_buy_button_click() instead."""
        self.handle_buy_button_click(player)
    
    def auctionBtnAction(self, players: List) -> None:
        """Legacy method name - use handle_auction_button_click() instead."""
        self.handle_auction_button_click(players)
    
    def canBuild(self) -> bool:
        """Legacy method name - use can_build_improvements() instead."""
        return self.can_build_improvements()
    
    def getRent(self, level) -> int:
        """Legacy method name - use calculate_rent() instead."""
        return self.calculate_rent()
    
    def smallCard(self, x: int, y: int, width: int, height: int) -> None:
        """Legacy method name - use render_small_card() instead."""
        self.render_small_card(x, y, width, height)
    
    def update(self, players: List) -> None:
        """Legacy method name - use update_rent_level() instead."""
        self.update_rent_level(players)
    
    # Legacy property names
    @property
    def isOwned(self) -> bool:
        """Legacy property name - use is_owned instead."""
        return self.is_owned
    
    @property
    def price(self) -> int:
        """Legacy property name - use purchase_price instead."""
        return self.purchase_price
    
    @property
    def mortgagePrice(self) -> int:
        """Legacy property name - use mortgage_value instead."""
        return self.mortgage_value
    
    @property
    def unmortgagePirce(self) -> int:
        """Legacy property name - use unmortgage_cost instead."""
        return self.unmortgage_cost
    
    @property
    def isMortgaged(self) -> bool:
        """Legacy property name - use is_mortgaged instead."""
        return self.is_mortgaged
    
    @isMortgaged.setter
    def isMortgaged(self, value: bool) -> None:
        """Legacy property setter - use is_mortgaged instead."""
        self.is_mortgaged = value
    
    @property
    def tagPos(self) -> Tuple[int, int]:
        """Legacy property name - use tag_position instead."""
        return self.tag_position
    
    @property
    def isTagHorz(self) -> bool:
        """Legacy property name - use is_tag_horizontal instead."""
        return self.is_tag_horizontal
    
    @property
    def buyBtn(self) -> Button:
        """Legacy property name - use buy_button instead."""
        return self.buy_button
    
    @property
    def auctionBtn(self) -> Button:
        """Legacy property name - use auction_button instead."""
        return self.auction_button


class ColorSetProperty(Property):
    """
    Represents a standard colored property that can have houses and hotels.
    
    These are the most common properties on the board, organized into color groups.
    Players who own all properties in a color set can build houses and hotels,
    which dramatically increase the rent charged to other players.
    
    Attributes:
        color (Tuple[int, int, int]): RGB color tuple for this property set
        building_cost (int): Cost to build houses/hotels
        current_profit_level (str): Current rent level (Base, Color Set, House 1-4, Hotel)
        rent_schedule (Tuple): Rent amounts for each development level
        house_coordinates (Tuple): Screen coordinates for displaying buildings
        house_count (int): Number of houses/hotels built (5 = hotel)
    """
    
    # Building constants
    MAX_HOUSES = 4
    HOTEL_INDICATOR = 5
    COLOR_BAR_HEIGHT_RATIO = 5  # Height of color bar relative to window
    
    def __init__(self, name: str, screen: pygame.Surface) -> None:
        """
        Initialize a color set property with building capabilities.
        
        Args:
            name: The name of the property
            screen: The pygame surface for rendering
        """
        super().__init__(name, screen)
        
        # Property-specific attributes
        self.color = PROPCOLORS[self.name]
        self.building_cost = BUILDINGCOSTS[self.name]
        self.current_profit_level = "Base"
        self.rent_schedule = RENTPRICES[self.name]
        
        # Building management
        house_data = HOUSECOORDS[self.name]
        self.house_coordinates = house_data[0]
        self.house_count = 0
    
    def can_build_improvements(self) -> bool:
        """
        Check if houses/hotels can be built on this property.
        
        Returns:
            True if owned and not at maximum development
        """
        return (self.is_owned and 
                self.house_count < self.HOTEL_INDICATOR and
                not self.is_mortgaged)
    
    def can_charge_rent(self, player) -> bool:
        """
        Check if rent can be charged to the given player.
        
        Args:
            player: The player to potentially charge
            
        Returns:
            True if property is owned by someone else and player can pay
        """
        return (self.is_owned and 
                self not in player.properties and
                player.money >= self.calculate_rent())
    
    def calculate_rent(self) -> int:
        """
        Calculate rent based on current development level.
        
        Returns:
            The rent amount for the current profit level
        """
        rent_index_map = {
            "Base": 0,
            "Color Set": 1,
            "House 1": 2,
            "House 2": 3,
            "House 3": 4,
            "House 4": 5,
            "Hotel": 6
        }
        
        index = rent_index_map.get(self.current_profit_level, 0)
        return self.rent_schedule[index]
    
    def check_even_building(self, player) -> bool:
        """
        Check if buildings can be built evenly across the color set.
        
        The Monopoly rules require that houses be built evenly across all
        properties in a color set before any property can build additional houses.
        
        Args:
            player: The player attempting to build
            
        Returns:
            True if building would maintain even development
        """
        color_set_properties = [
            prop for prop in player.properties 
            if isinstance(prop, ColorSetProperty) and prop.color == self.color
        ]
        
        if len(color_set_properties) <= 1:
            return True
        
        # Check if this property has fewer or equal houses than others
        for other_property in color_set_properties:
            if other_property != self and self.house_count > other_property.house_count:
                return False
        
        return True
    
    def render_ui(self) -> None:
        """Render the property purchase/information interface."""
        if not self.should_show_ui or self.is_owned:
            return
        
        self._draw_property_window()
        self._draw_color_header()
        self._draw_property_header()
        self._draw_property_price()
        self._draw_rent_schedule()
        self._draw_action_buttons()
    
    def _draw_color_header(self) -> None:
        """Draw the colored header bar for the property."""
        # Draw color bar border
        color_bar_height = BUY_WIN_HEIGHT // self.COLOR_BAR_HEIGHT_RATIO
        border_rect = (
            BUY_WIN_X + 13, BUY_WIN_Y + 13,
            BUY_WIN_WIDTH - 26, color_bar_height - 26
        )
        pygame.draw.rect(self.screen, BLACK, border_rect)
        
        # Draw color bar
        color_rect = (
            BUY_WIN_X + 15, BUY_WIN_Y + 15,
            BUY_WIN_WIDTH - 30, color_bar_height - 30
        )
        pygame.draw.rect(self.screen, self.color, color_rect)
    
    def _draw_rent_schedule(self) -> None:
        """Draw the rent amounts for each development level."""
        for level_name, level_data in PROPLEVELS.items():
            rent_amount = self.calculate_rent_for_level(level_name)
            rent_text = f"{level_data[0]} ${rent_amount}"
            drawText(
                self.screen, rent_text, PROPTXTFONT, BLACK, level_data[1]
            )
    
    def calculate_rent_for_level(self, level: str) -> int:
        """
        Calculate rent for a specific development level.
        
        Args:
            level: The development level (Base, Color Set, House 1-4, Hotel)
            
        Returns:
            The rent amount for that level
        """
        level_index_map = {
            "Base": 0, "Color Set": 1, "House 1": 2, "House 2": 3,
            "House 3": 4, "House 4": 5, "Hotel": 6
        }
        
        index = level_index_map.get(level, 0)
        return self.rent_schedule[index]
    
    def render_small_card(self, x: int, y: int, width: int, height: int) -> None:
        """
        Render a compact version of the property card for auctions.
        
        Args:
            x: X coordinate for the card
            y: Y coordinate for the card  
            width: Width of the card
            height: Height of the card
        """
        # Draw card window
        self._draw_small_card_window(x, y, width, height)
        
        # Draw color header
        self._draw_small_color_header(x, y, width, height)
        
        # Draw property details
        property_name_pos = (x + AUC_CARD_NAME_X, y + AUC_CARD_NAME_Y)
        drawText(self.screen, self.name, AUCCARDFONT, BLACK, property_name_pos)
        
        price_pos = (x + AUC_CARD_PRICE_X, y + AUC_CARD_PRICE_Y)
        price_text = f"Price: ${self.purchase_price}"
        drawText(self.screen, price_text, AUCCARDFONT, BLACK, price_pos)
        
        # Draw condensed rent schedule
        for level_name, level_data in PROPLEVELS_SMALL.items():
            rent_amount = self.calculate_rent_for_level(level_name)
            rent_text = f"{level_data[0]} ${rent_amount}"
            drawText(
                self.screen, rent_text, AUCCARDRENTFONT, BLACK, level_data[1]
            )
    
    def _draw_small_card_window(self, x: int, y: int, width: int, height: int) -> None:
        """Draw the window for a small property card."""
        # Border
        border_rect = (x - 10, y - 10, width + 20, height + 20)
        pygame.draw.rect(self.screen, WHITE, border_rect)
        
        # Frame
        frame_rect = (x - 2, y - 2, width + 4, height + 4)
        pygame.draw.rect(self.screen, BLACK, frame_rect)
        
        # Main window
        main_rect = (x, y, width, height)
        pygame.draw.rect(self.screen, WHITE, main_rect)
    
    def _draw_small_color_header(self, x: int, y: int, width: int, height: int) -> None:
        """Draw the color header for a small property card."""
        color_height = height // self.COLOR_BAR_HEIGHT_RATIO
        
        # Color bar border
        border_rect = (x + 3, y + 3, width - 6, color_height - 6)
        pygame.draw.rect(self.screen, BLACK, border_rect)
        
        # Color bar
        color_rect = (x + 5, y + 5, width - 10, color_height - 10)
        pygame.draw.rect(self.screen, self.color, color_rect)
    
    def update_rent_level(self, players: List) -> None:
        """
        Update the rent level based on color set ownership and building count.
        
        Args:
            players: List of all players in the game
        """
        # Check for color set bonus
        for player in players:
            if hasattr(player, 'get_owned_color_sets'):
                owned_sets = player.get_owned_color_sets()
                if owned_sets and self.color in owned_sets:
                    self.current_profit_level = "Color Set"
                    break
        else:
            self.current_profit_level = "Base"
        
        # Override with building level if applicable
        building_levels = {
            1: "House 1", 2: "House 2", 3: "House 3",
            4: "House 4", 5: "Hotel"
        }
        
        if self.house_count in building_levels:
            self.current_profit_level = building_levels[self.house_count]
    
    # Legacy method names for backward compatibility
    def builtEvenly(self, player) -> bool:
        """Legacy method name - use check_even_building() instead."""
        return self.check_even_building(player)
    
    def getRent(self, level: str) -> int:
        """Legacy method name - use calculate_rent_for_level() instead."""
        return self.calculate_rent_for_level(level)
    
    # Legacy property names
    @property
    def buildCost(self) -> int:
        """Legacy property name - use building_cost instead."""
        return self.building_cost
    
    @property
    def currProfit(self) -> str:
        """Legacy property name - use current_profit_level instead."""
        return self.current_profit_level
    
    @currProfit.setter
    def currProfit(self, value: str) -> None:
        """Legacy property setter - use current_profit_level instead."""
        self.current_profit_level = value
    
    @property
    def rents(self) -> Tuple:
        """Legacy property name - use rent_schedule instead."""
        return self.rent_schedule
    
    @property
    def houseCoords(self) -> Tuple:
        """Legacy property name - use house_coordinates instead."""
        return self.house_coordinates
    
    @property
    def numHouses(self) -> int:
        """Legacy property name - use house_count instead."""
        return self.house_count
    
    @numHouses.setter
    def numHouses(self, value: int) -> None:
        """Legacy property setter - use house_count instead."""
        self.house_count = value


class RailroadProperty(Property):
    """
    Represents a railroad property with rent based on railroad ownership.
    
    Railroad properties have special rent calculation - the more railroads
    a player owns, the higher the rent on each individual railroad becomes.
    
    Attributes:
        current_profit_level (str): Current rent level based on railroad count
        rent_schedule (Dict): Rent amounts for different ownership levels
    """
    
    def __init__(self, name: str, screen: pygame.Surface) -> None:
        """
        Initialize a railroad property.
        
        Args:
            name: The name of the railroad
            screen: The pygame surface for rendering
        """
        super().__init__(name, screen)
        self.current_profit_level = "Base"
        self.rent_schedule = RAILROADRENT
    
    def can_build_improvements(self) -> bool:
        """Railroads cannot have buildings constructed on them."""
        return False
    
    def can_charge_rent(self, player) -> bool:
        """
        Check if rent can be charged to the given player.
        
        Args:
            player: The player to potentially charge
            
        Returns:
            True if railroad is owned by someone else and player can pay
        """
        return (self.is_owned and 
                self not in player.properties and
                player.money >= self.calculate_rent())
    
    def calculate_rent(self) -> int:
        """
        Calculate rent based on number of railroads owned.
        
        Returns:
            The rent amount for the current ownership level
        """
        return self.rent_schedule[self.current_profit_level]
    
    def render_ui(self) -> None:
        """Render the railroad purchase/information interface."""
        if not self.should_show_ui or self.is_owned:
            return
        
        self._draw_property_window()
        self._draw_property_header()
        self._draw_railroad_image()
        self._draw_property_price()
        self._draw_railroad_rent_schedule()
        self._draw_action_buttons()
    
    def _draw_railroad_image(self) -> None:
        """Draw the railroad image in the center of the window."""
        image_rect = RAILROADIMG.get_rect()
        image_rect.center = (RAIL_IMG_X, RAIL_IMG_Y)
        self.screen.blit(RAILROADIMG, image_rect)
    
    def _draw_property_price(self) -> None:
        """Draw the railroad purchase price."""
        price_text = f"Price: ${self.purchase_price}"
        drawText(
            self.screen, price_text, PROPTXTFONT, BLACK,
            (RAIL_BUY_PRICE_X, RAIL_BUY_PRICE_Y)
        )
    
    def _draw_railroad_rent_schedule(self) -> None:
        """Draw the rent schedule for different railroad ownership levels."""
        for level_name, level_data in RAILROADLEVELS.items():
            rent_amount = self.rent_schedule[level_name]
            rent_text = f"{level_data[0]} ${rent_amount}"
            drawText(
                self.screen, rent_text, PROPTXTFONT, BLACK, level_data[1]
            )
    
    def render_small_card(self, x: int, y: int, width: int, height: int) -> None:
        """
        Render a compact version of the railroad card for auctions.
        
        Args:
            x: X coordinate for the card
            y: Y coordinate for the card
            width: Width of the card
            height: Height of the card
        """
        # Draw card window
        self._draw_small_card_window(x, y, width, height)
        
        # Draw railroad details
        name_pos = (x + AUC_CARD_NAME_X, y + AUC_CARD_NAME_Y)
        drawText(self.screen, self.name, AUCCARDFONT, BLACK, name_pos)
        
        # Draw underline
        pygame.draw.line(
            self.screen, BLACK, SMALL_CARD_LINE_START, SMALL_CARD_LINE_END, 2
        )
        
        # Draw price
        price_pos = (x + AUC_CARD_PRICE_X, y + AUC_CARD_PRICE_Y + 80)
        price_text = f"Price: ${self.purchase_price}"
        drawText(self.screen, price_text, AUCCARDFONT, BLACK, price_pos)
        
        # Draw small railroad image
        image_rect = RAILROADIMGSML.get_rect()
        image_rect.center = (RAIL_IMG_SML_X, RAIL_IMG_SML_Y)
        self.screen.blit(RAILROADIMGSML, image_rect)
        
        # Draw condensed rent schedule
        for level_name, level_data in RAILROADLEVELS_SMALL.items():
            rent_amount = self.rent_schedule[level_name]
            rent_text = f"{level_data[0]} ${rent_amount}"
            drawText(
                self.screen, rent_text, AUCCARDRENTFONT, BLACK, level_data[1]
            )
    
    def _draw_small_card_window(self, x: int, y: int, width: int, height: int) -> None:
        """Draw the window for a small railroad card."""
        # Border
        border_rect = (x - 10, y - 10, width + 20, height + 20)
        pygame.draw.rect(self.screen, WHITE, border_rect)
        
        # Frame
        frame_rect = (x - 2, y - 2, width + 4, height + 4)
        pygame.draw.rect(self.screen, BLACK, frame_rect)
        
        # Main window
        main_rect = (x, y, width, height)
        pygame.draw.rect(self.screen, WHITE, main_rect)
    
    def update_rent_level(self, players: List) -> None:
        """
        Update rent level based on how many railroads the owner has.
        
        Args:
            players: List of all players in the game
        """
        railroad_count = 0
        
        # Find the owner and count their railroads
        for player in players:
            if self in player.properties:
                railroad_count = sum(
                    1 for prop in player.properties 
                    if isinstance(prop, RailroadProperty)
                )
                break
        
        # Set profit level based on railroad count
        profit_levels = {
            1: "Base", 2: "Own 2", 3: "Own 3", 4: "Own 4"
        }
        self.current_profit_level = profit_levels.get(railroad_count, "Base")
    
    # Legacy property names
    @property
    def currProfit(self) -> str:
        """Legacy property name - use current_profit_level instead."""
        return self.current_profit_level
    
    @currProfit.setter
    def currProfit(self, value: str) -> None:
        """Legacy property setter - use current_profit_level instead."""
        self.current_profit_level = value
    
    @property
    def rents(self) -> Dict:
        """Legacy property name - use rent_schedule instead."""
        return self.rent_schedule


class UtilityProperty(Property):
    """
    Represents a utility property with dice-based rent calculation.
    
    Utility properties charge rent based on a multiplier times the dice roll.
    The multiplier increases if a player owns both utilities.
    
    Attributes:
        current_profit_level (str): Current rent level (Base or Own 2)
        rent_multipliers (Dict): Multipliers for dice-based rent calculation
    """
    
    def __init__(self, name: str, screen: pygame.Surface) -> None:
        """
        Initialize a utility property.
        
        Args:
            name: The name of the utility
            screen: The pygame surface for rendering
        """
        super().__init__(name, screen)
        self.current_profit_level = "Base"
        self.rent_multipliers = UTILRENT
    
    def can_build_improvements(self) -> bool:
        """Utilities cannot have buildings constructed on them."""
        return False
    
    def can_charge_rent(self, player) -> bool:
        """
        Check if rent can be charged to the given player.
        
        Args:
            player: The player to potentially charge
            
        Returns:
            True if utility is owned by someone else
        """
        return (self.is_owned and 
                self not in player.properties)
    
    def calculate_rent(self, dice_roll: int = 0) -> int:
        """
        Calculate rent based on dice roll and utility ownership.
        
        Args:
            dice_roll: The result of the dice roll (default 0 for display)
            
        Returns:
            The rent amount (multiplier * dice_roll)
        """
        multiplier = self.rent_multipliers[self.current_profit_level]
        return multiplier * dice_roll
    
    def get_rent_multiplier(self) -> int:
        """
        Get the current rent multiplier.
        
        Returns:
            The multiplier used for rent calculation
        """
        return self.rent_multipliers[self.current_profit_level]
    
    def render_ui(self) -> None:
        """Render the utility purchase/information interface."""
        if not self.should_show_ui or self.is_owned:
            return
        
        self._draw_property_window()
        self._draw_property_header()
        self._draw_utility_image()
        self._draw_property_price()
        self._draw_utility_rent_info()
        self._draw_action_buttons()
    
    def _draw_utility_image(self) -> None:
        """Draw the utility-specific image."""
        image = UTILIMGS[self.name]
        image_rect = image.get_rect()
        image_rect.center = (UTIL_IMG_X, UTIL_IMG_Y)
        self.screen.blit(image, image_rect)
    
    def _draw_property_price(self) -> None:
        """Draw the utility purchase price."""
        price_text = f"Price: ${self.purchase_price}"
        drawText(
            self.screen, price_text, PROPTXTFONT, BLACK,
            (RAIL_BUY_PRICE_X, RAIL_BUY_PRICE_Y)
        )
    
    def _draw_utility_rent_info(self) -> None:
        """Draw the rent calculation information for utilities."""
        for level_name, level_data in UTILLEVELS.items():
            multiplier = self.rent_multipliers[level_name]
            
            # Draw three lines of text for each level
            line1_pos = (level_data[2][0], level_data[2][1] - 25)
            line2_pos = level_data[2]
            line3_pos = (level_data[2][0], level_data[2][1] + 25)
            
            drawText(self.screen, level_data[0], PROPTXTFONT, BLACK, line1_pos)
            drawText(self.screen, f"{level_data[1]}{multiplier}", PROPTXTFONT, BLACK, line2_pos)
            drawText(self.screen, "times the amount shown on the dice", PROPTXTFONT, BLACK, line3_pos)
    
    def render_small_card(self, x: int, y: int, width: int, height: int) -> None:
        """
        Render a compact version of the utility card for auctions.
        
        Args:
            x: X coordinate for the card
            y: Y coordinate for the card
            width: Width of the card
            height: Height of the card
        """
        # Draw card window
        self._draw_small_card_window(x, y, width, height)
        
        # Draw utility details
        name_pos = (x + AUC_CARD_NAME_X, y + AUC_CARD_NAME_Y)
        drawText(self.screen, self.name, AUCCARDFONT, BLACK, name_pos)
        
        # Draw underline
        pygame.draw.line(
            self.screen, BLACK, SMALL_CARD_LINE_START, SMALL_CARD_LINE_END, 2
        )
        
        # Draw price
        price_pos = (x + AUC_CARD_PRICE_X, y + AUC_CARD_PRICE_Y + 80)
        price_text = f"Price: ${self.purchase_price}"
        drawText(self.screen, price_text, AUCCARDFONT, BLACK, price_pos)
        
        # Draw small utility image
        image = UTILIMGSSML[self.name]
        image_rect = image.get_rect()
        image_rect.center = (UTIL_IMG_SML_X, UTIL_IMG_SML_Y)
        self.screen.blit(image, image_rect)
        
        # Draw condensed rent information
        for level_name, level_data in UTILLEVELS_SMALL.items():
            multiplier = self.rent_multipliers[level_name]
            rent_text = f"{level_data[0]} ${multiplier}"
            drawTextMultiLines(
                self.screen, rent_text, AUCCARDRENTFONT, BLACK, level_data[1], 15
            )
    
    def _draw_small_card_window(self, x: int, y: int, width: int, height: int) -> None:
        """Draw the window for a small utility card."""
        # Border
        border_rect = (x - 10, y - 10, width + 20, height + 20)
        pygame.draw.rect(self.screen, WHITE, border_rect)
        
        # Frame
        frame_rect = (x - 2, y - 2, width + 4, height + 4)
        pygame.draw.rect(self.screen, BLACK, frame_rect)
        
        # Main window
        main_rect = (x, y, width, height)
        pygame.draw.rect(self.screen, WHITE, main_rect)
    
    def update_rent_level(self, players: List) -> None:
        """
        Update rent level based on how many utilities the owner has.
        
        Args:
            players: List of all players in the game
        """
        utility_count = 0
        
        # Find the owner and count their utilities
        for player in players:
            if self in player.properties:
                utility_count = sum(
                    1 for prop in player.properties 
                    if isinstance(prop, UtilityProperty)
                )
                break
        
        # Set profit level based on utility count
        self.current_profit_level = "Own 2" if utility_count >= 2 else "Base"
    
    # Legacy property names
    @property
    def currProfit(self) -> str:
        """Legacy property name - use current_profit_level instead."""
        return self.current_profit_level
    
    @currProfit.setter
    def currProfit(self, value: str) -> None:
        """Legacy property setter - use current_profit_level instead."""
        self.current_profit_level = value
    
    @property
    def rents(self) -> Dict:
        """Legacy property name - use rent_multipliers instead."""
        return self.rent_multipliers


# Special board spaces that don't function as properties

class FreeParkingSpace(BoardSpace):
    """
    Represents the Free Parking space where tax money accumulates.
    
    This space collects money from taxes and other game events, which is
    awarded to players who land on Free Parking (house rule in many families).
    
    Attributes:
        accumulated_money (int): Amount of money currently in the pot
        ok_button (Button): UI button to collect the money
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize the Free Parking space.
        
        Args:
            screen: The pygame surface for rendering
        """
        super().__init__("Free Parking", screen)
        self.accumulated_money = 0
        
        # Initialize UI button
        button_rect = (OK_BTN_X, OK_BTN_Y, OK_BTN_WIDTH, OK_BTN_HEIGHT)
        self.ok_button = Button(screen, "Ok", BTNFONT, button_rect, GREEN)
    
    def handle_player_landing(self, player) -> None:
        """
        Handle a player landing on Free Parking.
        
        Args:
            player: The player who landed on Free Parking
        """
        self.should_show_ui = True
    
    def render_ui(self) -> None:
        """Render the Free Parking collection interface."""
        if not self.should_show_ui:
            return
        
        # Draw window
        self._draw_standard_window()
        
        # Draw header
        drawText(
            self.screen, self.name, PROPNAMEFONT, BLACK,
            (PROP_NAME_X, PROP_NAME_Y)
        )
        pygame.draw.line(
            self.screen, BLACK, NAME_LN_START, NAME_LN_END, 2
        )
        
        # Draw Free Parking image
        image_rect = FREEPARKINGIMG.get_rect()
        image_rect.center = (FREE_PARKING_X, FREE_PARKING_Y)
        self.screen.blit(FREEPARKINGIMG, image_rect)
        
        # Draw description and amount
        drawText(
            self.screen, "Free Parking!", PROPTXTFONT, BLACK,
            (TAX_TXT_X, TAX_TXT_Y)
        )
        drawText(
            self.screen, f"${self.accumulated_money}", PROPTXTFONT, BLACK,
            (TAX_TXT_X, TAX_TXT_Y + 50)
        )
        
        # Draw OK button
        self.ok_button.draw()
    
    def _draw_standard_window(self) -> None:
        """Draw the standard property-style window."""
        # Border
        border_rect = (
            BUY_WIN_X - 10, BUY_WIN_Y - 10,
            BUY_WIN_WIDTH + 20, BUY_WIN_HEIGHT + 20
        )
        pygame.draw.rect(self.screen, WHITE, border_rect)
        
        # Frame
        frame_rect = (
            BUY_WIN_X - 2, BUY_WIN_Y - 2,
            BUY_WIN_WIDTH + 4, BUY_WIN_HEIGHT + 4
        )
        pygame.draw.rect(self.screen, BLACK, frame_rect)
        
        # Main window
        main_rect = (BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, main_rect)
    
    def collect_money(self, player) -> None:
        """
        Transfer all accumulated money to the player.
        
        Args:
            player: The player collecting the money
        """
        player.receive_money(self.accumulated_money)
        self.accumulated_money = 0
    
    def deposit_money(self, amount: int) -> None:
        """
        Add money to the Free Parking pot.
        
        Args:
            amount: Amount of money to add
        """
        self.accumulated_money += amount
    
    def handle_ok_button_click(self, player) -> None:
        """
        Handle the OK button being clicked.
        
        Args:
            player: The player clicking the button
        """
        self.collect_money(player)
        self.should_show_ui = False
    
    # Legacy method names for backward compatibility
    def pay(self, player) -> None:
        """Legacy method name - use collect_money() instead."""
        self.collect_money(player)
    
    def deposit(self, amount: int) -> None:
        """Legacy method name - use deposit_money() instead."""
        self.deposit_money(amount)
    
    def okBtnAction(self, player) -> None:
        """Legacy method name - use handle_ok_button_click() instead."""
        self.handle_ok_button_click(player)
    
    @property
    def value(self) -> int:
        """Legacy property name - use accumulated_money instead."""
        return self.accumulated_money
    
    @value.setter
    def value(self, amount: int) -> None:
        """Legacy property setter - use accumulated_money instead."""
        self.accumulated_money = amount
    
    @property
    def okBtn(self) -> Button:
        """Legacy property name - use ok_button instead."""
        return self.ok_button


class GoToJailSpace(BoardSpace):
    """
    Represents the "Go To Jail" corner space.
    
    This space immediately sends players to jail without passing Go
    or collecting the usual $200 bonus.
    
    Attributes:
        ok_button (Button): UI button to acknowledge going to jail
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize the Go To Jail space.
        
        Args:
            screen: The pygame surface for rendering
        """
        super().__init__("Go To Jail", screen)
        
        # Initialize UI button
        button_rect = (OK_BTN_X, OK_BTN_Y, OK_BTN_WIDTH, OK_BTN_HEIGHT)
        self.ok_button = Button(screen, "Ok", BTNFONT, button_rect, GREEN)
    
    def handle_player_landing(self, player) -> None:
        """
        Handle a player landing on Go To Jail.
        
        Args:
            player: The player who landed on the space
        """
        self.should_show_ui = True
    
    def render_ui(self) -> None:
        """Render the Go To Jail notification interface."""
        if not self.should_show_ui:
            return
        
        # Draw window
        self._draw_standard_window()
        
        # Draw header
        drawText(
            self.screen, self.name, PROPNAMEFONT, BLACK,
            (PROP_NAME_X, PROP_NAME_Y)
        )
        pygame.draw.line(
            self.screen, BLACK, NAME_LN_START, NAME_LN_END, 2
        )
        
        # Draw Go To Jail image
        image_rect = GOTOJAILIMG.get_rect()
        image_rect.center = (GO_TO_JAIL_X, GO_TO_JAIL_Y)
        self.screen.blit(GOTOJAILIMG, image_rect)
        
        # Draw instructions
        drawText(
            self.screen, "Do Not Pass Go", PROPTXTFONT, BLACK,
            (TAX_TXT_X, TAX_TXT_Y)
        )
        drawText(
            self.screen, "Do Not Collect $200", PROPTXTFONT, BLACK,
            (TAX_TXT_X, TAX_TXT_Y + 50)
        )
        
        # Draw OK button
        self.ok_button.draw()
    
    def _draw_standard_window(self) -> None:
        """Draw the standard property-style window."""
        # Border
        border_rect = (
            BUY_WIN_X - 10, BUY_WIN_Y - 10,
            BUY_WIN_WIDTH + 20, BUY_WIN_HEIGHT + 20
        )
        pygame.draw.rect(self.screen, WHITE, border_rect)
        
        # Frame
        frame_rect = (
            BUY_WIN_X - 2, BUY_WIN_Y - 2,
            BUY_WIN_WIDTH + 4, BUY_WIN_HEIGHT + 4
        )
        pygame.draw.rect(self.screen, BLACK, frame_rect)
        
        # Main window
        main_rect = (BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, main_rect)
    
    def handle_ok_button_click(self, player) -> None:
        """
        Handle the OK button being clicked.
        
        Args:
            player: The player acknowledging they're going to jail
        """
        player.send_to_jail()
        self.should_show_ui = False
    
    # Legacy method names for backward compatibility
    def okBtnAction(self, player) -> None:
        """Legacy method name - use handle_ok_button_click() instead."""
        self.handle_ok_button_click(player)
    
    @property
    def okBtn(self) -> Button:
        """Legacy property name - use ok_button instead."""
        return self.ok_button


class JailSpace(BoardSpace):
    """
    Represents the Jail space where players can be imprisoned.
    
    This space provides options for players to escape jail by paying bail,
    rolling doubles, or using Get Out of Jail Free cards.
    
    Attributes:
        pay_button (Button): UI button to pay bail and escape jail
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize the Jail space.
        
        Args:
            screen: The pygame surface for rendering
        """
        super().__init__("In Jail", screen)
        
        # Initialize UI button
        button_rect = (
            JAIL_TXT_X, JAIL_TXT_Y + 150, PAY_BTN_WIDTH, PAY_BTN_HEIGHT
        )
        self.pay_button = Button(screen, "Pay", BTNFONT, button_rect, GREEN)
    
    def handle_player_landing(self, player) -> None:
        """
        Handle a player being in jail (not landing, but being there).
        
        Args:
            player: The player currently in jail
        """
        if player.is_in_jail:
            self.should_show_ui = True
    
    def render_ui(self) -> None:
        """Render the jail interface with escape options."""
        if not self.should_show_ui:
            return
        
        # Draw jail window
        self._draw_jail_window()
        
        # Draw header
        drawText(
            self.screen, self.name, PROPNAMEFONT, BLACK,
            (PROP_NAME_X, PROP_NAME_Y)
        )
        pygame.draw.line(
            self.screen, BLACK, NAME_LN_START, NAME_LN_END, 2
        )
        
        # Draw escape options
        drawText(
            self.screen, "Roll a Double", PROPTXTFONT, BLACK,
            (JAIL_TXT_X, JAIL_TXT_Y)
        )
        drawText(
            self.screen, "Or Pay Bail ($50)", PROPTXTFONT, BLACK,
            (JAIL_TXT_X, JAIL_TXT_Y + 50)
        )
        
        # Draw pay button
        self.pay_button.draw()
    
    def _draw_jail_window(self) -> None:
        """Draw the jail-specific window."""
        # Border
        border_rect = (
            IN_JAIL_WIN_X - 10, IN_JAIL_WIN_Y - 10,
            IN_JAIL_WIN_WIDTH + 20, IN_JAIL_WIN_HEIGHT + 20
        )
        pygame.draw.rect(self.screen, WHITE, border_rect)
        
        # Frame
        frame_rect = (
            IN_JAIL_WIN_X - 2, IN_JAIL_WIN_Y - 2,
            IN_JAIL_WIN_WIDTH + 4, IN_JAIL_WIN_HEIGHT + 4
        )
        pygame.draw.rect(self.screen, BLACK, frame_rect)
        
        # Main window
        main_rect = (
            IN_JAIL_WIN_X, IN_JAIL_WIN_Y, IN_JAIL_WIN_WIDTH, IN_JAIL_WIN_HEIGHT
        )
        pygame.draw.rect(self.screen, WHITE, main_rect)
    
    def handle_pay_button_click(self, player) -> None:
        """
        Handle the pay bail button being clicked.
        
        Args:
            player: The player paying bail
        """
        player.pay_jail_bail()
        self.should_show_ui = False
    
    # Legacy method names for backward compatibility
    def payBtnAction(self, player) -> None:
        """Legacy method name - use handle_pay_button_click() instead."""
        self.handle_pay_button_click(player)
    
    @property
    def payBtn(self) -> Button:
        """Legacy property name - use pay_button instead."""
        return self.pay_button


class TaxSpace(BoardSpace):
    """
    Represents a tax space that charges players a fixed amount.
    
    Tax spaces deduct money from players and typically deposit it
    into the Free Parking pot (house rule).
    
    Attributes:
        tax_amount (int): The amount of tax to charge
        ok_button (Button): UI button to acknowledge paying the tax
    """
    
    def __init__(self, name: str, screen: pygame.Surface) -> None:
        """
        Initialize a tax space.
        
        Args:
            name: The name of the tax space
            screen: The pygame surface for rendering
        """
        super().__init__(name, screen)
        self.tax_amount = TAXPRICES[self.name]
        
        # Initialize UI button
        button_rect = (OK_BTN_X, OK_BTN_Y, OK_BTN_WIDTH, OK_BTN_HEIGHT)
        self.ok_button = Button(screen, "Ok", BTNFONT, button_rect, GREEN)
    
    def handle_player_landing(self, player) -> None:
        """
        Handle a player landing on the tax space.
        
        Args:
            player: The player who landed on the tax space
        """
        self.should_show_ui = True
    
    def render_ui(self) -> None:
        """Render the tax payment interface."""
        if not self.should_show_ui:
            return
        
        # Draw window
        self._draw_standard_window()
        
        # Draw header
        drawText(
            self.screen, self.name, PROPNAMEFONT, BLACK,
            (PROP_NAME_X, PROP_NAME_Y)
        )
        pygame.draw.line(
            self.screen, BLACK, NAME_LN_START, NAME_LN_END, 2
        )
        
        # Draw tax image
        tax_image = TAXIMGS[self.name]
        image_rect = tax_image.get_rect()
        image_rect.center = (INCOME_TAX_X, INCOME_TAX_Y)
        self.screen.blit(tax_image, image_rect)
        
        # Draw tax amount
        tax_text = f"pay ${self.tax_amount}"
        drawText(
            self.screen, tax_text, PROPTXTFONT, BLACK,
            (TAX_TXT_X, TAX_TXT_Y)
        )
        
        # Draw OK button
        self.ok_button.draw()
    
    def _draw_standard_window(self) -> None:
        """Draw the standard property-style window."""
        # Border
        border_rect = (
            BUY_WIN_X - 10, BUY_WIN_Y - 10,
            BUY_WIN_WIDTH + 20, BUY_WIN_HEIGHT + 20
        )
        pygame.draw.rect(self.screen, WHITE, border_rect)
        
        # Frame
        frame_rect = (
            BUY_WIN_X - 2, BUY_WIN_Y - 2,
            BUY_WIN_WIDTH + 4, BUY_WIN_HEIGHT + 4
        )
        pygame.draw.rect(self.screen, BLACK, frame_rect)
        
        # Main window
        main_rect = (BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, main_rect)
    
    def collect_tax(self, player) -> int:
        """
        Collect tax from the player.
        
        Args:
            player: The player to charge tax
            
        Returns:
            The amount of tax collected
        """
        if player.money >= self.tax_amount:
            player.deduct_money(self.tax_amount)
            return self.tax_amount
        else:
            # Player doesn't have enough money - collect what they have
            remaining_money = player.money
            player.deduct_money(remaining_money)
            return remaining_money
    
    def handle_ok_button_click(self, player) -> int:
        """
        Handle the OK button being clicked.
        
        Args:
            player: The player acknowledging the tax payment
            
        Returns:
            The amount of tax collected
        """
        self.should_show_ui = False
        return self.collect_tax(player)
    
    # Legacy method names for backward compatibility
    def charge(self, player) -> int:
        """Legacy method name - use collect_tax() instead."""
        return self.collect_tax(player)
    
    def okBtnAction(self, player) -> int:
        """Legacy method name - use handle_ok_button_click() instead."""
        return self.handle_ok_button_click(player)
    
    @property
    def price(self) -> int:
        """Legacy property name - use tax_amount instead."""
        return self.tax_amount
    
    @property
    def okBtn(self) -> Button:
        """Legacy property name - use ok_button instead."""
        return self.ok_button


class CardSpace(BoardSpace):
    """
    Represents a Chance or Community Chest card space.
    
    These spaces draw cards from their respective decks and execute
    the card's effects on the game state.
    
    Attributes:
        card_deck (Union[ChanceDeck, CommunityChestDeck]): The deck to draw from
        current_card (Union[ChanceCard, CommunityChestCard]): The currently drawn card
        ok_button (Button): UI button to acknowledge the card effect
    """
    
    def __init__(self, name: str, screen: pygame.Surface) -> None:
        """
        Initialize a card space.
        
        Args:
            name: The name of the card space
            screen: The pygame surface for rendering
        """
        super().__init__(name, screen)
        
        # Create appropriate deck and draw initial card
        self._create_card_deck()
        self.current_card = self.card_deck.deal_card()
        
        # Initialize UI button
        button_rect = (
            JAIL_TXT_X, JAIL_TXT_Y + 150, PAY_BTN_WIDTH, PAY_BTN_HEIGHT
        )
        self.ok_button = Button(screen, "Ok", BTNFONT, button_rect, GREEN)
    
    def _create_card_deck(self) -> None:
        """Create the appropriate card deck based on the space name."""
        if "Chance" in self.name:
            self.card_deck = ChanceDeck(self.screen)
        elif "Community Chest" in self.name:
            self.card_deck = CommunityChestDeck(self.screen)
        else:
            # Fallback - this shouldn't happen
            self.card_deck = ChanceDeck(self.screen)
    
    def handle_player_landing(self, player) -> None:
        """
        Handle a player landing on the card space.
        
        Args:
            player: The player who landed on the space
        """
        self.should_show_ui = True
        # Note: Card effect is executed when OK button is clicked
    
    def render_ui(self) -> None:
        """Render the card display interface."""
        if not self.should_show_ui:
            return
        
        # Draw card window
        self._draw_card_window()
        
        # Draw card title
        card_title = self._get_card_title()
        drawText(
            self.screen, card_title, PROPNAMEFONT, BLACK,
            (PROP_NAME_X, PROP_NAME_Y)
        )
        pygame.draw.line(
            self.screen, BLACK, NAME_LN_START, NAME_LN_END, 2
        )
        
        # Draw card description
        drawTextMultiLines(
            self.screen, self.current_card.description, PROPTXTFONT, BLACK,
            (JAIL_TXT_X, JAIL_TXT_Y), 30
        )
        
        # Draw OK button
        self.ok_button.draw()
    
    def _draw_card_window(self) -> None:
        """Draw the card-specific window."""
        # Border
        border_rect = (
            IN_JAIL_WIN_X - 10, IN_JAIL_WIN_Y - 10,
            IN_JAIL_WIN_WIDTH + 20, IN_JAIL_WIN_HEIGHT + 20
        )
        pygame.draw.rect(self.screen, WHITE, border_rect)
        
        # Frame
        frame_rect = (
            IN_JAIL_WIN_X - 2, IN_JAIL_WIN_Y - 2,
            IN_JAIL_WIN_WIDTH + 4, IN_JAIL_WIN_HEIGHT + 4
        )
        pygame.draw.rect(self.screen, BLACK, frame_rect)
        
        # Main window
        main_rect = (
            IN_JAIL_WIN_X, IN_JAIL_WIN_Y, IN_JAIL_WIN_WIDTH, IN_JAIL_WIN_HEIGHT
        )
        pygame.draw.rect(self.screen, WHITE, main_rect)
    
    def _get_card_title(self) -> str:
        """
        Get the appropriate title for the current card.
        
        Returns:
            "Chance" or "Community Chest" based on card type
        """
        if isinstance(self.current_card, ChanceCard):
            return "Chance"
        else:
            return "Community Chest"
    
    def handle_ok_button_click(self, players: List) -> None:
        """
        Handle the OK button being clicked.
        
        Args:
            players: List of all players in the game
        """
        # Execute the card's effect
        self.current_card.execute_action(players)
        
        # Draw a new card for next time
        self.current_card = self.card_deck.deal_card()
        
        # Hide the UI
        self.should_show_ui = False
    
    # Legacy method names for backward compatibility
    def createDeck(self) -> None:
        """Legacy method name - use _create_card_deck() instead."""
        self._create_card_deck()
    
    def okBtnAction(self, players: List) -> None:
        """Legacy method name - use handle_ok_button_click() instead."""
        self.handle_ok_button_click(players)
    
    @property
    def deck(self):
        """Legacy property name - use card_deck instead."""
        return self.card_deck
    
    @property
    def currCard(self):
        """Legacy property name - use current_card instead."""
        return self.current_card
    
    @currCard.setter
    def currCard(self, value) -> None:
        """Legacy property setter - use current_card instead."""
        self.current_card = value
    
    @property
    def okBtn(self) -> Button:
        """Legacy property name - use ok_button instead."""
        return self.ok_button


class EmptySpace(BoardSpace):
    """
    Represents spaces that have no special effect (like Go, Just Visiting).
    
    These spaces don't trigger any actions when players land on them.
    They serve as neutral positions on the board.
    """
    
    def __init__(self, name: str, screen: pygame.Surface) -> None:
        """
        Initialize an empty space.
        
        Args:
            name: The name of the space
            screen: The pygame surface for rendering
        """
        super().__init__(name, screen)
        self.should_show_ui = False  # Empty spaces don't show UI
    
    def handle_player_landing(self, player) -> None:
        """
        Handle a player landing on an empty space.
        
        Args:
            player: The player who landed on the space (no effect)
        """
        pass  # Empty spaces do nothing
    
    def render_ui(self) -> None:
        """Empty spaces have no UI to render."""
        pass


class BoardSpaceFactory:
    """
    Factory class for creating all board spaces in the Monopoly game.
    
    This class centralizes the creation of all board spaces and maintains
    a registry of all spaces for easy access during gameplay.
    
    Attributes:
        spaces (Dict[str, BoardSpace]): Dictionary mapping space names to objects
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize the factory and create all board spaces.
        
        Args:
            screen: The pygame surface for rendering
        """
        self.spaces = self._create_all_spaces(screen)
    
    def _create_all_spaces(self, screen: pygame.Surface) -> Dict[str, BoardSpace]:
        """
        Create all board spaces for the Monopoly game.
        
        Args:
            screen: The pygame surface for rendering
            
        Returns:
            Dictionary mapping space names to BoardSpace objects
        """
        spaces = {}
        
        # Create color set properties
        for property_name in PROPERTIES:
            spaces[property_name] = ColorSetProperty(property_name, screen)
        
        # Create railroad properties
        for railroad_name in RAILROADS:
            spaces[railroad_name] = RailroadProperty(railroad_name, screen)
        
        # Create utility properties
        for utility_name in UTILS:
            spaces[utility_name] = UtilityProperty(utility_name, screen)
        
        # Create tax spaces
        for tax_name in TAXES:
            spaces[tax_name] = TaxSpace(tax_name, screen)
        
        # Create card spaces
        for card_space_name in CARDSPACES:
            spaces[card_space_name] = CardSpace(card_space_name, screen)
        
        # Create empty spaces (Go, Just Visiting)
        for empty_space_name in FREESPACES:
            spaces[empty_space_name] = EmptySpace(empty_space_name, screen)
        
        # Create special spaces
        spaces["Free Parking"] = FreeParkingSpace(screen)
        spaces["Go To Jail"] = GoToJailSpace(screen)
        spaces["In Jail"] = JailSpace(screen)
        
        return spaces
    
    def get_space(self, name: str) -> Optional[BoardSpace]:
        """
        Get a board space by name.
        
        Args:
            name: The name of the space to retrieve
            
        Returns:
            The BoardSpace object, or None if not found
        """
        return self.spaces.get(name)
    
    def print_all_spaces(self) -> None:
        """Print all spaces for debugging purposes."""
        for space_name, space_obj in self.spaces.items():
            print(f"{space_name}: {space_obj}")
    
    # Legacy method names for backward compatibility
    def createProperties(self, screen: pygame.Surface) -> Dict[str, BoardSpace]:
        """Legacy method name - use _create_all_spaces() instead."""
        return self._create_all_spaces(screen)
    
    def print(self) -> None:
        """Legacy method name - use print_all_spaces() instead."""
        self.print_all_spaces()
    
    @property
    def properties(self) -> Dict[str, BoardSpace]:
        """Legacy property name - use spaces instead."""
        return self.spaces


# Legacy class names for backward compatibility

class Cell(BoardSpace):
    """Legacy class name - use BoardSpace instead."""
    pass


class ColorSet(ColorSetProperty):
    """Legacy class name - use ColorSetProperty instead."""
    pass


class Railroad(RailroadProperty):
    """Legacy class name - use RailroadProperty instead."""
    pass


class Utility(UtilityProperty):
    """Legacy class name - use UtilityProperty instead."""
    pass


class FreeParking(FreeParkingSpace):
    """Legacy class name - use FreeParkingSpace instead."""
    pass


class GoToJail(GoToJailSpace):
    """Legacy class name - use GoToJailSpace instead."""
    pass


class Jail(JailSpace):
    """Legacy class name - use JailSpace instead."""
    pass


class Tax(TaxSpace):
    """Legacy class name - use TaxSpace instead."""
    pass


class Card(CardSpace):
    """Legacy class name - use CardSpace instead."""
    pass


class DoNothings(EmptySpace):
    """Legacy class name - use EmptySpace instead."""
    pass


class Cells(BoardSpaceFactory):
    """Legacy class name - use BoardSpaceFactory instead."""
    pass