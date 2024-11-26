import pygame
from player import Player
from wall import Wall

pygame.init()

map_width = 400
map_height = 400
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ray casting")

minimap_size = (200, 200)
minimap_scale_x = minimap_size[0] / map_width
minimap_scale_y = minimap_size[1] / map_height
minimap_surface = pygame.Surface(minimap_size)

walls = [
    Wall(0, 0, map_width, 10, color=(128, 0, 0)),
    Wall(0, map_height - 10, map_width, 10, color=(0, 128, 0)),
    Wall(0, 0, 10, map_height, color=(0, 0, 128)),
    Wall(map_width - 10, 0, 10, map_height, color=(128, 128, 0)),

    Wall(50, 50, 100, 10, color=(128, 0, 128)),
    Wall(50, 100, 10, 100, color=(0, 128, 128)),
    Wall(150, 150, 100, 10, color=(192, 128, 0)),
    Wall(250, 200, 10, 100, color=(128, 192, 64)),
    Wall(100, 250, 150, 10, color=(64, 64, 192)),
    Wall(200, 100, 10, 100, color=(192, 64, 64)),
    Wall(300, 50, 10, 150, color=(64, 192, 192)),
    Wall(50, 300, 200, 10, color=(255, 128, 128)),
    Wall(300, 250, 10, 100, color=(128, 128, 255)),
    Wall(200, 300, 10, 100, color=(255, 255, 128)),
    Wall(100, 350, 200, 10, color=(255, 128, 0)),

    Wall(75, 75, 100, 10, color=(255, 0, 0)),
    Wall(75, 150, 10, 75, color=(0, 255, 0)),
    Wall(175, 175, 50, 10, color=(0, 0, 255)),
    Wall(275, 225, 10, 75, color=(255, 255, 0)),
    Wall(125, 275, 100, 10, color=(0, 255, 255)),
    Wall(225, 125, 10, 50, color=(255, 0, 255)),
    Wall(325, 75, 10, 75, color=(128, 64, 0)),
    Wall(75, 325, 150, 10, color=(64, 128, 192)),
    Wall(325, 275, 10, 50, color=(192, 64, 192)),
    Wall(225, 325, 10, 75, color=(128, 255, 64)),
    Wall(125, 375, 200, 10, color=(192, 128, 128)),
]

player = Player(40, 40, 0, ray_count=200)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(walls)

    screen.fill((0, 0, 0))
    minimap_surface.fill((255, 255, 255))

    for wall in walls:
        wall.draw(minimap_surface, minimap_scale_x, minimap_scale_y)

    player.draw(minimap_surface, minimap_scale_x, minimap_scale_y)

    player.draw_main(screen, screen_width, screen_height)

    screen.blit(minimap_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
