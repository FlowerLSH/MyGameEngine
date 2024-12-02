import pygame
import math

class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (0, 0, 255)
        self.vx = 0
        self.vy = 0

    def apply_force(self, fx, fy):
        self.vx += fx
        self.vy += fy

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95
        self.vy *= 0.95

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def is_outside_screen(self, width, height):
        return (
            self.x + self.radius < 0 or self.x - self.radius > width or
            self.y + self.radius < 0 or self.y - self.radius > height
        )

    def collide_with(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2 + dy**2)
        return distance < self.radius + other.radius

    def resolve_collision(self, other, elastic):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            return

        overlap = self.radius + other.radius - distance
        nx, ny = dx / distance, dy / distance

        self.vx += nx * overlap * elastic
        self.vy += ny * overlap * elastic
        other.vx -= nx * overlap * elastic
        other.vy -= ny * overlap * elastic


class CircleManager:
    def __init__(self):
        self.circles = []
        self.elastic = 0.5

    def create_circle(self, x, y):
        self.circles.append(Circle(x, y))

    def apply_explosion(self, explosion_x, explosion_y, explosion_radius):
        for circle in self.circles:
            dx = circle.x - explosion_x
            dy = circle.y - explosion_y
            distance = (dx**2 + dy**2)**0.5
            if distance < explosion_radius and distance > 0:
                force_magnitude = 100 / distance
                fx = (dx / distance) * force_magnitude
                fy = (dy / distance) * force_magnitude
                circle.apply_force(fx, fy)

    def update(self, width, height):
        for circle in self.circles:
            circle.update()

        for i in range(len(self.circles)):
            for j in range(i + 1, len(self.circles)):
                if self.circles[i].collide_with(self.circles[j]):
                    self.circles[i].resolve_collision(self.circles[j], self.elastic)

        self.circles = [c for c in self.circles if not c.is_outside_screen(width, height)]

    def draw(self, surface):
        for circle in self.circles:
            circle.draw(surface)

    def adjust_elastic(self, delta):
        self.elastic = max(0.1, min(1, self.elastic + delta))
