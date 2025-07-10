"""
Monopoly Game Dice System Module

This module implements the dice rolling mechanics for the Monopoly board game.
It provides individual die objects and a dice set that handles rolling animations,
double detection, and visual display of dice results.

Author: Aidan Sabatini
"""

# Standard library imports
from enum import Enum
from random import randint
from time import sleep
from typing import List, Tuple

# Third-party imports
import pygame

# Local application imports
from src.config.displayAssets import (
    DICE_X1, DICE_Y1, DICE_X2, DICE_Y2,
    ROLL_RANGEL, ROLL_RANGEH
)
from src.config.imgAssets import DIEIMGS

# Initialize Pygame
pygame.init()


class DieSide(Enum):
    """
    Enumeration representing the six sides of a standard die.
    
    This enum provides a type-safe way to represent die faces and ensures
    only valid die values (1-6) can be used throughout the system.
    """
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6


class Die:
    """
    Represents a single six-sided die with visual representation.
    
    This class manages the state and display of an individual die, including
    its current face value, position on screen, and corresponding image.
    Each die can be rolled independently and displays the appropriate
    visual representation of its current value.
    
    Attributes:
        screen (pygame.Surface): The game display surface
        x_position (int): Horizontal position for rendering the die
        y_position (int): Vertical position for rendering the die
        current_side (DieSide): The currently showing face of the die
        die_images (List[pygame.Surface]): Images for each die face
        current_image (pygame.Surface): The image for the current side
    """
    
    # Die constants
    MIN_VALUE = 1
    MAX_VALUE = 6
    
    def __init__(self, screen: pygame.Surface, x_position: int, y_position: int) -> None:
        """
        Initialize a die with its position and starting state.
        
        Args:
            screen: The pygame surface to render the die on
            x_position: Horizontal pixel position for the die
            y_position: Vertical pixel position for the die
        """
        self.screen = screen
        self.x_position = x_position
        self.y_position = y_position
        
        # Initialize die state
        self.current_side = self._generate_random_side()
        self.die_images = DIEIMGS
        self.current_image = self._get_image_for_side()
    
    def _generate_random_side(self) -> DieSide:
        """
        Generate a random die side value.
        
        Returns:
            A randomly selected DieSide enum value
        """
        random_value = randint(self.MIN_VALUE, self.MAX_VALUE)
        return DieSide(random_value)
    
    def get_value(self) -> int:
        """
        Get the numeric value of the current die side.
        
        Returns:
            Integer value from 1-6 representing the current die face
        """
        return self.current_side.value
    
    def _get_image_for_side(self) -> pygame.Surface:
        """
        Get the appropriate image for the current die side.
        
        Returns:
            The pygame Surface containing the die face image
        """
        # Die images are 0-indexed, so subtract 1 from the die value
        image_index = self.current_side.value - 1
        return self.die_images[image_index]
    
    def render(self) -> None:
        """
        Render the die to the screen at its designated position.
        
        This method blits the current die image to the screen at the
        die's stored x and y coordinates.
        """
        self.screen.blit(self.current_image, (self.x_position, self.y_position))
    
    def roll(self) -> None:
        """
        Roll the die to a new random value.
        
        This method updates both the die's side value and its corresponding
        visual representation to reflect the new roll result.
        """
        self.current_side = self._generate_random_side()
        self.current_image = self._get_image_for_side()
    
    # Legacy method names for backward compatibility
    def getRandomSide(self) -> DieSide:
        """Legacy method name - use _generate_random_side() instead."""
        return self._generate_random_side()
    
    def getValue(self) -> int:
        """Legacy method name - use get_value() instead."""
        return self.get_value()
    
    def display(self) -> None:
        """Legacy method name - use render() instead."""
        self.render()
    
    def getImage(self) -> pygame.Surface:
        """Legacy method name - use _get_image_for_side() instead."""
        return self._get_image_for_side()
    
    def update(self) -> None:
        """Legacy method name - use roll() instead."""
        self.roll()


