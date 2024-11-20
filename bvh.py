import pygame
import calc
import settings as s

class BVHNode:
    def __init__(self, bounds, left=None, right=None):
        self.bounds = bounds
        self.left = left
        self.right = right
        self.is_leaf = (left is None and right is None)
        self.rectangles = []

        if self.is_leaf:
            self.rectangles = [bounds]

    @staticmethod
    def create_hierarchy(rectangles):
        if len(rectangles) == 1:
            node = BVHNode(rectangles[0])
            node.rectangles = [rectangles[0]]
            return node

        nodes = [BVHNode(rect) for rect in rectangles]
        while len(nodes) > 1:
            min_distance = float('inf')
            pair = None

            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    distance = calc.get_distance(nodes[i].bounds, nodes[j].bounds)
                    if distance < min_distance:
                        min_distance = distance
                        pair = (i, j)

            i, j = pair
            merged_bounds = calc.get_outline(nodes[i].bounds, nodes[j].bounds)
            new_node = BVHNode(merged_bounds, nodes[i], nodes[j])

            del nodes[j]
            del nodes[i]
            nodes.append(new_node)

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
