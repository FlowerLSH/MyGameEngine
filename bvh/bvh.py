import pygame
import calc
import settings as s
import heapq


class BVHNode:
    def __init__(self, bounds, left=None, right=None):
        self.bounds = bounds
        self.left = left
        self.right = right
        self.is_leaf = (left is None and right is None)
        self.rectangles = []

        if self.is_leaf:
            self.rectangles = [bounds]

    def create_hierarchy(rectangles):
        nodes = [BVHNode(rect) for rect in rectangles]

        heap = []
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                distance = calc.get_distance(nodes[i].bounds, nodes[j].bounds)
                heapq.heappush(heap, (distance, i, j))
        
        while len(nodes) > 1:
            distance, i, j = heapq.heappop(heap)
            
            try:
                outline = calc.get_outline(nodes[i].bounds, nodes[j].bounds)
            except:
                continue
            new = BVHNode(outline, nodes[i], nodes[j])

            nodes.append(new)

            del nodes[j]
            del nodes[i]

            for i in range(len(nodes) - 1):
                distance = calc.get_distance(nodes[i].bounds, new.bounds)
                heapq.heappush(heap, (distance, i, len(nodes) - 1))

        return nodes[0]

    def check_collision(self, rect, collisions, screen=None):
        if not self.bounds.colliderect(rect):
            return False

        if screen:
            pygame.draw.rect(screen, s.PURPLE, self.bounds, 1)

        if self.is_leaf:
            for r in self.rectangles:
                if rect.colliderect(r):
                    collisions.append(r)
        else:
            if self.left:
                self.left.check_collision(rect, collisions, screen)
            if self.right:
                self.right.check_collision(rect, collisions, screen)

        return True

    def visualize(self, screen, color):
        pygame.draw.rect(screen, color, self.bounds, 1)
        if self.left:
            self.left.visualize(screen, color)
        if self.right:
            self.right.visualize(screen, color)
