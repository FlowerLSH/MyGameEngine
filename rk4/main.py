import pygame
import numpy as np

dt = 0.02



def RK4(t, y, f):
    k1 = f(t, y)
    k2 = f(t + dt / 2, y + dt * k1 / 2)
    k3 = f(t + dt / 2, y + dt * k2 / 2)
    k4 = f(t + dt, y + dt * k3)

    return y + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

x0, y0 = 0.0, 0.0
vx0, vy0 = 12.0, 30.0

# 포물선운동
def f(t, pos):
    x, y = pos
    g = 9.8

    dxdt = vx0
    dydt = vy0 - g * t
    return np.array([dxdt, dydt])

position = np.array([x0, y0])
t0 = 0.0
count = 1000

save = []

for i in range(count):
    save.append(position)
    position = RK4(t0, position, f)
    t0 += dt

    if position[1] < 0:
        break

save = np.array(save)

pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("RK4")
clock = pygame.time.Clock()

scale = 10
trail = []
count_index = 0

loopFinished = False

while not loopFinished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loopFinished = True

    screen.fill((0, 0, 0))

    if count_index < len(save):
        x, y = save[count_index]
        particle_pos = (int(x * scale), int(height - y * scale))
        trail.append(particle_pos)
        count_index += 1

    if len(trail) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, trail, 2)

    if trail:
        pygame.draw.circle(screen, (255, 0, 0), trail[-1], 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()