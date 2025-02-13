from dataclasses import dataclass

import numpy as np

g = 9.81 # m/s^2
ZERO : float = 0.01

@dataclass
class CarInput:
    steer_angle: float
    throttle: float
    brake: float

class CarConfig:
    name: str = "game"
    b: float = 1.0 # m
    c: float = 1.0 # m
    height: float = 1.0 # m
    wheel_base: float = b + c # m
    m: float = 1500.0 # kg
    inertia: float = 1500.0 # kg*m
    drag : float = 5.0 # air resistance (drag)
    resistance : float = 30.0 # rolling resistance
    cornering_rear : float = -5.2 # cornering stiffness
    cornering_front : float = -5.0 # cornering stiffness
    max_grip : float = 2.0 # maximum (normalised) friction force, = radius of friction circle

    def set_b(self, b):
        self.b = b
        self.wheel_base = self.b + self.c

    def set_c(self, c):
        self.c = c
        self.wheel_base = self.b + self.c

    def set_m(self, m):
        self.m = m
        self.inertia = m

    def set_cornering_rear(self, cornering_rear):
        self.cornering_rear = cornering_rear

    def set_cornering_front(self, cornering_rear):
        self.cornering_front = cornering_rear

    def set_max_grip(self, max_grip):
        self.max_grip = max_grip

def f32_array(arr):
    return np.array(arr, dtype='float32')

@dataclass
class Car:
    def __init__(self):
        self.config: CarConfig = CarConfig()
        self.position_wc = f32_array([0.0, 0.0])
        self.velocity_wc = f32_array([0.0, 0.0])
        self.angle: float = 0
        self.orientation_vector = f32_array([np.cos(self.angle), np.sin(self.angle)])
        self.angular_velocity: float = 0
        self.velocity = f32_array([0.0, 0.0])
        self.acceleration_wc = f32_array([0.0, 0.0])
        self.rot_angle: float = 0.0
        self.side_slip: float = 0.0
        self.slip_angle_front: float = 0.0
        self.slip_angle_rear: float = 0.0
        self.force = f32_array([0.0, 0.0])
        self.rear_slip: int = 0
        self.front_slip: int = 0
        self.resistance = f32_array([0.0, 0.0])
        self.acceleration = f32_array([0.0, 0.0])
        self.torque: float = 0.0
        self.angular_acceleration: float = 0.0
        self.sin: float = 0.0
        self.cos: float = 0.0
        self.yaw_speed: float = 0.0
        self.weight: float = 0.0
        self.front_traction = f32_array([0.0, 0.0])
        self.lateral_force_front = f32_array([0.0, 0.0])
        self.lateral_force_rear = f32_array([0.0, 0.0])

        self.config = CarConfig()

    def update(self, car_input: CarInput, dt: float):
        sin = np.sin(self.angle)
        cos = np.cos(self.angle)

        self.velocity[0] = cos * self.velocity_wc[1] + sin * self.velocity_wc[0]
        self.velocity[1] = -sin * self.velocity_wc[1] + cos * self.velocity_wc[0]

        if np.linalg.norm(self.velocity) < ZERO:
            self.velocity = np.zeros(2)

        speed = np.linalg.norm(self.velocity)
        print(type(self.velocity[0]))

        yaw_speed = self.config.wheel_base * 0.5 * self.angular_velocity
        if speed > ZERO:
            # lateral force on wheels
            if self.velocity[0] < ZERO:
                rot_angle = 0
            else:
                rot_angle = np.arctan(yaw_speed / self.velocity[0])

            if self.velocity[0] < ZERO:
                side_slip = 0
            else:
                side_slip = np.arctan(self.velocity[1] / self.velocity[0])
            slip_angle_front = side_slip + rot_angle - car_input.steer_angle
            slip_angle_rear = side_slip - rot_angle
        else:
            slip_angle_front = 0
            slip_angle_rear = 0

        # weight per axle
        # TODO: check if better to depend on b and c
        weight = self.config.m * g * 0.5

        # calculate lateral force on front wheels (Ca * slip_angle) capped to friction * load
        self.lateral_force_front[0] = 0
        self.lateral_force_front[1] = self.config.cornering_front * slip_angle_front
        self.lateral_force_front[1] = np.clip(self.lateral_force_front[1], -self.config.max_grip, self.config.max_grip)
        self.lateral_force_front[1] *= weight
        if self.front_slip == 1:
            self.lateral_force_front[1] *= 0.5


        # calculate lateral force on rear wheels (Ca * slip_angle) capped to friction * load
        self.lateral_force_rear[0] = 0
        self.lateral_force_rear[1] = self.config.cornering_rear * slip_angle_rear
        self.lateral_force_rear[1] = np.clip(self.lateral_force_rear[1], -self.config.max_grip, self.config.max_grip)
        self.lateral_force_rear[1] *= weight
        if self.rear_slip == 1:
            self.lateral_force_rear[1] *= 0.5

        # longitudinal force on rear wheels - very simple traction model
        self.front_traction[0] = 150*(car_input.throttle - car_input.brake * np.sign(self.velocity[0]))
        self.front_traction[1] = 0
        if (self.rear_slip==1):
            self.front_traction[0] *= 0.5

        # forces and torque on body
        self.resistance = -(self.config.resistance*self.velocity + self.config.drag*self.velocity*np.absolute(self.velocity))
        # print("resistance:", resistance)

        # sum forces
        self.force[0] = self.front_traction[0] + np.sin(car_input.steer_angle) * self.lateral_force_front[0] + self.lateral_force_rear[0] + self.resistance[0]
        self.force[1] = self.front_traction[1] + np.cos(car_input.steer_angle) * self.lateral_force_front[1] + self.lateral_force_rear[1] + self.resistance[1]
        # print("force:", force)

        # torque on body from lateral forces
        torque = self.config.b * self.lateral_force_front[1] - self.config.c * self.lateral_force_rear[1]

        # acceleration
        self.acceleration[0] = self.force[0] / self.config.m
        self.acceleration[1] = self.force[1] / self.config.m
        angular_acceleration = torque / self.config.inertia
        if np.abs(angular_acceleration) < ZERO:
            angular_acceleration = 0

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
        ANGULAR_DAMPING = 0.99  # Adjust as needed
        self.angular_velocity *= ANGULAR_DAMPING
        if np.abs(self.angular_velocity) < ZERO:
            self.angular_velocity = 0

        self.angle += self.angular_velocity * dt
        self.orientation_vector = f32_array([np.cos(self.angle), np.sin(self.angle)])