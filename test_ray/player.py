import pygame
import math
from line import Line

class Player:
    def __init__(self, x, y, angle, size=5, speed=1, rotation_speed=1, vision=60, ray_count=300):
        self.pos = [x, y]
        self.angle = angle
        self.size = size
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.vision = vision
        self.ray_count = ray_count
        self.rays = []

    def handle_input(self):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.pos[0], self.pos[1]
        if keys[pygame.K_w]:
            new_x += self.speed * math.cos(math.radians(self.angle))
            new_y -= self.speed * math.sin(math.radians(self.angle))
        if keys[pygame.K_s]:
            new_x -= self.speed * math.cos(math.radians(self.angle))
            new_y += self.speed * math.sin(math.radians(self.angle))
        if keys[pygame.K_a]:
            new_x -= self.speed * math.cos(math.radians(self.angle - 90))
            new_y += self.speed * math.sin(math.radians(self.angle - 90))
        if keys[pygame.K_d]:
            new_x += self.speed * math.cos(math.radians(self.angle - 90))
            new_y -= self.speed * math.sin(math.radians(self.angle - 90))
        if keys[pygame.K_q]:
            self.angle += self.rotation_speed
        if keys[pygame.K_e]:
            self.angle -= self.rotation_speed

        return new_x, new_y

    def resolve_collision(self, new_x, new_y, walls):
        player_rect = pygame.Rect(new_x - self.size, new_y - self.size, self.size * 2, self.size * 2)
        for wall in walls:
            if wall.rect.colliderect(player_rect):
                if player_rect.right > wall.rect.left and player_rect.left < wall.rect.left:
                    new_x = wall.rect.left - self.size
                elif player_rect.left < wall.rect.right and player_rect.right > wall.rect.right:
                    new_x = wall.rect.right + self.size
                if player_rect.bottom > wall.rect.top and player_rect.top < wall.rect.top:
                    new_y = wall.rect.top - self.size
                elif player_rect.top < wall.rect.bottom and player_rect.bottom > wall.rect.bottom:
                    new_y = wall.rect.bottom + self.size
        return new_x, new_y

    def cast_ray(self, angle, walls):
        x, y = self.pos
        dx = math.cos(math.radians(angle))
        dy = -math.sin(math.radians(angle))

        max_distance = 1200
        closest_distance = max_distance
        hit = False
        hit_color = None

        for wall in walls:
            wall_points = [
                (wall.rect.left, wall.rect.top),
                (wall.rect.right, wall.rect.top),
                (wall.rect.right, wall.rect.bottom),
                (wall.rect.left, wall.rect.bottom)
            ]
            for i in range(len(wall_points)):
                x1, y1 = wall_points[i]
                x2, y2 = wall_points[(i + 1) % 4]

                denominator = (x2 - x1) * dy - (y2 - y1) * dx
                if denominator == 0:
                    continue

                t = ((x - x1) * dy - (y - y1) * dx) / denominator
                u = ((x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)) / denominator

                if 0 <= t <= 1 and u >= 0:
                    distance = u
                    if distance < closest_distance:
                        closest_distance = distance
                        hit = True
                        hit_color = wall.color

        return hit, closest_distance, hit_color

    def cast_rays(self, walls):
        self.rays = []
        start_angle = self.angle - (self.vision / 2)
        angle_step = self.vision / self.ray_count

        for i in range(self.ray_count):
            ray_angle = start_angle + i * angle_step
            ray = Line(self.pos, ray_angle)
            ray.cast(walls)
            self.rays.append(ray)

    def update(self, walls):
        new_x, new_y = self.handle_input()
        self.pos[0], self.pos[1] = self.resolve_collision(new_x, new_y, walls)
        self.cast_rays(walls)

    def draw(self, surface, minimap_scale_x, minimap_scale_y):
        player_minimap_x, player_minimap_y = int(self.pos[0] * minimap_scale_x), int(self.pos[1] * minimap_scale_y)
        pygame.draw.circle(surface, (0, 0, 255), (player_minimap_x, player_minimap_y), int(self.size * minimap_scale_x))

        line_length = 50
        end_x = int(player_minimap_x + line_length * math.cos(math.radians(self.angle)))
        end_y = int(player_minimap_y - line_length * math.sin(math.radians(self.angle)))
        pygame.draw.line(surface, (255, 0, 0), (player_minimap_x, player_minimap_y), (end_x, end_y), 2)

    def draw_main(self, screen, width, height):
        max_distance = 2000

        for i, ray in enumerate(self.rays):
            if not ray.hit:
                continue

            corrected_distance = ray.get_corrected_distance(self.angle)
            distance_ratio = corrected_distance / max_distance
            brightness = max(0, min(255, int(255 * (1 - math.sqrt(distance_ratio)))))

            base_color = ray.color
            shaded_color = (
                int(base_color[0] * (brightness / 255)),
                int(base_color[1] * (brightness / 255)),
                int(base_color[2] * (brightness / 255)),
            )

            line_height = height * 4.5 / corrected_distance
            line_width = width / self.ray_count

            centerx = width - line_width - (i * line_width)
            centery = height // 2

            top_left_x = centerx
            top_left_y = centery - line_height // 2

            rect = pygame.Rect(top_left_x, top_left_y, line_width, line_height)
            screen.fill(shaded_color, rect)

