import pygame

from UI.input_handling.car_input import InputHandler
from UI.screen import Screen
from button import Button


class GameScreen(Screen):

    def __init__(self, game):
        self.game = game
        self.input_handler = InputHandler()

        self.back_button = Button(50, 50, 200, 50, "Back to Menu")
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        """Handle events for game screen."""
        if self.back_button.handle_event(event):
            self.game.set_screen("menu")
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.input_handler.handle_input(event)

    def draw(self):
        """Draw game screen."""
        self.back_button.draw(self.game.screen)

        # Draw input text on the screen
        sim_input = self.input_handler.get_input()
        input_text = f"x: {sim_input.x:.2f}, y: {sim_input.y:.2f}"
        text_surface = self.font.render(input_text, True, (255, 255, 255))
        self.game.screen.blit(text_surface, (50, 150))  # Draw text on the screen