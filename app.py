import pygame
import sys
from button import Button


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
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.current_screen = "menu"

        # Load and scale background image
        try:
            self.background = pygame.image.load('assets/background.png').convert_alpha()
            self.background = pygame.transform.scale(self.background, (1920, 1080))
        except pygame.error as e:
            print(f"Couldn't load background image: {e}")
            self.background = pygame.Surface((1920, 1080))
            self.background.fill((0, 0, 0))

        # Center buttons horizontally and vertically
        screen_center_x = 1920 // 2
        screen_center_y = 1080 // 2
        button_width = 200
        button_height = 50
        button_spacing = 80

        # Create centered menu buttons
        self.menu_buttons = [
            Button(screen_center_x - button_width // 2, screen_center_y - button_spacing, button_width, button_height,
                   "Start Game"),
            Button(screen_center_x - button_width // 2, screen_center_y, button_width, button_height, "Options"),
            Button(screen_center_x - button_width // 2, screen_center_y + button_spacing, button_width, button_height,
                   "Exit")
        ]

        self.back_button = Button(50, 50, 200, 50, "Back to Menu")

        # Options screen elements
        self.options = {
            "Vehicle Mass": {"min": 500, "max": 3000, "value": "1500", "unit": "kg"},
            "Maximum Acceleration": {"min": 2, "max": 10, "value": "5", "unit": "m/s²"},
            "Maximum Braking": {"min": 5, "max": 12, "value": "8", "unit": "m/s²"}
        }

        # Create input boxes for options
        self.input_boxes = {}
        y_position = 250
        for option in self.options.keys():
            self.input_boxes[option] = pygame.Rect(screen_center_x - 100, y_position, 200, 40)
            y_position += 150

        self.active_option = None
        self.font = pygame.font.Font(None, 36)

    def handle_input(self):
        """Handle keyboard input for game movement."""
        # TODO @Adam Logic und so
        return 0, 0, 0  # Dummy values for now

    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.current_screen == "menu":
                    self._handle_menu_events(event)
                elif self.current_screen == "options":
                    self._handle_options_events(event)
                elif self.current_screen == "game":
                    self._handle_game_events(event)

            self.screen.fill((0, 0, 0))

            if self.current_screen == "menu":
                self._draw_menu()
            elif self.current_screen == "options":
                self._draw_options()
            elif self.current_screen == "game":
                self._draw_game()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def _handle_menu_events(self, event):
        """Handle events for menu screen."""
        for i, button in enumerate(self.menu_buttons):
            if button.handle_event(event):
                if i == 0:
                    self.current_screen = "game"
                elif i == 1:
                    self.current_screen = "options"
                elif i == 2:
                    pygame.quit()
                    sys.exit()

    def _handle_options_events(self, event):
        """Handle events for options screen."""
        if self.back_button.handle_event(event):
            if self.active_option:
                # Validate current input before going back to menu
                self._validate_input(self.active_option)
            self.current_screen = "menu"

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If there's an active option and we click somewhere else, validate the input
            if self.active_option:
                clicked_current_box = self.input_boxes[self.active_option].collidepoint(event.pos)
                if not clicked_current_box:
                    self._validate_input(self.active_option)
                    self.active_option = None

            # Check if clicked on any input box
            for option, box in self.input_boxes.items():
                if box.collidepoint(event.pos):
                    self.active_option = option
                    break

        if event.type == pygame.KEYDOWN and self.active_option:
            current_value = self.options[self.active_option]["value"]

            if event.key == pygame.K_RETURN:
                # Validate the entire input when Enter is pressed
                self._validate_input(self.active_option)
                self.active_option = None

            elif event.key == pygame.K_BACKSPACE:
                # Handle backspace
                self.options[self.active_option]["value"] = current_value[:-1]

            elif event.unicode.isnumeric() or (event.unicode == '.' and '.' not in current_value):
                # Allow numbers and one decimal point
                new_value = current_value + event.unicode

                try:
                    # Try to convert to float for validation
                    num_value = float(new_value)
                    min_val = self.options[self.active_option]["min"]
                    max_val = self.options[self.active_option]["max"]

                    # Only update if within range or if still typing
                    if num_value <= max_val:
                        self.options[self.active_option]["value"] = new_value
                except ValueError:
                    pass

    def _validate_input(self, option):
        """Validate and correct the input value for an option."""
        try:
            value = float(self.options[option]["value"])
            min_val = self.options[option]["min"]
            max_val = self.options[option]["max"]

            # Clamp value between min and max
            value = max(min_val, min(value, max_val))

            # Update the value, converting back to string
            self.options[option]["value"] = str(int(value))
        except ValueError:
            # Reset to minimum value if input is invalid
            self.options[option]["value"] = str(self.options[option]["min"])

    def _handle_game_events(self, event):
        """Handle events for game screen."""
        if self.back_button.handle_event(event):
            self.current_screen = "menu"
        if event.type == pygame.KEYDOWN:
            # TODO @Adam Was du halt hier brauchst aus der Eventliste
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d,
                             pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                self.handle_input()

    def _draw_menu(self):
        """Draw menu screen."""
        # Draw background first
        self.screen.blit(self.background, (0, 0))
        # Then draw buttons on top
        for button in self.menu_buttons:
            button.draw(self.screen)

    def _draw_options(self):
        """Draw options screen."""
        self.screen.blit(self.background, (0, 0))
        self.back_button.draw(self.screen)

        # Draw title
        title = self.font.render("Game Options", True, (255, 255, 255))
        title_rect = title.get_rect(center=(1920//2, 150))
        self.screen.blit(title, title_rect)

        for option, box in self.input_boxes.items():
            # Draw option label
            label = self.font.render(f"{option} ({self.options[option]['min']}-{self.options[option]['max']} {self.options[option]['unit']})",
                                   True, (255, 255, 255))
            label_rect = label.get_rect(center=(box.centerx, box.y - 25))
            self.screen.blit(label, label_rect)

            # Draw input box
            color = (100, 100, 100) if self.active_option == option else (50, 50, 50)
            pygame.draw.rect(self.screen, color, box, border_radius=5)

            # Draw input value
            value_text = self.font.render(self.options[option]["value"], True, (255, 255, 255))
            value_rect = value_text.get_rect(center=box.center)
            self.screen.blit(value_text, value_rect)

    def _draw_game(self):
        """Draw game screen."""
        self.back_button.draw(self.screen)


if __name__ == "__main__":
    game = Game()
    game.run()