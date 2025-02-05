from dataclasses import dataclass
import dataclasses
from pprint import pprint
from re import A
from typing import Mapping
import json
import numpy as np

g = 9.81 # m/s^2
DRAG : float = 5.0 # air resistance (drag)
RESISTANCE : float = 30.0 # rolling resistance
CA_R : float = -5.2 # cornering stiffness
CA_F : float = -5.0 # cornering stiffness
MAX_GRIP : float = 2.0 # maximum (normalised) friction force, = diameter of friction circle

@dataclass
class CarInput:
    steer_angle: float
    throttle: float
    brake: float

@dataclass
class CarConfig:
    name: str = "game"
    b: float = 1.0 # m
    c: float = 1.0 # m
    wheel_base: float = b + c # m
    h: float = 1.0 # m
    m: float = 1500.0 # kg
    inertia: float = 1500.0 # kg*m
    width: float = 1.5 # m
    length: float = 3.0 # m, must be > wheelbase
    wheel_length: float = 0.7 # m
    wheel_width: float = 0.3 # m

    def serialize(self, file_name):
        configs: list[CarConfig] = car_read_configs(file_name)
        data = []
        for config in configs:
            if self.name != config.name:
                data.append(dataclasses.asdict(config))
        data.append(dataclasses.asdict(self))
        with open(file_name, 'w') as file:
            json.dump(data, file)

    def load(self, file_name, config_name):
        configs: list[CarConfig] = car_read_configs(file_name)
        for config in configs:
            if config_name == config.name:
                self = config
            else:
                 raise Exception("Config not found.")

def car_read_configs(file_name) -> list[CarConfig]:
    result = []
    with open(file_name, '+r') as file:
        configs = json.load(file)
        for config in configs:
            result.append(CarConfig(**config))
    return result

@dataclass
class Car:
    def __init__(self):
        self.config: CarConfig = CarConfig()
        self.position_wc = np.array([0.0, 0.0])
        self.velocity_wc = np.array([0.0, 0.0])
        self.angle: float = 0
        self.orientation_vector = np.array([np.cos(self.angle), np.sin(self.angle)])
        self.angular_velocity: float = 0
        self.velocity = np.array([0.0, 0.0])
        self.acceleration_wc = np.array([0.0, 0.0])
        self.rot_angle: float = 0.0
        self.side_slip: float = 0.0
        self.slip_angle_front: float = 0.0
        self.slip_angle_rear: float = 0.0
        self.force = np.array([0.0, 0.0])
        self.rear_slip: int = 0
        self.front_slip: int = 0
        self.resistance = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.torque: float = 0.0
        self.angular_acceleration: float = 0.0
        self.sin: float = 0.0
        self.cos: float = 0.0
        self.yaw_speed: float = 0.0
        self.weight: float = 0.0
        self.front_traction = np.array([0.0, 0.0])
        self.lateral_force_front = np.array([0.0, 0.0])
        self.lateral_force_rear = np.array([0.0, 0.0])

        self.config.serialize("cars")
        exit()


    def update(self, input: CarInput, dt: float):

        sin = np.sin(self.angle)
        cos = np.cos(self.angle)

        self.velocity[0] = cos * self.velocity_wc[1] + sin * self.velocity_wc[0]
        self.velocity[1] = -sin * self.velocity_wc[1] + cos * self.velocity_wc[0]

        # lateral force on wheels
        yaw_speed = self.config.wheel_base * 0.5 * self.angular_velocity

        if self.velocity[0] == 0:
            rot_angle = 0
        else:
            rot_angle = np.arctan(yaw_speed / self.velocity[0])

        if self.velocity[0] == 0:
            side_slip = 0
        else:
            side_slip = np.arctan(self.velocity[1] / self.velocity[0])

        # calculate slip angles for front and rear wheels (alpha)
        slip_angle_front = side_slip + rot_angle - input.steer_angle
        slip_angle_rear = side_slip - rot_angle

        # weight per axle
        # TODO: check if better to depend on b and c
        weight = self.config.m * g * 0.5

        # calculate lateral force on front wheels (Ca * slip_angle) capped to friction * load
        self.lateral_force_front[0] = 0
        self.lateral_force_front[1] = CA_F * slip_angle_front
        self.lateral_force_front[1] = np.clip(self.lateral_force_front[1], -MAX_GRIP, MAX_GRIP)
        print("MAX", MAX_GRIP)
        print("lateral_force_front[1]", self.lateral_force_front[1])
        self.lateral_force_front[1] *= weight
        if self.front_slip == 1:
            self.lateral_force_front[1] *= 0.5


        # calculate lateral force on rear wheels (Ca * slip_angle) capped to friction * load
        self.lateral_force_rear[0] = 0
        self.lateral_force_rear[1] = CA_R * slip_angle_rear
        self.lateral_force_rear[1] = np.clip(self.lateral_force_rear[1], -MAX_GRIP, MAX_GRIP)
        self.lateral_force_rear[1] *= weight
        if self.rear_slip == 1:
            self.lateral_force_rear[1] *= 0.5

        # longitudinal force on rear wheels - very simple traction model
        self.front_traction[0] = 100*(input.throttle - input.brake*np.sign(self.velocity[0]))
        self.front_traction[1] = 0
        if (self.rear_slip==1):
            self.front_traction[0] *= 0.5

        # forces and torque on body
        self.resistance[0] = -(RESISTANCE*self.velocity[0] + DRAG*self.velocity[0]*np.absolute(self.velocity[0]))
        self.resistance[1] = -(RESISTANCE*self.velocity[1] + DRAG*self.velocity[1]*np.absolute(self.velocity[1]))
        # print("resistance:", resistance)

        # sum forces
        # TODO: check if better np one liner
        self.force[0] = self.front_traction[0] + np.sin(input.steer_angle) * self.lateral_force_front[0] + self.lateral_force_rear[0] + self.resistance[0]
        self.force[1] = self.front_traction[1] + np.cos(input.steer_angle) * self.lateral_force_front[1] + self.lateral_force_rear[1] + self.resistance[1]
        # print("force:", force)

        # torque on body from lateral forces
        torque = self.config.b * self.lateral_force_front[1] - self.config.c * self.lateral_force_rear[1]

        # acceleration
        self.acceleration[0] = self.force[0] / self.config.m
        self.acceleration[1] = self.force[1] / self.config.m
        angular_acceleration = torque / self.config.inertia

        # update velocity
        self.acceleration_wc[0] = cos * self.acceleration[1] + sin * self.acceleration[0]
        self.acceleration_wc[1] = -sin * self.acceleration[1] + cos * self.acceleration[0]
        # print("accel:", acceleration)

        # velocity is integrated acceleration
        self.velocity_wc += self.acceleration_wc * dt

        # position is integrated velocity
        self.position_wc += self.velocity_wc * dt

        # angular velocity and heading
        self.angular_velocity += angular_acceleration * dt
        self.angle += self.angular_velocity * dt
        self.orientation_vector = np.array([np.cos(self.angle), np.sin(self.angle)])
        print(self.angle/(2*np.pi)*360 % 360)