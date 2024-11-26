import pygame

class Wall:
    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface, minimap_scale_x, minimap_scale_y):
        wall_minimap = pygame.Rect(
            self.rect.x * minimap_scale_x, self.rect.y * minimap_scale_y,
            self.rect.width * minimap_scale_x, self.rect.height * minimap_scale_y
        )
        pygame.draw.rect(surface, self.color, wall_minimap)
