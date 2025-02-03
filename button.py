import pygame


class Button:
    """A class to create reusable UI buttons for pygame.

    Attributes:
        x (int): X-coordinate of button
        y (int): Y-coordinate of button
        width (int): Width of button
        height (int): Height of button
        text (str): Text to display on button
        base_color (tuple): RGB color for normal state
        hover_color (tuple): RGB color for hover state
    """

    def __init__(self, x, y, width, height, text, base_color=(200, 200, 200), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        """Draw the button on the given surface."""
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=12)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Handle mouse events for the button."""
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.base_color

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False