import pygame
import math
import pygame.gfxdraw


class Speedometer:
    def __init__(self, x, y, radius, max_speed):
        """
        Initialize the speedometer
        x, y: position of the center of the speedometer
        radius: radius of the speedometer
        max_speed: maximum speed that can be displayed
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.max_speed = max_speed
        self.current_speed = 0

        # Colors
        self.background_color = (20, 20, 20)
        self.text_color = (255, 255, 255)
        self.needle_color = (255, 0, 0)
        self.marking_color = (200, 200, 200)

        # Angles for the speedometer (in radians)
        self.start_angle = math.pi * 1.2  # ~216 degrees (8 o'clock)
        self.end_angle = math.pi * -0.1    # ~54 degrees (4 o'clock)

        # Create font
        self.font = pygame.font.SysFont('Arial', int(radius * 0.3))

    def update(self, speed):
        """Update the current speed"""
        self.current_speed = abs(min(speed, self.max_speed))

    def draw_aa_circle(self, surface, color, pos, radius, width=0):
        """Draw an anti-aliased circle"""
        x, y = pos
        if width == 0:  # Filled circle
            pygame.gfxdraw.aacircle(surface, int(x), int(y), radius, color)
            pygame.gfxdraw.filled_circle(surface, int(x), int(y), radius, color)
        else:  # Outlined circle
            for w in range(width):
                pygame.gfxdraw.aacircle(surface, int(x), int(y), radius - w, color)

    def draw_aa_line(self, surface, color, start_pos, end_pos, width=1):
        """Draw an anti-aliased line"""
        x1, y1 = start_pos
        x2, y2 = end_pos

        # Draw multiple lines for thickness
        if width > 1:
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx ** 2 + dy ** 2)

            if length > 0:
                dx = dx / length
                dy = dy / length

                for i in range(width):
                    offset = (i - (width - 1) / 2)
                    pygame.gfxdraw.line(surface,
                                        int(x1 + dy * offset), int(y1 - dx * offset),
                                        int(x2 + dy * offset), int(y2 - dx * offset),
                                        color)
        else:
            pygame.gfxdraw.line(surface, int(x1), int(y1), int(x2), int(y2), color)

    def draw(self, screen):
        """Draw the speedometer on the screen"""
        # Draw the background circle
        self.draw_aa_circle(screen, self.background_color, (self.x, self.y), self.radius)
        self.draw_aa_circle(screen, self.marking_color, (self.x, self.y), self.radius, 2)

        # Draw the markings
        for i in range(11):
            speed = i * (self.max_speed / 10)
            # Reverse the angle calculation to make it go clockwise
            angle = self.start_angle + (self.end_angle - self.start_angle) * (speed / self.max_speed)

            start_pos = (
                self.x + (self.radius - 20) * math.cos(angle),
                self.y - (self.radius - 20) * math.sin(angle)
            )
            end_pos = (
                self.x + self.radius * math.cos(angle),
                self.y - self.radius * math.sin(angle)
            )

            self.draw_aa_line(screen, self.marking_color, start_pos, end_pos, 2)

            # Draw speed numbers
            if i % 2 == 0:  # Draw every second number
                text = self.font.render(str(int(speed)), True, self.text_color)
                text_pos = (
                    self.x + (self.radius - 40) * math.cos(angle) - text.get_width() // 2,
                    self.y - (self.radius - 40) * math.sin(angle) - text.get_height() // 2
                )
                screen.blit(text, text_pos)

        # Draw the needle
        speed_angle = self.start_angle + (self.end_angle - self.start_angle) * (self.current_speed / self.max_speed)
        needle_length = self.radius - 10
        needle_end = (
            self.x + needle_length * math.cos(speed_angle),
            self.y - needle_length * math.sin(speed_angle)
        )
        self.draw_aa_line(screen, self.needle_color, (self.x, self.y), needle_end, 3)

        # Draw center circle
        self.draw_aa_circle(screen, self.needle_color, (self.x, self.y), 10)

        # Draw current speed text
        speed_text = self.font.render(f"{int(self.current_speed)} km/h", True, self.text_color)
        text_pos = (self.x - speed_text.get_width() // 2, self.y + self.radius // 2)
        screen.blit(speed_text, text_pos)