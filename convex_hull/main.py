import pygame
import math

pygame.init()

screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()

polygon = [(100, 100), (300, 100), (300, 300), (250, 250), (200, 250), (200, 200), (150, 150), (100, 200)]

def cross_product(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points):
    points = sorted(points)
    lower = []
    for point in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]

sorted_polygon = convex_hull(polygon)

running = True
font = pygame.font.Font(None, 24)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.polygon(screen, (0, 0, 255), polygon, 1)
    pygame.draw.polygon(screen, (255, 0, 0), sorted_polygon, 1)

    for idx, point in enumerate(polygon):
        pygame.draw.circle(screen, (0, 0, 255), point, 5)
        text = font.render(str(idx), True, (0, 0, 255))
        screen.blit(text, (point[0] + 5, point[1] + 5))

    for idx, point in enumerate(sorted_polygon):
        pygame.draw.circle(screen, (255, 0, 0), point, 5)
        text = font.render(str(idx), True, (255, 0, 0))
        screen.blit(text, (point[0] + 5, point[1] - 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
