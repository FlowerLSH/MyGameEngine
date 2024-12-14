import pygame
import sys
import subprocess

pygame.init()

WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

BUTTON_WIDTH, BUTTON_HEIGHT = 500, 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Button Example")

font = pygame.font.Font(None, 36)

buttons = [
    pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 100), (BUTTON_WIDTH, BUTTON_HEIGHT)),
    pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2), (BUTTON_WIDTH, BUTTON_HEIGHT)),
    pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 100), (BUTTON_WIDTH, BUTTON_HEIGHT))
]

labels = ["Bounding Volume Hierarchy", "Concave Object Collision Detection", "RK4 and Verlet Integration"]

def draw_buttons():
    for i, button in enumerate(buttons):
        pygame.draw.rect(screen, GRAY, button)
        text = font.render(labels[i], True, BLACK)
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)


def button1_action():
    subprocess.run(["python", "bvh/main.py"])

def button2_action():
    subprocess.run(["python", "concave/main.py"])

def button3_action():
    subprocess.run(["python", "numerical/main.py"])

def main():
    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        if i == 0:
                            button1_action()
                        elif i == 1:
                            button2_action()
                        elif i == 2:
                            button3_action()

        draw_buttons()

        pygame.display.flip()

if __name__ == "__main__":
    main()
