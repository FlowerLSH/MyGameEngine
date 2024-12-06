import pygame
import numpy as np
import math

dt = 0.02

def RK4(t, y, f):
    k1 = f(t, y)
    k2 = f(t + dt / 2, y + dt * k1 / 2)
    k3 = f(t + dt / 2, y + dt * k2 / 2)
    k4 = f(t + dt, y + dt * k3)
    return y + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

omega_x = 5.0
omega_y = 1.5
amplitude_x = 300.0
amplitude_y = 150.0

def f(t, pos):
    dxdt = amplitude_x * math.cos(omega_y * t)
    dydt = amplitude_y * math.sin(omega_x * t) 

    return np.array([dxdt, dydt])

def to_screen_coordinates(x, y, scale, screen_width, screen_height):
    screen_x = int(x * scale + screen_width / 2)
    screen_y = int(-y * scale + screen_height / 2)
    return screen_x, screen_y

x0, y0 = 0.0, 0.0

position = np.array([x0, y0])
t0 = 0.0
count = 1000

save_rk4 = []

position_copy = position.copy()
for i in range(count):
    save_rk4.append(position_copy)
    position_copy = RK4(t0, position_copy, f)
    t0 += dt

save_rk4 = np.array(save_rk4)

pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Advanced")
clock = pygame.time.Clock()

scale = 1
trail_rk4 = []
count_index = 0
loopFinished = False

while not loopFinished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loopFinished = True

    screen.fill((255, 255, 255))

    if count_index < len(save_rk4):
        x, y = save_rk4[count_index]
        particle_pos = to_screen_coordinates(x, y, scale, width, height)
        trail_rk4.append(particle_pos)

    count_index += 1

    if len(trail_rk4) > 1:
        pygame.draw.lines(screen, (255, 0, 0), False, trail_rk4, 2)

    if trail_rk4:
        pygame.draw.circle(screen, (255, 0, 0), trail_rk4[-1], 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
