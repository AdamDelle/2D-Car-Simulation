from typing import Tuple

import pygame

RED = [255, 0, 0, 255]
GREEN = [0, 255, 0, 255]
BLUE = [0, 0, 255, 255]
BLACK = [0, 0, 0, 255]

def draw_vector(screen, v, origin, color=GREEN, width=2):
    pygame.draw.line(screen, color, origin, origin+v, width)

def draw_rect(screen, image, center, angle):
    """
    pass an input `image` created like:
        image = pygame.Surface((1.5*10, 3*10))
        image.set_colorkey(BLACK)   # key/gamma color
        image.fill(BLUE)            # actual color of the rect
    """
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center = center)
    screen.blit(rotated, rect)

def get_image_and_rect(image_path: str, scale: float = 1, angle: float = 0, x: int = 0, y: int = 0) -> Tuple[pygame.Surface, pygame.Rect]:
    image = pygame.image.load(image_path)
    image = scale_image(image, scale)
    image = pygame.transform.rotate(image, angle)
    rect = image.get_rect()
    set_rect_center(rect, (x, y))
    return image, rect

def scale_image(image: pygame.Surface, scale: float) -> pygame.Surface:
    return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))

def set_rect_center(rect: pygame.Rect, center: Tuple[int, int]):
    rect.centerx = center[0]
    rect.centery = center[1]
    return rect