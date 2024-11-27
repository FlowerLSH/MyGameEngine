import math

class Line:
    def __init__(self, start_pos, angle, max_distance=1200):
        self.start_pos = start_pos
        self.angle = angle
        self.max_distance = max_distance
        self.hit = False
        self.distance = max_distance
        self.color = None

    def cast(self, walls):
        x, y = self.start_pos
        dx = math.cos(math.radians(self.angle))
        dy = -math.sin(math.radians(self.angle))

        closest_distance = self.max_distance
        hit_color = None
        hit = False

        for wall in walls:
            wall_points = [
                (wall.rect.left, wall.rect.top),
                (wall.rect.right, wall.rect.top),
                (wall.rect.right, wall.rect.bottom),
                (wall.rect.left, wall.rect.bottom),
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

        self.hit = hit
        self.distance = closest_distance
        self.color = hit_color

    def get_corrected_distance(self, player_angle):
        angle_offset = math.radians(self.angle - player_angle)
        return self.distance * math.cos(angle_offset)
