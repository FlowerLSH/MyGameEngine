import pygame
import concave
import math
import convex_hull

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("concave")
clock = pygame.time.Clock()

polygon1 = [
    (150, 250), (200, 150), (250, 250), (350, 200), (300, 300),
    (400, 350), (250, 350), (200, 450), (150, 350), (50, 300)
]

polygon2 = [
    (400, 400), (500, 350), (550, 450), (500, 500), (600, 550),
    (500, 600), (450, 650), (400, 550), (350, 500), (300, 400)
]


rotation_speed = 3

speed = 5


def rotate_polygon(polygon, angle, center):
    cx, cy = center
    angle_rad = math.radians(angle)
    rotated_polygon = []
    for x, y in polygon:
        dx, dy = x - cx, y - cy
        rotated_x = dx * math.cos(angle_rad) - dy * math.sin(angle_rad) + cx
        rotated_y = dx * math.sin(angle_rad) + dy * math.cos(angle_rad) + cy
        rotated_polygon.append((rotated_x, rotated_y))
    return rotated_polygon


def get_polygon_center(polygon):
    x_coords = [x for x, y in polygon]
    y_coords = [y for x, y in polygon]
    return sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords)


current_angle = 0
rotation_direction = 0
show_triangles = False
show_convex_hull = False

running = True
while running:
    used_axes = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_triangles = not show_triangles
            elif event.key == pygame.K_LCTRL:
                show_convex_hull = not show_convex_hull

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_w]:
        dy -= speed
    if keys[pygame.K_s]:
        dy += speed
    if keys[pygame.K_a]:
        dx -= speed
    if keys[pygame.K_d]:
        dx += speed

    if keys[pygame.K_q]:
        rotation_direction = -1
    elif keys[pygame.K_e]:
        rotation_direction = 1
    else:
        rotation_direction = 0

    polygon2 = [(x + dx, y + dy) for x, y in polygon2]

    center2 = get_polygon_center(polygon2)
    current_angle += rotation_speed * rotation_direction
    polygon2 = rotate_polygon(polygon2, rotation_speed * rotation_direction, center2)

    polygon1_convex_hull = convex_hull.convex_hull(polygon1)
    polygon2_convex_hull = convex_hull.convex_hull(polygon2)

    triangles1 = concave.ear_clipping_algorithm(polygon1)
    triangles2 = concave.ear_clipping_algorithm(polygon2)

    collision_triangles = []

    if concave.SAT_detect_collision(polygon1_convex_hull, polygon2_convex_hull):
        for t1 in triangles1:
            for t2 in triangles2:
                axes1 = concave.get_axes(t1)
                axes2 = concave.get_axes(t2)
                collision_detected = True
                for axis in axes1 + axes2:
                    poly1_min, poly1_max = concave.project_polygon(axis, t1)
                    poly2_min, poly2_max = concave.project_polygon(axis, t2)
                    if poly1_max < poly2_min or poly2_max < poly1_min:
                        collision_detected = False
                        break
                if collision_detected:
                    collision_triangles.append((t1, t2))

    screen.fill((255, 255, 255))

    if show_triangles:
        drawn_lines = set()
        for triangle in triangles1:
            color = (0, 255, 0) if any(triangle == t1 for t1, _ in collision_triangles) else (255, 0, 0)
            pygame.draw.polygon(screen, color, triangle, 1)

        for triangle in triangles2:
            color = (0, 255, 0) if any(triangle == t2 for _, t2 in collision_triangles) else (255, 0, 0)
            pygame.draw.polygon(screen, color, triangle, 1)
    else:
        polygon1_color = (0, 0, 255) if any(t1 for t1, _ in collision_triangles) else (255, 0, 0)
        polygon2_color = (0, 0, 255) if any(t2 for _, t2 in collision_triangles) else (255, 0, 0)

        pygame.draw.polygon(screen, polygon1_color, polygon1, 2)
        pygame.draw.polygon(screen, polygon2_color, polygon2, 2)

    if show_convex_hull:
        pygame.draw.polygon(screen, (0, 0, 0), polygon1_convex_hull, 2)
        pygame.draw.polygon(screen, (0, 0, 0), polygon2_convex_hull, 2)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
