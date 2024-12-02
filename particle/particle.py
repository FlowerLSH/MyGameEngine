import pygame
import random
import math

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 5)
        self.color = (random.randint(200, 255), random.randint(100, 200), random.randint(0, 100))
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2, 8)
        self.life = random.randint(30, 60)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 1
        self.size -= 0.1
        self.size = max(0, self.size)

    def draw(self, surface):
        if self.life > 0 and self.size > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class Explosion:
    def __init__(self, x, y, num_particles):
        self.x = x
        self.y = y
        self.particles = [Particle(x, y) for _ in range(num_particles)]

    def update(self):
        for particle in self.particles:
            particle.update()

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

    def is_finished(self):
        return all(particle.life <= 0 for particle in self.particles)

    def apply_to_circles(self, circles):
        for circle in circles:
            dx = circle.x - self.x
            dy = circle.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < 200 and distance > 0:
                force_magnitude = 100 / max(distance, 1)
                force_x = (dx / distance) * force_magnitude
                force_y = (dy / distance) * force_magnitude
                circle.apply_force(force_x, force_y)
