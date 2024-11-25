import pygame
import math
import settings as s

# 초기화
pygame.init()
screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# 첫 번째 사각형 정보
rect1 = pygame.Rect(375, 275, 50, 50)
rect1_color = s.RED
velocity1 = [0, 0]
mass1 = 10

# 두 번째 사각형 정보
rect2 = pygame.Rect(200, 150, 50, 50)
rect2_color = s.BLUE
velocity2 = [0, 0]
mass2 = 10

# 드래그 관련 변수
dragging = False
current_rect = None
start_pos = None
end_pos = None
drag_start_time = 0

# 탄성 계수 (1.0이 기본값)
elasticity = 1.0

# 게임 루프
loopFinished = False
while not loopFinished:
    dt = clock.tick(60) / 500
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loopFinished = True

        # 마우스 드래그 시작
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect1.collidepoint(event.pos):
                dragging = True
                velocity1 = [0, 0]
                current_rect = rect1
                start_pos = event.pos

            elif rect2.collidepoint(event.pos):
                dragging = True
                velocity2 = [0, 0]
                current_rect = rect2
                start_pos = event.pos


        # 마우스 드래그 끝
        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                end_pos = event.pos


                # 거리와 시간 계산
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                distance = math.sqrt(dx**2 + dy**2)

                if distance:
                    speed = distance
                    direction = (dx / distance, dy / distance)
                    if current_rect == rect1:
                        velocity1 = [speed * direction[0], speed * direction[1]]
                    elif current_rect == rect2:
                        velocity2 = [speed * direction[0], speed * direction[1]]
    
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_q:
                mass1 += 1
            if event.key == pygame.K_a:
                mass1 = min(1, mass1-1)
            if event.key == pygame.K_w:
                mass2 += 1
            if event.key == pygame.K_s:
                mass2 -= min(1, mass2-1)

        # 마우스 휠로 탄성 계수 조정
        if event.type == pygame.MOUSEWHEEL:
            elasticity += event.y * 0.05
            elasticity = max(0, min(1, elasticity))  # 탄성 계수 범위: 0.0 ~ 1.0

    # 첫 번째 사각형 이동
    rect1.x += velocity1[0] * dt
    rect1.y += velocity1[1] * dt

    # 두 번째 사각형 이동
    rect2.x += velocity2[0] * dt
    rect2.y += velocity2[1] * dt

    # 화면 경계 충돌 처리 (첫 번째 사각형)
    if rect1.left < 0:
        rect1.left = 0
        velocity1[0] = -velocity1[0] * elasticity
    if rect1.right > s.SCREEN_WIDTH:
        rect1.right = s.SCREEN_WIDTH
        velocity1[0] = -velocity1[0] * elasticity
    if rect1.top < 0:
        rect1.top = 0
        velocity1[1] = -velocity1[1] * elasticity
    if rect1.bottom > s.SCREEN_HEIGHT:
        rect1.bottom = s.SCREEN_HEIGHT
        velocity1[1] = -velocity1[1] * elasticity

    # 화면 경계 충돌 처리 (두 번째 사각형)
    if rect2.left < 0:
        rect2.left = 0
        velocity2[0] = -velocity2[0] * elasticity
    if rect2.right > s.SCREEN_WIDTH:
        rect2.right = s.SCREEN_WIDTH
        velocity2[0] = -velocity2[0] * elasticity
    if rect2.top < 0:
        rect2.top = 0
        velocity2[1] = -velocity2[1] * elasticity
    if rect2.bottom > s.SCREEN_HEIGHT:
        rect2.bottom = s.SCREEN_HEIGHT
        velocity2[1] = -velocity2[1] * elasticity

    # 사각형 간 충돌 처리
    if rect1.colliderect(rect2):

        velocity1_x = velocity1[0] - (mass1 / (mass1 + mass2)) * (1 + elasticity) * (velocity1[0] - velocity2[0])
        velocity2_x = velocity2[0] + (mass2 / (mass1 + mass2)) * (1 + elasticity) * (velocity1[0] - velocity2[0])

        velocity1_y = velocity1[1] - (mass1 / (mass1 + mass2)) * (1 + elasticity) * (velocity1[1] - velocity2[1])
        velocity2_y = velocity2[1] + (mass2 / (mass1 + mass2)) * (1 + elasticity) * (velocity1[1] - velocity2[1])

        velocity1 = [velocity1_x, velocity1_y]
        velocity2 = [velocity2_x, velocity2_y]
        print(velocity1)
        print(velocity2)

    # 화면 그리기
    screen.fill(s.WHITE)
    pygame.draw.rect(screen, rect1_color, rect1)
    pygame.draw.rect(screen, rect2_color, rect2)

    # 탄성 계수 표시
    elasticity_text = font.render(f"Elasticity: {elasticity:.2f}", True, s.BLACK)
    screen.blit(elasticity_text, (10, 10))
    elasticity_text = font.render(f"Mass1: {mass1}", True, s.BLACK)
    screen.blit(elasticity_text, (250, 10))
    elasticity_text = font.render(f"Mass2: {mass2}", True, s.BLACK)
    screen.blit(elasticity_text, (400, 10))

    # 업데이트
    pygame.display.flip()

pygame.quit()
