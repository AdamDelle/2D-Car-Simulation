from abc import ABC, abstractmethod


class Screen(ABC):

    WIDTH = 1920
    HEIGHT = 1080
    CENTER_X = WIDTH // 2
    CENTER_Y = HEIGHT // 2

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def draw(self, dt):
        pass