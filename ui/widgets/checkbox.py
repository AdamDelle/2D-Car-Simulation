import pygame

class Checkbox:
    def __init__(self, x, y, size, label=""):
        self.rect = pygame.Rect(x, y, size, size)
        self.label = label
        self.checked = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        if self.checked:
            pygame.draw.line(screen, (255, 255, 255), (self.rect.left, self.rect.top), (self.rect.right, self.rect.bottom), 2)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.top), 2)
        if self.label:
            label_surface = self.font.render(self.label, True, (255, 255, 255))
            screen.blit(label_surface, (self.rect.right + 10, self.rect.centery - label_surface.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                return True
        return False