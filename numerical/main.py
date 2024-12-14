import pygame
import numpy as np

dt = 0.02

def RK4(t, y, f):
    k1 = f(t, y)
    k2 = f(t + dt / 2, y + dt * k1 / 2)
    k3 = f(t + dt / 2, y + dt * k2 / 2)
    k4 = f(t + dt, y + dt * k3)

    return y + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

def verlet_integration(y_k, y_k_1, a):
    return 2 * y_k - y_k_1 + a * dt ** 2

def analytic(t):
    x = x0 + vx0 * t
    y = y0 + vy0 * t - 0.5 * g * t ** 2
    return np.array([x, y])

x0, y0 = 0.0, 0.0
vx0, vy0 = 12.0, 30.0
g = 9.8

# 포물선운동
def f(t, pos):
    dxdt = vx0
    dydt = vy0 - g * t
    return np.array([dxdt, dydt])

def a(t, pos):
    return np.array([0, -g])

position = np.array([x0, y0])
velocity = np.array([vx0, vy0])
t0 = 0.0
count = 1000

save_rk4 = []
save_verlet = []

position_copy = position.copy()
for i in range(count):
    save_rk4.append(position_copy)
    position_copy = RK4(t0, position_copy, f)
    t0 += dt

    if position_copy[1] < 0:
        break

t0 = 0.0
position_current = position.copy()
past_position = analytic(-dt)
for i in range(count):
    save_verlet.append(position_current)
    future_position = verlet_integration(position_current, past_position, a(t0, position_current))
    past_position = position_current
    position_current = future_position
    t0 += dt

    if position_current[1] < 0:
        break

t0 = 0.0
save_analytic = []
for i in range(count):
    pos = analytic(t0)
    save_analytic.append(pos)
    t0 += dt
    if pos[1] < 0:
        break

save_rk4 = np.array(save_rk4)
save_verlet = np.array(save_verlet)
save_analytic = np.array(save_analytic)

pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Numerical")
clock = pygame.time.Clock()

scale = 10
trail_rk4 = []
trail_verlet = []
trail_analystic = []
count_index = 0

loopFinished = False

font = pygame.font.Font(None, 36)



while not loopFinished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loopFinished = True


    screen.fill((255, 255, 255))

    if count_index < len(save_rk4):
        x, y = save_rk4[count_index]
        particle_pos = (int(x * scale), int(height - y * scale))
        trail_rk4.append(particle_pos)

    if count_index < len(save_verlet):
        x, y = save_verlet[count_index]
        particle_pos = (int(x * scale), int(height - y * scale))
        trail_verlet.append(particle_pos)

    if count_index < len(save_analytic):
        x, y = save_analytic[count_index]
        particle_pos = (int(x * scale), int(height - y * scale))
        trail_analystic.append(particle_pos)

    
    error_rk4 = [0, 0]
    error_verlet = [0, 0]

    for i in range(len(trail_rk4)):
        error_rk4[0] += (trail_analystic[i][0] - trail_rk4[i][0])
        error_rk4[1] += (trail_analystic[i][1] - trail_rk4[i][1])

    for i in range(len(trail_verlet)):
        error_verlet[0] += (trail_analystic[i][0] - trail_verlet[i][0])
        error_verlet[1] += (trail_analystic[i][1] - trail_verlet[i][1])

    count_index += 1

    if len(trail_rk4) > 1:
        pygame.draw.lines(screen, (255, 0, 0), False, trail_rk4, 2)

    if trail_rk4:
        pygame.draw.circle(screen, (255, 0, 0), trail_rk4[-1], 5)

    if len(trail_verlet) > 1:
        pygame.draw.lines(screen, (0, 0, 255), False, trail_verlet, 2)

    if trail_verlet:
        pygame.draw.circle(screen, (0, 0, 255), trail_verlet[-1], 5)

    if len(trail_analystic) > 1:
        pygame.draw.lines(screen, (0, 255, 0), False, trail_analystic, 2)

    if trail_analystic:
        pygame.draw.circle(screen, (0, 255, 0), trail_analystic[-1], 5)

    error_rk4_text = font.render(f"Error RK4: {error_rk4}", True, (0, 0, 0))
    error_verlet_text = font.render(f"Error Verlet: {error_verlet}", True, (0, 0, 0))

    screen.blit(error_rk4_text, (10, 10))
    screen.blit(error_verlet_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()