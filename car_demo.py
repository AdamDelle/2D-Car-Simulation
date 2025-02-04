from multiprocessing.reduction import steal_handle
import pygame
from pygame import Vector2
from car import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_CENTER_X = SCREEN_WIDTH * 0.5
SCREEN_CENTER_Y = SCREEN_HEIGHT * 0.5

RED = [255, 0, 0, 255]
GREEN = [0, 255, 0, 255]
BLUE = [0, 0, 255, 255]
BLACK = [0, 0, 0, 255]

def draw_vector(screen, v, origin, color=GREEN, width=2):
    pygame.draw.line(screen, color, origin, origin+v, width)

black_image = pygame.Surface((1.5*10, 3*10))
black_image.set_colorkey(BLACK)
black_image.fill(BLUE)
def draw_rect(screen, center, angle):
    rotated = pygame.transform.rotate(black_image, angle)
    rect = rotated.get_rect(center = center)
    screen.blit(rotated, rect)


car_input = CarInput(0, 0, 0)
def main():
    # init()
    pygame.init()
    pygame.display.init()
    pygame.joystick.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    clock = pygame.time.Clock()

    car = Car()
    car.position_wc = np.array([SCREEN_CENTER_X*0.1, SCREEN_CENTER_Y*0.1])
    print(car.position_wc)
    running = True
    while running:
        dt = clock.get_time()/1000
        # handle_input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w:
                    car_input.throttle = 1.0
                elif event.key == pygame.K_s:
                    car_input.brake = 1.0
                elif event.key == pygame.K_d:
                    car_input.steer_angle = 1.0
                elif event.key == pygame.K_a:
                    car_input.steer_angle = -1.0

        left_joystick = joysticks[0].get_axis(0)
        left_trigger = joysticks[0].get_axis(4)
        right_trigger = joysticks[0].get_axis(5)
        car_input.steer_angle = -left_joystick*np.pi/4.0
        car_input.throttle = (right_trigger+1) * 0.5 * 100
        car_input.brake = (left_trigger+1) * 0.5 * 100
        print(car_input)

        # update
        car.update(car_input, dt)

        # render
        screen.fill((255, 255, 255))
        # car
        # pygame.draw.circle(screen, [0, 0, 0, 0], Vector2(car.position_wc.tolist()), 10)
        draw_vector(screen, np.array([np.sin(car.angle), np.cos(-car.angle)])*car.config.length, car.position_wc, BLACK, 3)
        draw_vector(screen, np.array([0, car_input.brake]), np.array([SCREEN_CENTER_X - 200, SCREEN_CENTER_Y]))

        # input
        draw_vector(screen, np.array([car_input.steer_angle, 0]), np.array([SCREEN_CENTER_X, SCREEN_CENTER_Y]))
        # draw_vector(screen, acceleration_wc*10, car.position_wc, RED)
        draw_vector(screen, np.array([0, car_input.throttle*100]), np.array([SCREEN_CENTER_X + 200, SCREEN_CENTER_Y]))
        draw_rect(screen, car.position_wc*10, np.rad2deg(car.angle))
        pygame.draw.circle(screen, GREEN, (200, 200), MAX_GRIP*30)
        draw_vector(screen, -np.flip(car.front_traction/car.config.m*30), (200, 200), RED, 2)
        draw_vector(screen,np.flip(car.lateral_force_front/car.config.m*30), (200, 200), RED, 2)
        draw_vector(screen,np.flip(car.lateral_force_front/car.config.m*30)-np.flip(car.front_traction/car.config.m*30), (200, 200), BLACK, 2)
        pygame.display.flip()
        clock.tick(60)

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    main()