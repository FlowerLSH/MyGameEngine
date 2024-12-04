import pygame
import particle
import object

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Explosion Simulation")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)

running = True
explosions = []
circle_manager = object.CircleManager()
explosion_power = 1.0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if event.button == 1:
                explosions.append(particle.Explosion(x, y, 300, power=explosion_power))
            elif event.button == 3:
                circle_manager.create_circle(x, y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                explosion_power = max(0.1, explosion_power - 0.1)
            elif event.key == pygame.K_RIGHT:
                explosion_power = min(5.0, explosion_power + 0.1)
            elif event.key == pygame.K_UP:
                circle_manager.adjust_elastic(0.1)
            elif event.key == pygame.K_DOWN:
                circle_manager.adjust_elastic(-0.1)

    screen.fill(BLACK)

    for explosion in explosions:
        explosion.update()
        explosion.apply_to_circles(circle_manager.circles)
        explosion.draw(screen)
    explosions = [e for e in explosions if not e.is_finished()]

    circle_manager.update(WIDTH, HEIGHT)
    circle_manager.draw(screen)

    font = pygame.font.Font(None, 36)
    power_text = font.render(f"Explosion Power: {explosion_power:.1f}", True, (255, 255, 255))
    elastic_text = font.render(f"Elasticity: {circle_manager.elastic:.1f}", True, (255, 255, 255))
    screen.blit(power_text, (10, 10))
    screen.blit(elastic_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
