import sys

import pygame

from ui.screen import Screen
from ui.widgets.button import Button

class MenuScreen(Screen):

    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50
    BUTTON_SPACING = 40

    def __init__(self, game):
        self.game = game

        # Load and scale background image
        try:
            self.background = pygame.image.load('assets/background.png').convert_alpha()
            self.background = pygame.transform.scale(self.background, (Screen.WIDTH, Screen.HEIGHT))
        except pygame.error as e:
            print(f"Couldn't load background image: {e}")
            self.background = pygame.Surface((Screen.WIDTH, Screen.HEIGHT))
            self.background.fill((0, 0, 0))

        self.menu_buttons = [
            Button(Screen.CENTER_X - MenuScreen.BUTTON_WIDTH // 2, Screen.CENTER_Y - MenuScreen.BUTTON_SPACING, MenuScreen.BUTTON_WIDTH, MenuScreen.BUTTON_HEIGHT,
                   "Start Game"),
            Button(Screen.CENTER_X - MenuScreen.BUTTON_WIDTH // 2, Screen.CENTER_Y + MenuScreen.BUTTON_SPACING, MenuScreen.BUTTON_WIDTH, MenuScreen.BUTTON_HEIGHT,
                   "Exit")
        ]

    def handle_event(self, event):
        for i, button in enumerate(self.menu_buttons):
            if button.handle_event(event):
                if i == 0:
                    self.game.set_screen("game")
                elif i == 1:
                    pygame.quit()
                    sys.exit()

    def draw(self, dt):
        """Draw menu screen."""
        # Draw background first
        self.game.screen.blit(self.background, (0, 0))
        # Then draw buttons on top
        for button in self.menu_buttons:
            button.draw(self.game.screen)