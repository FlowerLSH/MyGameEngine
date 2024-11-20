import pygame
import math

def get_distance(rect1: pygame.Rect, rect2: pygame.Rect):
        dx = rect1.centerx - rect2.centerx
        dy = rect1.centery - rect2.centery
        return math.sqrt(dx ** 2 + dy ** 2)

def get_outline(rect1: pygame.Rect, rect2: pygame.Rect):
    x1 = min(rect1.x, rect2.x)
    y1 = min(rect1.y, rect2.y)
    x2 = max(rect1.right, rect2.right)
    y2 = max(rect1.bottom, rect2.bottom)
    return pygame.Rect(x1, y1, x2 - x1, y2 - y1)