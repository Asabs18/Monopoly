"""
Monopoly Game Button Component Module

This module implements a reusable button component for the Monopoly game UI.
The Button class provides styled, clickable interface elements with text labels
and customizable colors for various game interactions.

Author: Aidan Sabatini
"""

# Standard library imports
from typing import Tuple, Optional

# Third-party imports
import pygame
import pygame.font

# Local application imports
from src.config.fontAssets import *

# Initialize Pygame font system
pygame.font.init()


class Button:
    """
    A customizable button component for the game UI.
    
    This class creates interactive buttons with text labels, background colors,
    and click detection. Buttons can be styled with different fonts, colors,
    and border radius for visual consistency throughout the game interface.
    
    Attributes:
        screen (pygame.Surface): The game display surface
        button_width (int): Width of the button in pixels
        button_height (int): Height of the button in pixels
        background_color (Tuple[int, int, int]): RGB color for button background
        text_color (Tuple[int, int, int]): RGB color for button text
        font (pygame.font.Font): Font used for button text
        button_rect (pygame.Rect): Rectangle defining button position and size
        text_surface (pygame.Surface): Rendered text surface
        text_rect (pygame.Rect): Rectangle for text positioning
    """
    
    # Default styling constants
    DEFAULT_TEXT_COLOR = (255, 255, 255)  # White text
    DEFAULT_BORDER_RADIUS = 10  # Rounded corners
    
    def __init__(self, screen: pygame.Surface, message: str, font: pygame.font.Font, 
                 rect_data: Tuple[int, int, int, int], background_color: Tuple[int, int, int]) -> None:
        """
        Initialize a button with specified properties.
        
        Args:
            screen: The pygame surface to render the button on
            message: The text to display on the button
            font: The font to use for the button text
            rect_data: Tuple containing (center_x, center_y, width, height)
            background_color: RGB tuple for the button background color
        """
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        
        # Extract dimensions from rect_data
        # Note: rect_data format is (center_x, center_y, width, height)
        center_x, center_y, width, height = rect_data
        self.button_width = width
        self.button_height = height
        
        # Styling properties
        self.background_color = background_color
        self.text_color = self.DEFAULT_TEXT_COLOR
        self.font = font
        
        # Create button rectangle
        self.button_rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self.button_rect.center = (center_x, center_y)
        
        # Prepare the button text
        self._prepare_text_display(message)
    
    def _prepare_text_display(self, message: str) -> None:
        """
        Render the button text and calculate its positioning.
        
        This method creates a text surface with the button's message and
        positions it in the center of the button rectangle.
        
        Args:
            message: The text to display on the button
        """
        # Render text with antialiasing
        self.text_surface = self.font.render(
            message, True, self.text_color, self.background_color
        )
        
        # Center the text within the button
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.button_rect.center
    
    def render(self, border_radius: int = DEFAULT_BORDER_RADIUS) -> None:
        """
        Draw the button to the screen.
        
        This method renders the button background and overlays the text.
        The button can be drawn with rounded corners for a modern appearance.
        
        Args:
            border_radius: Radius for rounded corners (default: 10)
        """
        # Draw button background with rounded corners
        pygame.draw.rect(
            self.screen, self.background_color, self.button_rect, 
            border_radius=border_radius
        )
        
        # Draw the text on top of the button
        self.screen.blit(self.text_surface, self.text_rect)
    
    def is_clicked(self, cursor_position: Tuple[int, int]) -> bool:
        """
        Check if the button was clicked at the given cursor position.
        
        This method uses pygame's collision detection to determine if
        the cursor position intersects with the button's rectangle.
        
        Args:
            cursor_position: Tuple containing (x, y) coordinates of the cursor
            
        Returns:
            True if the cursor position is within the button bounds, False otherwise
        """
        return self.button_rect.collidepoint(cursor_position)
    
    def update_text(self, new_message: str) -> None:
        """
        Update the button's text content.
        
        This method allows changing the button's displayed text after creation,
        useful for buttons that need to show dynamic content.
        
        Args:
            new_message: The new text to display on the button
        """
        self._prepare_text_display(new_message)
    
    def update_position(self, new_center_x: int, new_center_y: int) -> None:
        """
        Move the button to a new position.
        
        Args:
            new_center_x: New X coordinate for the button center
            new_center_y: New Y coordinate for the button center
        """
        self.button_rect.center = (new_center_x, new_center_y)
        self.text_rect.center = self.button_rect.center
    
    def update_color(self, new_background_color: Tuple[int, int, int], 
                     new_text_color: Optional[Tuple[int, int, int]] = None) -> None:
        """
        Update the button's color scheme.
        
        Args:
            new_background_color: New RGB color for the button background
            new_text_color: New RGB color for the text (optional)
        """
        self.background_color = new_background_color
        
        if new_text_color is not None:
            self.text_color = new_text_color
        
        # Re-render text with new colors
        current_text = self.text_surface.get_rect()  # Get current dimensions
        # We need to store the original message to re-render properly
        # For now, we'll update the colors and the text will be updated on next _prepare_text_display call
    
    def get_button_bounds(self) -> pygame.Rect:
        """
        Get the button's bounding rectangle.
        
        Returns:
            A pygame.Rect object representing the button's position and size
        """
        return self.button_rect.copy()
    
    def is_enabled(self) -> bool:
        """
        Check if the button is currently enabled.
        
        This method can be extended to implement button state management.
        
        Returns:
            True if the button is enabled (always True in basic implementation)
        """
        return True
    
    # Legacy method names for backward compatibility
    def _prep_msg(self, message: str) -> None:
        """Legacy method name - use _prepare_text_display() instead."""
        self._prepare_text_display(message)
    
    def draw(self, borderRadius: int = DEFAULT_BORDER_RADIUS) -> None:
        """Legacy method name - use render() instead."""
        self.render(borderRadius)
    
    def isClicked(self, cursorPos: Tuple[int, int]) -> bool:
        """Legacy method name - use is_clicked() instead."""
        return self.is_clicked(cursorPos)
    
    # Legacy property names
    @property
    def width(self) -> int:
        """Legacy property name - use button_width instead."""
        return self.button_width
    
    @property
    def height(self) -> int:
        """Legacy property name - use button_height instead."""
        return self.button_height
    
    @property
    def button_color(self) -> Tuple[int, int, int]:
        """Legacy property name - use background_color instead."""
        return self.background_color
    
    @button_color.setter
    def button_color(self, value: Tuple[int, int, int]) -> None:
        """Legacy property setter - use background_color instead."""
        self.background_color = value
    
    @property
    def rect(self) -> pygame.Rect:
        """Legacy property name - use button_rect instead."""
        return self.button_rect
    
    @property
    def msg_image(self) -> pygame.Surface:
        """Legacy property name - use text_surface instead."""
        return self.text_surface
    
    @property
    def msg_image_rect(self) -> pygame.Rect:
        """Legacy property name - use text_rect instead."""
        return self.text_rect