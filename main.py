import sys

import pygame
import pygame_widgets

from ui.game_screen import GameScreen
from ui.menu_screen import MenuScreen
from ui.screen import Screen


class Game:
    """Main game class handling the game loop and screens.

    Attributes:
        screen (pygame.Surface): The main game window
        clock (pygame.time.Clock): Game clock for controlling FPS
        current_screen (str): Current active screen
        background (pygame.Surface): Background image for menu and options
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()

        self.menu_screen = MenuScreen(self)
        self.game_screen = GameScreen(self)
        self.current_screen: Screen = self.menu_screen

        # Load and scale background image
        try:
            self.background = pygame.image.load('assets/background.png').convert_alpha()
            self.background = pygame.transform.scale(self.background, (Screen.WIDTH, Screen.HEIGHT))
        except pygame.error as e:
            print(f"Couldn't load background image: {e}")
            self.background = pygame.Surface((Screen.WIDTH, Screen.HEIGHT))
            self.background.fill((0, 0, 0))

    def set_screen(self, screen_name):
        """Set the current active screen."""
        if screen_name == "menu":
            self.current_screen = self.menu_screen
        elif screen_name == "game":
            self.current_screen = self.game_screen

    def run(self):
        """Main game loop."""
        running = True
        while running:
            dt = self.clock.get_time() *0.001
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                self.current_screen.handle_event(event)
            pygame_widgets.update(events)

            self.screen.fill((0, 0, 0))
            self.current_screen.draw(dt)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()