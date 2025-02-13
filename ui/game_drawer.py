from typing import Tuple
import numpy as np
import pygame

from core.car import Car, CarInput
from ui.helpers import scale_and_rotate, draw_vector, RED
from ui.input_handling import ControlsInput
from ui.screen import Screen
from ui.widgets.speedometer import Speedometer

class GameDrawer:
    CAR_X = Screen.CENTER_X
    CAR_Y = Screen.CENTER_Y
    CAR_POSITION = (CAR_X, CAR_Y)
    WHEEL_X_OFFSET = 350 # in original png
    WHEEL_Y_OFFSET = 300 # in original png

    MAP_START_X = Screen.CENTER_X
    MAP_START_Y = Screen.CENTER_Y
    MAP_START_ROTATION = 0

    PX_M_RATIO_SCREEN = 30   #pixel/meter
    PX_M_RATIO_CAR_IMAGE = 1277 / 3 # pixel/meter
    PX_M_RATIO_MAP_IMAGE = 240 / 6 # pixel/meter

    def __init__(self, screen, car, input_handler):
        self._screen = screen
        self._input_handler = input_handler
        self._car: Car = car


        map_image = pygame.image.load('assets/new_racetrack.png')
        racing_line = pygame.image.load('assets/racing_line.png')
        map_image_scaling_factor = 1/GameDrawer.PX_M_RATIO_MAP_IMAGE * GameDrawer.PX_M_RATIO_SCREEN

        self._map_image = scale_and_rotate(map_image, scale=map_image_scaling_factor, angle=GameDrawer.MAP_START_ROTATION)
        self._racing_line_image = scale_and_rotate(racing_line, scale=map_image_scaling_factor, angle=GameDrawer.MAP_START_ROTATION)

        car_image = pygame.image.load('assets/car_blue.png')
        self._car_image_scaling_factor = 1/GameDrawer.PX_M_RATIO_CAR_IMAGE * GameDrawer.PX_M_RATIO_SCREEN
        self._car_image = scale_and_rotate(car_image, scale=self._car_image_scaling_factor, angle=+90)

        self._wheel_x_offset = GameDrawer.WHEEL_X_OFFSET * self._car_image_scaling_factor
        self._wheel_y_offset = GameDrawer.WHEEL_Y_OFFSET * self._car_image_scaling_factor

        self._front_left_wheel_image= scale_and_rotate(pygame.image.load('assets/wheel.png'), scale=self._car_image_scaling_factor, angle=+90)
        self._front_right_wheel_image= scale_and_rotate(pygame.image.load('assets/wheel.png'), scale=self._car_image_scaling_factor, angle=+90)
        self._rear_left_wheel_image= scale_and_rotate(pygame.image.load('assets/wheel.png'), scale=self._car_image_scaling_factor, angle=+90)
        self._rear_right_wheel_image= scale_and_rotate(pygame.image.load('assets/wheel.png'), scale=self._car_image_scaling_factor, angle=+90)

        self.speedometer = Speedometer(100, 980, 80, 200)
        self._last_update_time = 0

        # debug mode
        self._is_debug_mode = False
        self._draw_acceleration = False
        self._draw_velocity = False
        self._draw_friction_circle = False
        self._draw_resistance = False

    def update(self, dt):
        controls_input = self._input_handler.get_input()
        car_input = self._controls_input_to_car_input(controls_input)
        self._car.update(car_input, dt)
        self.speedometer.update(self._car.velocity[0]*3.6)

    def draw(self):
        self._draw_map()

        if self._is_debug_mode:
            self._draw_debug_car()
        else:
            self._draw_car()
        self._draw_vectors()
        self._draw_car_stats_as_text_on_screen()
        self.speedometer.draw(self._screen)

    def _draw_map(self):
        x, y, _ = self._calculate_map_transform()
        self._screen.blit(self._map_image, self._map_image.get_rect(center=(x, y)))
        self._screen.blit(self._racing_line_image, self._map_image.get_rect(center=(x, y)))

    def _get_wheel_position(self, car_direction_norm, car_direction_perpendicular_norm, x_sign, y_sign):
        return np.array([GameDrawer.CAR_X, GameDrawer.CAR_Y]) + car_direction_perpendicular_norm * x_sign * self._wheel_x_offset + car_direction_norm * y_sign * self._wheel_y_offset

    def _draw_car(self):
        car_rotation = np.rad2deg(self._car.angle)
        car_angle_rotated = -car_rotation - 90
        car_direction = np.array([np.cos(np.deg2rad(car_angle_rotated)), np.sin(np.deg2rad(car_angle_rotated))])
        car_direction_norm = car_direction / np.linalg.norm(car_direction)
        car_direction_perpendicular_norm = np.array([-car_direction_norm[1], car_direction_norm[0]])

        front_left_wheel_position = self._get_wheel_position(car_direction_norm, car_direction_perpendicular_norm, -1, 1)
        front_right_wheel_position = self._get_wheel_position(car_direction_norm, car_direction_perpendicular_norm, 1, 1)
        rear_left_wheel_position = self._get_wheel_position(car_direction_norm, car_direction_perpendicular_norm, -1, -1)
        rear_right_wheel_position = self._get_wheel_position(car_direction_norm, car_direction_perpendicular_norm, 1, -1)

        rotated_car = pygame.transform.rotate(self._car_image, car_rotation)
        rotated_car_rect = rotated_car.get_rect(center=(GameDrawer.CAR_X, GameDrawer.CAR_Y))

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

    def _draw_rect(self, position, width, length, angle, color):
        surf = pygame.Surface((width, length))
        surf.set_colorkey((0, 255, 0))
        surf.fill(color)
        surf = pygame.transform.rotate(surf, angle)
        rect = surf.get_rect(center = position)
        self._screen.blit(surf, rect)

    def _draw_debug_car(self):
        scale = GameDrawer.PX_M_RATIO_SCREEN

        # car
        car_rotation = np.rad2deg(self._car.angle)
        orientation_vector = np.flip(self._car.orientation_vector)

        front_part_center = np.array([self.CAR_X, self.CAR_Y]) + self._car.config.b*0.5 * orientation_vector * scale
        rear_part_center = np.array([self.CAR_X, self.CAR_Y]) - self._car.config.c*0.5 * orientation_vector * scale
        self._draw_rect(front_part_center, 1*scale, scale*self._car.config.b, car_rotation, (200, 200, 200))
        self._draw_rect(rear_part_center, 1*scale, scale*self._car.config.c, car_rotation, (200, 200, 200))

        front_wheel_position = np.array([self.CAR_X, self.CAR_Y]) + self._car.config.b*scale * orientation_vector
        front_wheel_rotation = car_rotation + (-self._input_handler.get_input().x * 35)
        self._draw_rect(front_wheel_position, 0.2*scale, 0.4*scale, front_wheel_rotation, (0, 0, 0))

        rear_wheel_position = np.array([self.CAR_X, self.CAR_Y]) - self._car.config.c*scale * orientation_vector
        self._draw_rect(rear_wheel_position, 0.2*scale, 0.4*scale, car_rotation, (0, 0, 0))

    def _draw_vectors(self):
        orientation_vector = np.flip(self._car.orientation_vector)
        scale = GameDrawer.PX_M_RATIO_SCREEN
        if self._draw_acceleration:
            draw_vector(self._screen, self._car.acceleration_wc*scale, self.CAR_POSITION, RED, 3)
        if self._draw_velocity:
            draw_vector(self._screen, self._car.velocity_wc*scale, self.CAR_POSITION, (0, 255, 0), 3)
        if self._draw_resistance:
            dir = self._car.velocity_wc / np.linalg.norm(self._car.velocity_wc)
            draw_vector(self._screen, -dir*np.linalg.norm(self._car.resistance)/self._car.config.m*scale, self.CAR_POSITION, (255, 165, 0), 3)

        front_longitudinal_vec = orientation_vector*self._car.front_traction[0]/self._car.config.m*scale
        front_lateral_vec = np.array([-orientation_vector[1], orientation_vector[0]]) * self._car.lateral_force_front[1]/self._car.config.m*scale
        front_sum = front_longitudinal_vec + front_lateral_vec
        print(front_sum)
        # draw_vector(self._screen, orientation_vector*self._car.front_traction[0]/self._car.config.m*scale, front_wheel_position, (0, 255, 0), 3)
        # draw_vector(self._screen, np.array([-orientation_vector[1], orientation_vector[0]]) * self._car.lateral_force_front[1]/self._car.config.m*scale, front_wheel_position, (0, 255, 0), 3)
        # draw_vector(self._screen, front_sum, front_wheel_position, (255, 0, 0), 3)
        if self._draw_friction_circle:
            front_wheel_position = np.array([self.CAR_X, self.CAR_Y]) + self._car.config.b*scale * orientation_vector
            pygame.draw.circle(self._screen, (255, 0, 255), (front_wheel_position[0], front_wheel_position[1]), scale*self._car.config.max_grip, 3)

            R = np.array([[np.cos(self._car.angle), np.sin(self._car.angle)],
                        [-np.sin(self._car.angle), np.cos(self._car.angle)]])

            lateral = self._car.lateral_force_front/(self._car.config.m*9.81*0.5)
            lateral = np.flip(lateral)
            lateral = R.dot(lateral)
            lateral *= scale

            longitudinal = self._car.front_traction/(self._car.config.m*9.81*0.5)
            longitudinal = np.flip(longitudinal)
            longitudinal = R.dot(longitudinal)
            longitudinal *= scale

            draw_vector(self._screen, lateral, front_wheel_position, (255, 0, 255, 100), 3)
            draw_vector(self._screen, longitudinal, front_wheel_position, (255, 0, 255, 100), 3)
            friction_point_np = (longitudinal+lateral+ front_wheel_position)
            friction_point = (friction_point_np[0], friction_point_np[1])
            pygame.draw.circle(self._screen, (255, 0, 255), friction_point, 4)


    def _draw_car_stats_as_text_on_screen(self):
        velocity = np.linalg.norm(self._car.velocity)
        acceleration = np.linalg.norm(self._car.acceleration)

        current_y = 120
        text = f"Velocity: {round(velocity,2)}"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (0, 0, 0))
        self._screen.blit(text_surface, (30, current_y))

        current_y += 30
        text = f"Acceleration: {round(acceleration, 2)}"
        text_surface = font.render(text, True, (0, 0, 0))
        self._screen.blit(text_surface, (30, current_y))

        current_y += 30
        text = f"Angular velocity: {round(self._car.angular_velocity, 2)}"
        text_surface = font.render(text, True, (0, 0, 0))
        self._screen.blit(text_surface, (30, current_y))

        current_y += 30
        text = f"Angular acceleration: {round(self._car.angular_acceleration, 2)}"
        text_surface = font.render(text, True, (0, 0, 0))
        self._screen.blit(text_surface, (30, current_y))

    def _calculate_map_transform(self):
        car_x = self._car.position_wc[0]
        car_y = self._car.position_wc[1]
        map_x = GameDrawer.MAP_START_X - car_x * GameDrawer.PX_M_RATIO_SCREEN
        map_y = GameDrawer.MAP_START_Y - car_y * GameDrawer.PX_M_RATIO_SCREEN
        return map_x, map_y, 0

    @staticmethod
    def _controls_input_to_car_input(controls_input: ControlsInput) -> CarInput:
        steering_angle = -controls_input.x * np.pi / 4
        throttle = controls_input.y * 100 if controls_input.y > 0 else 0
        brake = -controls_input.y * 100 if controls_input.y < 0 else 0
        return CarInput(steering_angle, throttle, brake)