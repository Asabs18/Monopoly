import pygame

from src.config.colorAssets import *
from src.config.fontAssets import *

class TextBox:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.font = INBOXFONT
        self.text_color = BLACK
        self.bg_color = WHITE
        self.cursor_color = BLACK
        self.text = ""
        self.cursor_visible = True
        self.cursor_timer = 0

        self.isActive = False

    def handle_event(self, event):
        if self.isActive:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return self.text  # Submit text
            else:
                self.text += event.unicode

    def update(self):
        if self.isActive:
            self.cursor_timer += 1
            if self.cursor_timer >= 30:  # Blink every 30 frames
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

    def isClicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.isActive = True
        else:
            self.isActive = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect[0] + 5, self.rect[1] + 5))
        if self.cursor_visible and self.isActive:
            cursor_x = self.rect[0] + 5 + text_surface.get_width()
            pygame.draw.line(screen, self.cursor_color, (cursor_x, self.rect[1] + 5), (cursor_x, self.rect[1] + self.rect[3] - 5), 2)