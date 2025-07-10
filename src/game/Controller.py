"""
Monopoly Game Controller Module

This module contains the main Game class that controls the core game loop,
event handling, and game state management for the Monopoly board game.

Author: Aidan Sabatini
"""

# Standard library imports
import random
from time import sleep
from typing import List, Optional, Union

# Third-party imports
import pygame

# Local application imports
from src.game.Player import Player
from src.game.Dice import DiceSet
from src.game.Cards import Card
from src.game.Properties import (
    Cells, Property, FreeParking, GoToJail, Tax, Jail
)
from src.ui.menus.BuildMenu import BuildMenu
from src.ui.menus.TradeMenu import TradeMenu
from src.config.colorAssets import GREEN, RED
from src.config.displayAssets import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    NXT_TURN_BTN_X, NXT_TURN_BTN_Y, NXT_TURN_BTN_WIDTH, NXT_TURN_BTN_HEIGHT
)
from src.config.fontAssets import BTNFONT
from src.config.imgAssets import ST_PIECE_IMGS
from src.config.boardAssets import FREESPACES
from src.ui.components.Button import Button
from src.ui.components.StartupWindow import StartupWindow
from src.ui.components.Board import Board

# Initialize Pygame
pygame.init()


class Game:
    """
    Main game controller class for the Monopoly board game.
    
    This class manages the entire game state, including player management,
    game loop execution, event handling, and UI coordination. It serves as
    the central hub connecting all game components.
    
    Attributes:
        screen (pygame.Surface): The main game display surface
        board (Board): The game board display component
        dice_set (DiceSet): The dice rolling mechanism
        startup_window (StartupWindow): Player setup interface
        board_spaces (Cells): All board spaces and properties
        build_menu (BuildMenu): House/hotel building interface
        trade_menu (TradeMenu): Player trading interface
        players (List[Player]): All players in the game
        current_turn (Optional[Player]): Player whose turn it currently is
        current_turn_location (Optional): Current player's board location
        display_dice (bool): Whether dice should be displayed
        dice_rolled (bool): Whether dice have been rolled this turn
        next_turn_button (Button): Button to advance to next turn
    """
    
    # Game constants
    SLEEP_DURATION = 1.0  # Seconds to pause after dice roll
    MIN_PLAYERS = 2       # Minimum players to start game
    MAX_PLAYERS = 4       # Maximum players allowed
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize the game with all necessary components.
        
        Args:
            screen: The pygame surface to render the game on
        """
        self.screen = screen
        
        # Initialize game components
        self._initialize_game_components()
        self._initialize_game_state()
        self._initialize_ui_components()
        
        # Set window properties
        pygame.display.set_caption("Monopoly")
    
    def _initialize_game_components(self) -> None:
        """Initialize core game components like board, dice, and spaces."""
        self.board = Board(self.screen)
        self.dice_set = DiceSet(self.screen)
        self.board_spaces = Cells(self.screen)
    
    def _initialize_game_state(self) -> None:
        """Initialize game state variables."""
        self.players: List[Player] = []
        self.current_turn: Optional[Player] = None
        self.current_turn_location: Optional[Union[Property, Card, Tax, Jail]] = None
        self.display_dice = False
        self.dice_rolled = False
    
    def _initialize_ui_components(self) -> None:
        """Initialize user interface components."""
        self.startup_window = StartupWindow(self.screen, ST_PIECE_IMGS)
        self.build_menu = BuildMenu(self.screen)
        self.trade_menu = TradeMenu(self.screen)
        
        # Create next turn button
        button_rect = (
            NXT_TURN_BTN_X, NXT_TURN_BTN_Y, 
            NXT_TURN_BTN_WIDTH, NXT_TURN_BTN_HEIGHT
        )
        self.next_turn_button = Button(
            self.screen, "End Turn", BTNFONT, button_rect, RED
        )
    
    def loop(self) -> None:
        """
        Execute the main game loop.
        
        This is the primary game loop that handles events, updates game state,
        and renders the display. The loop continues until the user quits.
        """
        running = True
        
        while running:
            # Process all pygame events
            for event in pygame.event.get():
                if self._is_quit_event(event):
                    running = False
                
                self._handle_keyboard_input(event)
                self._handle_mouse_input(event)
            
            # Update game state
            self._handle_dice_display()
            self._update_current_turn_location()
            self._update_property_interactions()
            
            # Render everything to screen
            self._render_display()
            pygame.display.flip()
    
    def test_loop(self) -> None:
        """
        Execute a test version of the game loop with pre-configured players.
        
        This method sets up a test scenario with two players and some
        pre-purchased properties for development and debugging purposes.
        """
        # Set up test players
        self.add_player("Aidan", 0, 2)
        self.add_player("Piv", 1, 3)
        
        # Pre-purchase some properties for testing
        self._setup_test_properties()
        
        # Start the game and run the main loop
        self.start_game()
        self.loop()
    
    def _setup_test_properties(self) -> None:
        """Set up pre-purchased properties for testing purposes."""
        player1, player2 = self.players[0], self.players[1]
        
        # Player 1 properties
        test_properties_p1 = [
            "Connecticut Avenue", "Vermont Avenue", "Oriental Avenue",
            "Marvin Gardens", "Pennsylvania Railroad"
        ]
        
        # Player 2 properties  
        test_properties_p2 = [
            "States Avenue", "St. Charles Place", 
            "Virginia Avenue", "Boardwalk"
        ]
        
        for prop_name in test_properties_p1:
            self.board_spaces.properties[prop_name].buy(player1)
            
        for prop_name in test_properties_p2:
            self.board_spaces.properties[prop_name].buy(player2)
    
    def _handle_keyboard_input(self, event: pygame.event.Event) -> None:
        """
        Handle keyboard input events.
        
        Args:
            event: The pygame event to process
        """
        if event.type != pygame.KEYDOWN:
            return
        
        # Handle name input during startup
        if self.startup_window.isStartup:
            self.startup_window.nameInputBox.handle_event(event)
            return
        
        # Handle dice rolling with spacebar
        if (event.key == pygame.K_SPACE and 
            self.dice_set.isDisplayed and 
            not self.current_turn_location.show):
            
            self._handle_dice_roll()
    
    def _handle_dice_roll(self) -> None:
        """Handle the dice rolling logic for the current player."""
        if not self.current_turn.inJail:
            # Normal dice roll and movement
            roll_result = self.dice_set.roll()
            self.current_turn.move(roll_result)
        else:
            # Jail turn handling
            self.dice_set.roll()
            self.current_turn.jailTurn(self.dice_set)
        
        sleep(self.SLEEP_DURATION)
        self.dice_rolled = True
    
    def _handle_mouse_input(self, event: pygame.event.Event) -> None:
        """
        Handle mouse click events.
        
        Args:
            event: The pygame event to process
        """
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Always check startup window input first
        self._handle_startup_window_input()
        
        # Handle next turn button
        if self.next_turn_button.isClicked(mouse_pos):
            self.advance_turn()
        
        # Handle game-specific clicks only if we have a current location
        if self.current_turn_location is not None:
            self._handle_game_clicks(mouse_pos)
    
    def _handle_game_clicks(self, mouse_pos: tuple) -> None:
        """
        Handle clicks during active gameplay.
        
        Args:
            mouse_pos: The (x, y) coordinates of the mouse click
        """
        # Handle building menu
        self._handle_build_menu_clicks(mouse_pos)
        
        # Handle trade menu
        self._handle_trade_menu_clicks(mouse_pos)
        
        # Handle property-specific clicks
        self._handle_property_clicks(mouse_pos)
        
        # Handle special space clicks
        self._handle_special_space_clicks(mouse_pos)
    
    def _handle_build_menu_clicks(self, mouse_pos: tuple) -> None:
        """Handle building menu related clicks."""
        if self.build_menu.activateBtn.isClicked(mouse_pos):
            self.build_menu.activateBtnAction()
        
        if self.build_menu.displayWin:
            if self.build_menu.closeBtn.isClicked(mouse_pos):
                self.build_menu.closeBtnAction()
            self.build_menu.checkBtnClicks(self.current_turn, mouse_pos)
    
    def _handle_trade_menu_clicks(self, mouse_pos: tuple) -> None:
        """Handle trade menu related clicks."""
        if self.trade_menu.activateBtn.isClicked(mouse_pos):
            self.trade_menu.activateBtnAction()
        
        if self.trade_menu.displayWin:
            if self.trade_menu.closeBtn.isClicked(mouse_pos):
                self.trade_menu.closeBtnAction()
            self.trade_menu.checkBtnClicks(self.current_turn, mouse_pos)
    
    def _handle_property_clicks(self, mouse_pos: tuple) -> None:
        """Handle property-specific clicks like buying and auctioning."""
        if not isinstance(self.current_turn_location, Property):
            return
        
        prop = self.current_turn_location
        
        # Handle auction interactions
        if prop.auction is not None:
            if prop.auction.bidBtn.isClicked(mouse_pos):
                prop.auction.bidBtnAction()
            elif prop.auction.withdrawBtn.isClicked(mouse_pos):
                prop.auction.withdrawBtnAction()
        
        # Handle buy/auction buttons
        if prop.buyBtn.isClicked(mouse_pos):
            if prop.canBuy(self.current_turn):
                prop.buyBtnAction(self.current_turn)
        elif prop.auctionBtn.isClicked(mouse_pos):
            prop.auctionBtnAction(self.players)
    
    def _handle_special_space_clicks(self, mouse_pos: tuple) -> None:
        """Handle clicks on special board spaces."""
        location = self.current_turn_location
        
        # Handle Free Parking and Go To Jail
        if isinstance(location, (FreeParking, GoToJail)):
            if location.okBtn.isClicked(mouse_pos):
                location.okBtnAction(self.current_turn)
        
        # Handle Card spaces (Chance/Community Chest)
        elif isinstance(location, Card):
            if location.okBtn.isClicked(mouse_pos):
                location.okBtnAction(self.players)
        
        # Handle Tax spaces
        elif isinstance(location, Tax):
            if location.okBtn.isClicked(mouse_pos):
                tax_amount = location.okBtnAction(self.current_turn)
                self.board_spaces.properties["Free Parking"].deposit(tax_amount)
        
        # Handle Jail space
        elif isinstance(location, Jail):
            if location.payBtn.isClicked(mouse_pos):
                location.payBtnAction(self.current_turn)
    
    def _update_property_interactions(self) -> None:
        """Update property-related interactions and charges."""
        if not isinstance(self.current_turn_location, Property):
            return
        
        prop = self.current_turn_location
        prop.update(self.players)
        
        if prop.show:
            if prop.canCharge(self.current_turn):
                prop.charge(self.current_turn)
                prop.show = False
            elif prop in self.current_turn.properties:
                prop.show = False
    
    def _handle_startup_window_input(self) -> None:
        """Handle input events for the startup window."""
        if not self.startup_window.isStartup:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle close button
        if self.startup_window.closeBtn.isClicked(mouse_pos):
            if len(self.players) >= self.MIN_PLAYERS:
                self.start_game()
        
        # Handle add player button
        if self.startup_window.addBtn.isClicked(mouse_pos):
            self._try_add_player()
        
        # Handle input box and piece selection
        self.startup_window.nameInputBox.isClicked(mouse_pos)
        self.startup_window.selectedPiece = self.startup_window.isPieceClicked(mouse_pos)
    
    def _try_add_player(self) -> None:
        """Attempt to add a new player if conditions are met."""
        name = self.startup_window.nameInputBox.text
        selected_piece = self.startup_window.selectedPiece
        
        # Validate input
        if (name and 
            selected_piece is not None and 
            len(self.players) < self.MAX_PLAYERS):
            
            # Add the player
            self.add_player(name, len(self.players), selected_piece)
            
            # Update startup window
            self.startup_window.PieceImages[selected_piece] = None
            self.startup_window = StartupWindow(
                self.screen, self.startup_window.PieceImages
            )
    
    def _handle_dice_display(self) -> None:
        """Manage when dice should be displayed or hidden."""
        self.display_dice = self._should_display_dice()
        
        # Show dice when needed
        if self.display_dice and not self.dice_set.isDisplayed:
            self.dice_set.toggle()
        
        # Hide dice after rolling
        if self.dice_rolled:
            self.display_dice = False
            if self.dice_set.isDisplayed:
                if (self.current_turn.inJail or 
                    not self.current_turn_location.show):
                    self.dice_set.toggle()
    
    def _should_display_dice(self) -> bool:
        """
        Determine if dice should be displayed.
        
        Returns:
            bool: True if dice should be shown, False otherwise
        """
        if self.current_turn is None:
            return False
        
        if self.dice_rolled:
            return False
        
        if (self.current_turn.inJail or 
            self.current_turn.location[0] == "Go"):
            return True
        
        if self.current_turn_location and self.current_turn_location.show:
            return False
        
        return True
    
    def _update_current_turn_location(self) -> None:
        """Update the current turn location reference."""
        if self.current_turn is not None:
            location_name = self.current_turn.location[0]
            self.current_turn_location = self.board_spaces.properties[location_name]
    
    def _display_property_window(self) -> None:
        """Display property information window when appropriate."""
        should_display = (
            self.current_turn is not None and 
            self.dice_rolled
        )
        
        if should_display:
            self.current_turn_location.display()
    
    def _is_quit_event(self, event: pygame.event.Event) -> bool:
        """
        Check if the event is a quit event.
        
        Args:
            event: The pygame event to check
            
        Returns:
            bool: True if this is a quit event, False otherwise
        """
        return (event.type == pygame.QUIT or 
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE))
    
    def add_player(self, name: str, player_id: int, piece: int) -> None:
        """
        Add a new player to the game.
        
        Args:
            name: The player's name
            player_id: Unique identifier for the player
            piece: The piece/token the player will use
        """
        new_player = Player(self.screen, name, player_id, piece)
        self.players.append(new_player)
    
    def _pick_starting_player(self) -> None:
        """Randomly select which player goes first."""
        starting_player = random.choice(self.players)
        starting_player.giveTurn()
        self.current_turn = starting_player
    
    def advance_turn(self) -> None:
        """
        Advance to the next player's turn.
        
        This method handles the transition between players, including
        updating turn status and preparing for the next player's actions.
        """
        # Show current location if not a free space
        if self.current_turn_location.name not in FREESPACES:
            self.current_turn_location.show = True
        
        # Remove turn from current player
        self.current_turn.removeTurn()
        
        # Determine next player
        next_player_id = (self.current_turn.id + 1) % len(self.players)
        self.current_turn = self.players[next_player_id]
        
        # Give turn to next player
        self.current_turn.giveTurn()
        
        # Update location and reset turn state
        self._update_current_turn_location()
        self.current_turn_location.show = False
        self.dice_rolled = False
        self.display_dice = self._should_display_dice()
        
        # Handle bankruptcy (recursive call if needed)
        if self.current_turn.isBankrupt:
            self.advance_turn()
    
    def start_game(self) -> None:
        """
        Start the game by closing startup window and picking first player.
        """
        self.startup_window.isStartup = False
        self._pick_starting_player()
        self._update_current_turn_location()
    
    def send_player_to_jail(self, player: Player) -> None:
        """
        Send a player to jail.
        
        Args:
            player: The player to send to jail
        """
        player.sendToJail()
        self.dice_rolled = True
        self.current_turn_location.show = False
    
    def _render_display(self) -> None:
        """
        Render all game elements to the screen.
        
        This method coordinates the rendering of all visual elements
        in the correct order to create the complete game display.
        """
        # Clear screen with background color
        self.screen.fill(GREEN)
        
        # Render player properties
        for player in self.players:
            player.displayProperties()
        
        # Render game board and dice
        self.board.display()
        self.dice_set.display()
        
        # Render players
        for player in self.players:
            player.playerBanner.draw()
            player.playerPiece.draw()
        
        # Render startup window if active
        if self.startup_window.isStartup:
            self.startup_window.display()
        
        # Render menus if game is active
        if self.current_turn is not None:
            self.build_menu.display(self.players, self.current_turn)
            self.trade_menu.display(self.players, self.current_turn)
        
        # Render active auctions
        self._render_auctions()
        
        # Render next turn button when appropriate
        if self.dice_rolled and not self.current_turn_location.show:
            self.next_turn_button.draw()
        
        # Render property window
        self._display_property_window()
    
    def _render_auctions(self) -> None:
        """Render any active property auctions."""
        for prop in self.board_spaces.properties.values():
            if (isinstance(prop, Property) and 
                prop.auction is not None and 
                prop.auction.isRunning):
                prop.auction.display()