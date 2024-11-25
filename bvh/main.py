import pygame
import sys
import settings as s
from rectangle_manager import RectangleManager

pygame.init()

screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
clock = pygame.time.Clock()

rect_manager = RectangleManager()

show_bvh = False

loopFinished = False
while not loopFinished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loopFinished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                rect_manager.create_rectangle(event.pos)
            elif event.button == 1:
                rect_manager.select_rectangle(event.pos)
            elif event.button == 4:
                rect_manager.resize_selected(5)
            elif event.button == 5:
                rect_manager.resize_selected(-5)
                
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_DELETE:
                rect_manager.delete_selected()
            if event.key == pygame.K_p:
                rect_manager.toggle_player()
            if event.key == pygame.K_SPACE:
                show_bvh = not show_bvh
                
    if show_bvh:
        rect_manager.apply_bvh()
    rect_manager.move()

    screen.fill(s.WHITE)
    rect_manager.draw_rectangles(screen)

    pygame.display.flip()
    clock.tick(60)  

pygame.quit()
sys.exit()
