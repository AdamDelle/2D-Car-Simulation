import pygame

from ui.screen import Screen
from ui.widgets.button import Button


class OptionsScreen(Screen):

    def __init__(self, game):
        self.game = game
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
            self.input_boxes[option] = pygame.Rect(Screen.CENTER_X - 100, y_position, 200, 40)
            y_position += 150

        self.active_option = None
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        """Handle events for options screen."""
        if self.back_button.handle_event(event):
            if self.active_option:
                # Validate current input before going back to menu
                self._validate_input(self.active_option)
            self.game.set_screen("menu")

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

    def draw(self):
        """Draw options screen."""
        self.game.screen.blit(self.game.background, (0, 0))
        self.back_button.draw(self.game.screen)

        # Draw title
        title = self.font.render("Game Options", True, (255, 255, 255))
        title_rect = title.get_rect(center=(Screen.CENTER_X, 150))
        self.game.screen.blit(title, title_rect)

        for option, box in self.input_boxes.items():
            # Draw option label
            label = self.font.render(f"{option} ({self.options[option]['min']}-{self.options[option]['max']} {self.options[option]['unit']})",
                                     True, (255, 255, 255))
            label_rect = label.get_rect(center=(box.centerx, box.y - 25))
            self.game.screen.blit(label, label_rect)

            # Draw input box
            color = (100, 100, 100) if self.active_option == option else (50, 50, 50)
            pygame.draw.rect(self.game.screen, color, box, border_radius=5)

            # Draw input value
            value_text = self.font.render(self.options[option]["value"], True, (255, 255, 255))
            value_rect = value_text.get_rect(center=box.center)
            self.game.screen.blit(value_text, value_rect)

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