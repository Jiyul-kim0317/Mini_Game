import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("사각형 공룡 게임")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
SKY = (135, 206, 235)   # 하늘색
BROWN = (160, 82, 45)   # 땅 색

# FPS
clock = pygame.time.Clock()
FPS = 60

# 글꼴
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

def game_loop():
    # 공룡 설정
    dino_width, dino_height = 40, 40
    dino_x, dino_y = 50, HEIGHT - dino_height - 50
    dino_vel_y = 0
    gravity = 0.5
    is_jumping = False

    # 장애물 설정
    obstacles = []
    obstacle_width, obstacle_height = 20, 40
    obstacle_speed = 5
    spawn_time = 1500  # 1.5초마다 생성
    last_spawn = pygame.time.get_ticks()

    # 땅(바닥) 설정
    ground_height = 20
    ground_x = 0
    ground_speed = 5

    # 구름 설정
    clouds = []
    cloud_speed = 2
    cloud_spawn_time = 3000  # 3초마다 구름 생성
    last_cloud_spawn = pygame.time.get_ticks()

    # 점수
    score = 0

    running = True
    while running:
        screen.fill(SKY)  # 하늘색 배경

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    dino_vel_y = -10
                    is_jumping = True

        # 공룡 점프
        dino_y += dino_vel_y
        dino_vel_y += gravity
        if dino_y >= HEIGHT - dino_height - ground_height:
            dino_y = HEIGHT - dino_height - ground_height
            is_jumping = False

        # 장애물 생성
        now = pygame.time.get_ticks()
        if now - last_spawn > spawn_time:
            obstacles.append(pygame.Rect(WIDTH, HEIGHT - obstacle_height - ground_height, obstacle_width, obstacle_height))
            last_spawn = now

        # 장애물 이동
        for obs in obstacles:
            obs.x -= obstacle_speed

        # 구름 생성
        if now - last_cloud_spawn > cloud_spawn_time:
            cloud_y = random.randint(50, 150)
            cloud_size = random.randint(20, 40)
            clouds.append({"x": WIDTH, "y": cloud_y, "size": cloud_size})
            last_cloud_spawn = now

        # 구름 이동
        for cloud in clouds:
            cloud["x"] -= cloud_speed

        # 충돌 체크
        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        for obs in obstacles:
            if dino_rect.colliderect(obs):
                return score  # 점수 반환하고 종료

        # 점수 업데이트
        score += 1
        score_text = font.render(f"점수: {score}", True, BLACK)

        # 땅 움직임 효과 (무한 반복)
        ground_x -= ground_speed
        if ground_x <= -WIDTH:
            ground_x = 0

        # 그리기
        pygame.draw.rect(screen, BLACK, dino_rect)  # 공룡
        for obs in obstacles:
            pygame.draw.rect(screen, GREEN, obs)  # 장애물
        screen.blit(score_text, (10, 10))

        # 땅 그리기
        pygame.draw.rect(screen, BROWN, (ground_x, HEIGHT - ground_height, WIDTH, ground_height))
        pygame.draw.rect(screen, BROWN, (ground_x + WIDTH, HEIGHT - ground_height, WIDTH, ground_height))

        # 구름 그리기
        for cloud in clouds:
            x, y, s = cloud["x"], cloud["y"], cloud["size"]
            pygame.draw.circle(screen, WHITE, (x, y), s)
            pygame.draw.circle(screen, WHITE, (x + s, y + 10), s)
            pygame.draw.circle(screen, WHITE, (x - s, y + 10), s)

        pygame.display.flip()
        clock.tick(FPS)

def game_over_screen(score):
    screen.fill(SKY)
    text1 = big_font.render("게임 오버!", True, BLACK)
    text2 = font.render(f"점수: {score}", True, BLACK)
    text3 = font.render("스페이스바를 눌러 다시 시작하세요", True, BLACK)

    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 100))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 - 30))
    screen.blit(text3, (WIDTH//2 - text3.get_width()//2, HEIGHT//2 + 40))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# 메인 루프
while True:
    final_score = game_loop()
    game_over_screen(final_score)
