import pygame

pygame.init()

def drawText(screen, text, font, color, pos):
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = (pos[0], pos[1])
    screen.blit(textSurface, textRect)

def drawTextMultiLines(screen, text, font, color, pos, spacing):
    text_y = pos[1]
    for line in text.splitlines():
        drawText(screen, line, font, color, (pos[0], text_y))
        text_y += spacing


#Rounded Rect Helper Function:
def draw_rounded_rect(surface, color, rect, radius):
    x, y, w, h = map(int, rect)  # Ensure all values are integers
    radius = int(radius)  # Ensure radius is an integer

    # Draw corner circles
    pygame.gfxdraw.aacircle(surface, x + radius, y + radius, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + radius, y + radius, radius, color)
    pygame.gfxdraw.aacircle(surface, x + w - radius - 1, y + radius, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + w - radius - 1, y + radius, radius, color)
    pygame.gfxdraw.aacircle(surface, x + radius, y + h - radius - 1, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + radius, y + h - radius - 1, radius, color)
    pygame.gfxdraw.aacircle(surface, x + w - radius - 1, y + h - radius - 1, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + w - radius - 1, y + h - radius - 1, radius, color)

    # Draw rectangles to fill the middle and straight edges
    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))