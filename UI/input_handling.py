import pygame


class ControlsInput:
    def __init__(self):
        self.x = 0  # -1 for left, 1 for right
        self.y = 0  # -1 for up, 1 for down

class InputHandler:
    TIME_UNTIL_MAX_INPUT = 500  # ms
    TIME_TO_FADE_BACK = 250  # ms

    def __init__(self):
        self._input = ControlsInput()
        self._start_time_x = None
        self._start_time_y = None
        self._release_time_x = None
        self._release_time_y = None
        self._last_value_x = 0
        self._last_value_y = 0

        self._w_down = False
        self._s_down = False
        self._a_down = False
        self._d_down = False

    def get_input(self):
        self.update_input()
        return self._input

    def handle_input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self._handle_w_pressed()
            elif event.key == pygame.K_s:
                self._handle_s_pressed()
            elif event.key == pygame.K_a:
                self._handle_a_pressed()
            elif event.key == pygame.K_d:
                self._handle_d_pressed()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self._handle_w_released()
            elif event.key == pygame.K_s:
                self._handle_s_released()
            elif event.key == pygame.K_a:
                self._handle_a_released()
            elif event.key == pygame.K_d:
                self._handle_d_released()

    def update_input(self):
        current_time = pygame.time.get_ticks()

        # Handle Y-axis (acceleration/braking)
        if self._w_down:
            time_diff = current_time - self._start_time_y
            self._input.y = min(time_diff / self.TIME_UNTIL_MAX_INPUT, 1)
            self._last_value_y = self._input.y
        elif self._s_down:
            time_diff = current_time - self._start_time_y
            self._input.y = -min(time_diff / self.TIME_UNTIL_MAX_INPUT, 1)
            self._last_value_y = self._input.y
        elif self._release_time_y is not None:
            time_since_release = current_time - self._release_time_y
            if time_since_release < self.TIME_TO_FADE_BACK:
                fade_factor = 1 - (time_since_release / self.TIME_TO_FADE_BACK)
                self._input.y = self._last_value_y * fade_factor
            else:
                self._input.y = 0
                self._release_time_y = None
        else:
            self._input.y = 0

        # Handle X-axis (steering)
        if self._a_down:
            time_diff = current_time - self._start_time_x
            self._input.x = -min(time_diff / self.TIME_UNTIL_MAX_INPUT, 1)
            self._last_value_x = self._input.x
        elif self._d_down:
            time_diff = current_time - self._start_time_x
            self._input.x = min(time_diff / self.TIME_UNTIL_MAX_INPUT, 1)
            self._last_value_x = self._input.x
        elif self._release_time_x is not None:
            time_since_release = current_time - self._release_time_x
            if time_since_release < self.TIME_TO_FADE_BACK:
                fade_factor = 1 - (time_since_release / self.TIME_TO_FADE_BACK)
                self._input.x = self._last_value_x * fade_factor
            else:
                self._input.x = 0
                self._release_time_x = None
        else:
            self._input.x = 0

    def _handle_w_pressed(self):
        self._w_down = True
        self._s_down = False
        self._start_time_y = pygame.time.get_ticks()
        self._release_time_y = None

    def _handle_w_released(self):
        self._w_down = False
        self._release_time_y = pygame.time.get_ticks()

    def _handle_s_pressed(self):
        self._s_down = True
        self._w_down = False
        self._start_time_y = pygame.time.get_ticks()
        self._release_time_y = None

    def _handle_s_released(self):
        self._s_down = False
        self._release_time_y = pygame.time.get_ticks()

    def _handle_a_pressed(self):
        self._a_down = True
        self._d_down = False
        self._start_time_x = pygame.time.get_ticks()
        self._release_time_x = None

    def _handle_a_released(self):
        self._a_down = False
        self._release_time_x = pygame.time.get_ticks()

    def _handle_d_pressed(self):
        self._d_down = True
        self._a_down = False
        self._start_time_x = pygame.time.get_ticks()
        self._release_time_x = None

    def _handle_d_released(self):
        self._d_down = False
        self._release_time_x = pygame.time.get_ticks()