class DiceSet:
    """
    Manages a pair of dice for Monopoly gameplay.
    
    This class coordinates two individual dice, handling their display,
    rolling animations, and game-specific functionality like double detection.
    The dice set can be shown or hidden as needed during gameplay and provides
    smooth rolling animations for visual appeal.
    
    Attributes:
        screen (pygame.Surface): The game display surface
        dice (List[Die]): The two dice in this set
        is_visible (bool): Whether the dice should be displayed
    """
    
    # Animation constants
    ANIMATION_DELAY = 0.01  # Seconds between animation frames
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize a dice set with two dice.
        
        Args:
            screen: The pygame surface to render the dice on
        """
        self.screen = screen
        self.dice = [
            Die(screen, DICE_X1, DICE_Y1),
            Die(screen, DICE_X2, DICE_Y2)
        ]
        self.is_visible = False
    
    def render(self) -> None:
        """
        Render both dice to the screen if they should be visible.
        
        This method only displays the dice when the dice set is marked
        as visible, allowing for controlled showing/hiding of dice.
        """
        if self.is_visible:
            for die in self.dice:
                die.render()
    
    def roll_with_animation(self) -> int:
        """
        Roll both dice with a visual animation effect.
        
        This method creates a rolling animation by rapidly updating the dice
        faces multiple times before settling on the final values. The animation
        only occurs when the dice are visible.
        
        Returns:
            The sum of both dice values after rolling
        """
        if self.is_visible:
            self._perform_rolling_animation()
        
        return self.get_total_value()
    
    def _perform_rolling_animation(self) -> None:
        """
        Execute the visual rolling animation for both dice.
        
        This method rapidly cycles through random die faces to create
        the illusion of dice rolling, with timing controlled by the
        ANIMATION_DELAY constant.
        """
        animation_cycles = randint(ROLL_RANGEL, ROLL_RANGEH)
        
        for _ in range(animation_cycles):
            # Update both dice to new random values
            for die in self.dice:
                die.roll()
            
            # Render the updated dice
            self.render()
            pygame.display.flip()
            sleep(self.ANIMATION_DELAY)
    
    def get_total_value(self) -> int:
        """
        Calculate the sum of both dice values.
        
        Returns:
            Integer sum of the two dice (range: 2-12)
        """
        return sum(die.get_value() for die in self.dice)
    
    def get_individual_values(self) -> Tuple[int, int]:
        """
        Get the individual values of both dice.
        
        Returns:
            Tuple containing (first_die_value, second_die_value)
        """
        return (self.dice[0].get_value(), self.dice[1].get_value())
    
    def is_double_roll(self) -> bool:
        """
        Check if both dice show the same value.
        
        Returns:
            True if both dice have the same face value, False otherwise
        """
        return self.dice[0].current_side == self.dice[1].current_side
    
    def _update_both_dice(self) -> None:
        """Update both dice to new random values without animation."""
        for die in self.dice:
            die.roll()
    
    def show_dice(self) -> None:
        """Make the dice visible on screen."""
        self.is_visible = True
    
    def hide_dice(self) -> None:
        """Hide the dice from view."""
        self.is_visible = False
    
    def toggle_visibility(self) -> None:
        """Switch the dice between visible and hidden states."""
        self.is_visible = not self.is_visible
    
    # Legacy method names for backward compatibility
    def display(self) -> None:
        """Legacy method name - use render() instead."""
        self.render()
    
    def roll(self) -> int:
        """Legacy method name - use roll_with_animation() instead."""
        return self.roll_with_animation()
    
    def getValue(self) -> int:
        """Legacy method name - use get_total_value() instead."""
        return self.get_total_value()
    
    def isDouble(self) -> bool:
        """Legacy method name - use is_double_roll() instead."""
        return self.is_double_roll()
    
    def update(self) -> None:
        """Legacy method name - use _update_both_dice() instead."""
        self._update_both_dice()
    
    def on(self) -> None:
        """Legacy method name - use show_dice() instead."""
        self.show_dice()
    
    def off(self) -> None:
        """Legacy method name - use hide_dice() instead."""
        self.hide_dice()
    
    def toggle(self) -> None:
        """Legacy method name - use toggle_visibility() instead."""
        self.toggle_visibility()
    
    @property
    def isDisplayed(self) -> bool:
        """Legacy property name - use is_visible instead."""
        return self.is_visible
    
    @isDisplayed.setter
    def isDisplayed(self, value: bool) -> None:
        """Legacy property setter - use is_visible instead."""
        self.is_visible = value


# Legacy names for backward compatibility
Side = DieSide
Dice = Die