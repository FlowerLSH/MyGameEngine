import pygame
from bvh import *
import settings as s

class RectangleManager:
    def __init__(self):
        self.rectangles = []
        self.selected_rect = None
        self.speed = 5
        self.bvh = None
        self.player = None
        self.visualize_bvh = False

    def create_rectangle(self, pos):
        new_rect = pygame.Rect(pos[0] - 25, pos[1] - 25, 50, 50)
        self.rectangles.append(new_rect)

    def select_rectangle(self, pos):
        for rect in self.rectangles:
            if rect.collidepoint(pos):
                self.selected_rect = rect
                break
        else:
            self.selected_rect = None

    def delete_selected(self):
        if self.selected_rect:
            self.rectangles.remove(self.selected_rect)
            self.selected_rect = None

    def move(self):
        keys = pygame.key.get_pressed()

        if self.player:
            if keys[pygame.K_a]:
                self.player.x -= self.speed
            if keys[pygame.K_d]:
                self.player.x += self.speed
            if keys[pygame.K_w]:
                self.player.y -= self.speed
            if keys[pygame.K_s]:
                self.player.y += self.speed
            self.player.clamp_ip(pygame.Rect(0, 0, s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        elif self.selected_rect:
            if keys[pygame.K_a]:
                self.selected_rect.x -= self.speed
            if keys[pygame.K_d]:
                self.selected_rect.x += self.speed
            if keys[pygame.K_w]:
                self.selected_rect.y -= self.speed
            if keys[pygame.K_s]:
                self.selected_rect.y += self.speed
            self.selected_rect.clamp_ip(pygame.Rect(0, 0, s.SCREEN_WIDTH, s.SCREEN_HEIGHT))

    def resize_selected(self, delta):
        if self.player:
            self.player.width = max(10, self.player.width + delta)
            self.player.height = max(10, self.player.height + delta)
        elif self.selected_rect:
            self.selected_rect.width = max(10, self.selected_rect.width + delta)
            self.selected_rect.height = max(10, self.selected_rect.height + delta)

    def apply_bvh(self):
        if self.rectangles:
            self.bvh = BVHNode.create_hierarchy(self.rectangles)
            self.visualize_bvh = True

    def toggle_player(self):
        if self.player is None:
            self.player = pygame.Rect(s.SCREEN_WIDTH // 2 - 25, s.SCREEN_HEIGHT // 2 - 25, 50, 50)
            self.selected_rect = None
        else:
            self.player = None

    def draw_rectangles(self, screen):
        for rect in self.rectangles:
            if rect == self.selected_rect and self.player is None:
                pygame.draw.rect(screen, s.BLUE, rect)
            else:
                pygame.draw.rect(screen, s.RED, rect)

        if self.visualize_bvh and self.bvh:
            self.bvh.visualize(screen, s.GOLD)

        if self.player and self.bvh:
            collisions = []
            self.bvh.check_collision(self.player, collisions, screen)
            for rect in collisions:
                pygame.draw.rect(screen, s.FOREST_GREEN, rect)

        if self.player:
            pygame.draw.rect(screen, s.BLACK, self.player)
