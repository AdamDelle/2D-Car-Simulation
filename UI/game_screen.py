import pygame

from UI.screen import Screen
from button import Button


class GameScreen(Screen):

    def __init__(self, game):
        self.game = game
        self.back_button = Button(50, 50, 200, 50, "Back to Menu")

    def handle_event(self, event):
        """Handle events for game screen."""
        if self.back_button.handle_event(event):
            self.game.set_screen("menu")
        if event.type == pygame.KEYDOWN:
            # TODO @Adam Was du halt hier brauchst aus der Eventliste
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d,
                             pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                self.handle_input()

    def draw(self):
        """Draw game screen."""
        self.back_button.draw(self.game.screen)

    def handle_input(self):
        """Handle keyboard input for game movement."""
        # TODO @Adam Logic und so
        return 0, 0, 0  # Dummy values for now