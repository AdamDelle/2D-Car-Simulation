import numpy as np
import pygame

from UI.input_handling import ControlsInput
from UI.screen import Screen
from UI.ui_widgets.speedometer import Speedometer
from car import Car, CarInput
from helpers import get_image_and_rect, draw_vector, RED


class GameDrawer:

    CAR_X = Screen.CENTER_X
    CAR_Y = Screen.CENTER_Y
    WHEEL_X_OFFSET = 35
    WHEEL_Y_OFFSET = 30
    LEFT_WHEEL_X = CAR_X - WHEEL_X_OFFSET
    RIGHT_WHEEL_X = CAR_X + WHEEL_X_OFFSET
    FRONT_LEFT_WHEEL_Y = CAR_Y - WHEEL_Y_OFFSET
    FRONT_RIGHT_WHEEL_Y = CAR_Y - WHEEL_Y_OFFSET
    REAR_LEFT_WHEEL_Y = CAR_Y + WHEEL_Y_OFFSET
    REAR_RIGHT_WHEEL_Y = CAR_Y + WHEEL_Y_OFFSET

    MAP_START_X = Screen.CENTER_X
    MAP_START_Y = Screen.CENTER_Y
    MAP_START_ROTATION = 0

    def __init__(self, screen, car, input_handler):
        self._screen = screen
        self._car = car
        self._input_handler = input_handler
        self._car = Car()

        self._car_image, self._car_rect = get_image_and_rect(
            'assets/car_blue.png',
            scale=0.1, angle=-90,
            x=GameDrawer.CAR_X, y=GameDrawer.CAR_Y)
        self._front_left_wheel_image, self._front_left_wheel_rect = get_image_and_rect(
            'assets/wheel.png',
            scale=0.1, angle=-90,
            x=GameDrawer.LEFT_WHEEL_X, y=GameDrawer.FRONT_LEFT_WHEEL_Y)
        self._front_right_wheel_image, self._front_right_wheel_rect = get_image_and_rect(
            'assets/wheel.png',
            scale=0.1, angle=-90,
            x=GameDrawer.RIGHT_WHEEL_X, y=GameDrawer.FRONT_RIGHT_WHEEL_Y)
        self._rear_left_wheel_image, self._rear_left_wheel_rect = get_image_and_rect(
            'assets/wheel.png',
            scale=0.1, angle=-90,
            x=GameDrawer.LEFT_WHEEL_X, y=GameDrawer.REAR_LEFT_WHEEL_Y)
        self._rear_right_wheel_image, self._rear_right_wheel_rect = get_image_and_rect(
            'assets/wheel.png',
            scale=0.1, angle=-90,
            x=GameDrawer.RIGHT_WHEEL_X, y=GameDrawer.REAR_RIGHT_WHEEL_Y)

        self._map_image, self._map_rect = get_image_and_rect(
            'assets/rennstrecke.png',
            scale=1, angle=0,
            x=Screen.CENTER_X, y=Screen.CENTER_Y)

        self.speedometer = Speedometer(100, 980, 80, 200)  # x, y, radius, max_speed
        self._last_update_time = 0

    def update(self, controls_input: ControlsInput):
        current_time = pygame.time.get_ticks()
        dt = (current_time - self._last_update_time) / 1000
        self._last_update_time = current_time
        car_input = self._controls_input_to_car_input(controls_input)
        self._car.update(car_input, dt)
        self.speedometer.update(self._car.velocity[0]*3.6)


    def draw(self):

        self._draw_map()
        self._draw_car()
        self._draw_car_stats_as_text_on_screen()
        self.speedometer.draw(self._screen)


    def _draw_map(self):
        x, y, angle = self._calculate_map_transform()
        self._map_rect.center = (x, y)
        #rotated_map = pygame.transform.rotate(self._map_image, angle)
        self._screen.blit(self._map_image, self._map_rect)

    def _draw_car(self):
        car_rotation = np.rad2deg(self._car.angle)
        car_angle_rotated = -car_rotation - 90
        car_direction = np.array([np.cos(np.deg2rad(car_angle_rotated)), np.sin(np.deg2rad(car_angle_rotated))])
        car_direction_norm = car_direction / np.linalg.norm(car_direction)
        car_direction_perpendicular_norm = np.array([-car_direction_norm[1], car_direction_norm[0]])

        front_left_wheel_position = np.array([GameDrawer.CAR_X, GameDrawer.CAR_Y]) - car_direction_perpendicular_norm * GameDrawer.WHEEL_X_OFFSET + car_direction_norm * GameDrawer.WHEEL_Y_OFFSET
        front_right_wheel_position = np.array([GameDrawer.CAR_X, GameDrawer.CAR_Y]) + car_direction_perpendicular_norm * GameDrawer.WHEEL_X_OFFSET + car_direction_norm * GameDrawer.WHEEL_Y_OFFSET
        rear_left_wheel_position = np.array([GameDrawer.CAR_X, GameDrawer.CAR_Y]) - car_direction_perpendicular_norm * GameDrawer.WHEEL_X_OFFSET - car_direction_norm * GameDrawer.WHEEL_Y_OFFSET
        rear_right_wheel_position = np.array([GameDrawer.CAR_X, GameDrawer.CAR_Y]) + car_direction_perpendicular_norm * GameDrawer.WHEEL_X_OFFSET - car_direction_norm * GameDrawer.WHEEL_Y_OFFSET

        rotated_car = pygame.transform.rotate(self._car_image, car_rotation)
        rotated_car_rect = rotated_car.get_rect(center=self._car_rect.center)

        input_rotation = -self._input_handler.get_input().x * 35
        front_wheel_rotation = car_rotation + input_rotation
        rotated_front_wheel = pygame.transform.rotate(self._front_left_wheel_image, front_wheel_rotation)
        rotated_rear_wheel = pygame.transform.rotate(self._rear_left_wheel_image, car_rotation)
        front_left_rotated_wheel_rect = rotated_front_wheel.get_rect(center=(front_left_wheel_position[0], front_left_wheel_position[1]))
        front_right_rotated_wheel_rect = rotated_front_wheel.get_rect(center=(front_right_wheel_position[0], front_right_wheel_position[1]))
        rear_left_rotated_wheel_rect = rotated_rear_wheel.get_rect(center=(rear_left_wheel_position[0], rear_left_wheel_position[1]))
        rear_right_rotated_wheel_rect = rotated_rear_wheel.get_rect(center=(rear_right_wheel_position[0], rear_right_wheel_position[1]))

        self._screen.blit(rotated_front_wheel, front_left_rotated_wheel_rect)
        self._screen.blit(rotated_front_wheel, front_right_rotated_wheel_rect)
        self._screen.blit(rotated_rear_wheel, rear_left_rotated_wheel_rect)
        self._screen.blit(rotated_rear_wheel, rear_right_rotated_wheel_rect)
        self._screen.blit(rotated_car, rotated_car_rect)
        draw_vector(self._screen, car_direction_norm*100, (GameDrawer.CAR_X, GameDrawer.CAR_Y), color=RED, width=2)
        draw_vector(self._screen, car_direction_perpendicular_norm*100, (GameDrawer.CAR_X, GameDrawer.CAR_Y), color=RED, width=2)

    def _draw_car_stats_as_text_on_screen(self):
        velocity = self._car.velocity[0]
        acceleration = self._car.acceleration[0]
        text = f"Velocity: {round(velocity,2)}\tAcceleration: {round(acceleration, 2)}"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, RED)
        self._screen.blit(text_surface, (10, 10))


    def _calculate_map_transform(self):
        car_x = self._car.position_wc[0]
        car_y = self._car.position_wc[1]
        car_angle = np.rad2deg(self._car.angle)
        map_x = GameDrawer.MAP_START_X + car_x*10
        map_y = GameDrawer.MAP_START_Y + car_y*10
        map_angle = 0 # GameDrawer.MAP_START_ROTATION - car_angle
        return map_x, map_y, map_angle

    @staticmethod
    def _controls_input_to_car_input(controls_input: ControlsInput) -> CarInput:
        steering_angle = -controls_input.x * np.pi / 4
        throttle = controls_input.y * 100 if controls_input.y > 0 else 0
        brake = -controls_input.y * 100 if controls_input.y < 0 else 0
        return CarInput(steering_angle, throttle, brake)