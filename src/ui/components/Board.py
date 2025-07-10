"""
Monopoly Game Board Display Module

This module handles the visual display of the Monopoly game board.
It manages board positioning, centering, and rendering to ensure the
board is properly displayed in the center of the game window.

Author: Aidan Sabatini
"""

# Standard library imports
from typing import Tuple

# Third-party imports
import pygame

# Local application imports
from src.config.displayAssets import BOARD_WIDTH, BOARD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT
from src.config.colorAssets import BLACK
from src.config.imgAssets import BOARDIMG

# Initialize Pygame
pygame.init()


class Board:
    """
    Manages the visual display of the Monopoly game board.
    
    This class handles the positioning and rendering of the main game board
    image. It automatically centers the board on the screen and provides
    a border for visual appeal.
    
    Attributes:
        screen (pygame.Surface): The game display surface
        board_width (int): Width of the board in pixels
        board_height (int): Height of the board in pixels
        board_x (int): X coordinate of the board's top-left corner
        board_y (int): Y coordinate of the board's top-left corner
        board_image (pygame.Surface): The board image to display
    """
    
    # Display constants
    BORDER_WIDTH = 5  # Width of the border around the board
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize the board with positioning and image data.
        
        Args:
            screen: The pygame surface to render the board on
        """
        self.screen = screen
        
        # Board dimensions
        self.board_width = BOARD_WIDTH
        self.board_height = BOARD_HEIGHT
        
        # Calculate board position (centered on screen)
        self.board_x, self.board_y = self._calculate_board_position()
        
        # Load board image
        self.board_image = BOARDIMG
    
    def _calculate_screen_center(self) -> Tuple[int, int]:
        """
        Calculate the center point of the game screen.
        
        Returns:
            Tuple containing (center_x, center_y) coordinates
        """
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        return (center_x, center_y)
    
    def _calculate_board_position(self) -> Tuple[int, int]:
        """
        Calculate the top-left position for centering the board on screen.
        
        This method determines where to place the board so that it appears
        centered within the game window.
        
        Returns:
            Tuple containing (x, y) coordinates for the board's top-left corner
        """
        center_x, center_y = self._calculate_screen_center()
        
        # Calculate top-left position to center the board
        board_x = center_x - (self.board_width // 2)
        board_y = center_y - (self.board_height // 2)
        
        return (board_x, board_y)
    
    def render(self) -> None:
        """
        Render the game board to the screen.
        
        This method draws the board with a decorative border for visual appeal.
        The board is automatically positioned in the center of the screen.
        """
        # Draw border rectangle
        border_rect = (
            self.board_x - self.BORDER_WIDTH,
            self.board_y - self.BORDER_WIDTH,
            self.board_width + (2 * self.BORDER_WIDTH),
            self.board_height + (2 * self.BORDER_WIDTH)
        )
        pygame.draw.rect(self.screen, BLACK, border_rect)
        
        # Draw the main board image
        self.screen.blit(self.board_image, (self.board_x, self.board_y))
    
    def get_board_bounds(self) -> Tuple[int, int, int, int]:
        """
        Get the bounding rectangle of the board.
        
        Returns:
            Tuple containing (x, y, width, height) of the board area
        """
        return (self.board_x, self.board_y, self.board_width, self.board_height)
    
    def get_board_center(self) -> Tuple[int, int]:
        """
        Get the center point of the board.
        
        Returns:
            Tuple containing (center_x, center_y) coordinates of the board
        """
        center_x = self.board_x + (self.board_width // 2)
        center_y = self.board_y + (self.board_height // 2)
        return (center_x, center_y)
    
    def is_point_on_board(self, x: int, y: int) -> bool:
        """
        Check if a point is within the board area.
        
        Args:
            x: X coordinate to check
            y: Y coordinate to check
            
        Returns:
            True if the point is within the board bounds, False otherwise
        """
        return (self.board_x <= x <= self.board_x + self.board_width and
                self.board_y <= y <= self.board_y + self.board_height)
    
    # Legacy method names for backward compatibility
    def findCenter(self) -> Tuple[int, int]:
        """Legacy method name - use _calculate_screen_center() instead."""
        return self._calculate_screen_center()
    
    def findBoardCoord(self) -> Tuple[int, int]:
        """Legacy method name - use _calculate_board_position() instead."""
        return self._calculate_board_position()
    
    def display(self) -> None:
        """Legacy method name - use render() instead."""
        self.render()
    
    # Legacy property names
    @property
    def width(self) -> int:
        """Legacy property name - use board_width instead."""
        return self.board_width
    
    @property
    def height(self) -> int:
        """Legacy property name - use board_height instead."""
        return self.board_height
    
    @property
    def x(self) -> int:
        """Legacy property name - use board_x instead."""
        return self.board_x
    
    @property
    def y(self) -> int:
        """Legacy property name - use board_y instead."""
        return self.board_y
    
    @property
    def image(self) -> pygame.Surface:
        """Legacy property name - use board_image instead."""
        return self.board_image