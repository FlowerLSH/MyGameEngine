import pygame
import math

def get_distance(poly1, poly2):
    dx = poly1.centerx - poly2.centerx
    dy = poly1.centery - poly2.centery
    return math.sqrt(dx ** 2 + dy ** 2)

def get_outline(poly1, poly2):
    if isinstance(poly1, pygame.Rect):
        vertices1 = [(poly1.x, poly1.y), (poly1.right, poly1.y), (poly1.x, poly1.bottom), (poly1.right, poly1.bottom)]
    else:
        vertices1 = poly1.vertices

    if isinstance(poly2, pygame.Rect):
        vertices2 = [(poly2.x, poly2.y), (poly2.right, poly2.y), (poly2.x, poly2.bottom), (poly2.right, poly2.bottom)]
    else:
        vertices2 = poly2.vertices

    vertices = vertices1 + vertices2

    x1 = min(point[0] for point in vertices)
    y1 = min(point[1] for point in vertices)
    x2 = max(point[0] for point in vertices)
    y2 = max(point[1] for point in vertices)

    
    return pygame.Rect(x1, y1, x2 - x1, y2 - y1)