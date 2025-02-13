import pygame

from core.car import Car
from ui.game_drawer import GameDrawer
from ui.input_handling import InputHandler
from ui.screen import Screen
from ui.widgets.button import Button
from ui.widgets.checkbox import Checkbox
from ui.widgets.settings import CarSettingsWidget


class GameScreen(Screen):
    # Constants for input visualization
    BAR_WIDTH = 30
    BAR_HEIGHT = 100
    BAR_PADDING = 20
    BAR_BORDER = 2
    WHEEL_SIZE = 100
    MAX_ROTATION = 180  # Maximum rotation angle in degrees

    def __init__(self, game):
        self.game = game
        self.car = Car()
        self.input_handler = InputHandler()
        self.game_drawer = GameDrawer(self.game.screen, self.car,  self.input_handler)
        self.back_button = Button(50, 50, 200, 50, "Back to Menu")
        self.font = pygame.font.Font(None, 36)

        # Load and prepare steering wheel image
        try:
            self.wheel_image = pygame.image.load('assets/steering_wheel.png').convert_alpha()
            self.wheel_image = pygame.transform.scale(self.wheel_image,
                                                      (self.WHEEL_SIZE, self.WHEEL_SIZE))
            self.wheel_rect = self.wheel_image.get_rect()
        except pygame.error as e:
            print(f"Couldn't load steering wheel image: {e}")
            self.wheel_image = None
            self.wheel_rect = pygame.Rect(0, 0, self.WHEEL_SIZE, self.WHEEL_SIZE)

        # Calculate positions
        self.wheel_rect.centerx = Screen.WIDTH - self.WHEEL_SIZE - self.BAR_PADDING
        self.wheel_rect.centery = Screen.HEIGHT - self.WHEEL_SIZE - self.BAR_PADDING

        self.throttle_brake_rect = pygame.Rect(
            self.wheel_rect.right + self.BAR_PADDING,
            self.wheel_rect.centery - self.BAR_HEIGHT // 2,
            self.BAR_WIDTH,
            self.BAR_HEIGHT
        )
        self._settings_checkbox = Checkbox(Screen.WIDTH - 150, 10, 30, "Settings")
        self._mode_checkbox = Checkbox(Screen.WIDTH - 290, 10, 30, "Debug")
        self._settings = CarSettingsWidget(self.car.config, self.game.screen)

    def handle_event(self, event):
        """Handle events for game screen."""
        if self.back_button.handle_event(event):
            self.game.set_screen("menu")
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.input_handler.handle_input(event)
        self._settings_checkbox.handle_event(event)
        self._mode_checkbox.handle_event(event)

    def draw(self, dt):
        """Draw game screen."""
        controls_input = self.input_handler.get_input()
        self._settings.update()
        self.game_drawer.update(dt)

        self.game_drawer.draw()
        self._settings.draw()

        self._draw_throttle_brake_bar(controls_input.y)
        self._draw_steering_wheel(controls_input.x)
        self.back_button.draw(self.game.screen)

        self.game_drawer._is_debug_mode = self._settings.mode_toggle.value
        self.game_drawer._draw_acceleration = self._settings.acceleration_toggle.value
        self.game_drawer._draw_velocity = self._settings.velocity_toggle.value
        self.game_drawer._draw_friction_circle = self._settings.friction_circle_toggle.value
        self.game_drawer._draw_resistance = self._settings.resistance_toggle.value

    def _draw_throttle_brake_bar(self, y_input):
        """Draw the vertical throttle (green) and brake (red) bar."""
        # Draw border
        pygame.draw.rect(self.game.screen, (100, 100, 100), self.throttle_brake_rect, self.BAR_BORDER)

        # Calculate the fill height and position based on input
        center_y = self.throttle_brake_rect.centery
        fill_height = abs(y_input) * (self.BAR_HEIGHT / 2)

        if y_input > 0:  # Throttle (green)
            fill_rect = pygame.Rect(
                self.throttle_brake_rect.left,
                center_y - fill_height,
                self.BAR_WIDTH,
                fill_height
            )
            pygame.draw.rect(self.game.screen, (0, 255, 0), fill_rect)
        elif y_input < 0:  # Brake (red)
            fill_rect = pygame.Rect(
                self.throttle_brake_rect.left,
                center_y,
                self.BAR_WIDTH,
                fill_height
            )
            pygame.draw.rect(self.game.screen, (255, 0, 0), fill_rect)

        # Draw center line
        pygame.draw.line(self.game.screen, (200, 200, 200),
                         (self.throttle_brake_rect.left, center_y),
                         (self.throttle_brake_rect.right, center_y),
                         2)

    def _draw_steering_wheel(self, x_input):
        """Draw the rotating steering wheel."""
        if self.wheel_image is None:
            # Fallback if image loading failed
            pygame.draw.circle(self.game.screen, (150, 150, 150),
                               self.wheel_rect.center, self.WHEEL_SIZE // 2)
            return

        # Calculate rotation angle based on input
        angle = -x_input * self.MAX_ROTATION  # Negative because pygame rotation is clockwise

        # Rotate the wheel image
        rotated_wheel = pygame.transform.rotate(self.wheel_image, angle)

        # Get the rect of the rotated image and center it
        rotated_rect = rotated_wheel.get_rect(center=self.wheel_rect.center)

        # Draw the rotated wheel
        self.game.screen.blit(rotated_wheel, rotated_rect)