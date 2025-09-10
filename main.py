import pygame
import sys
import random
import os

pygame.init()

# 화면
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game Upgraded")

# 색상
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,200,0)
GRAY = (128,128,128)
RED = (255,0,0)
BLUE = (0,0,255)
SKY_DAY = (135,206,235)
SKY_NIGHT = (25,25,112)
BROWN = (160,82,45)
YELLOW = (255, 255, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# 폰트
font = pygame.font.SysFont(None,36)
big_font = pygame.font.SysFont(None,72)

# 효과음
try:
    jump_sound = pygame.mixer.Sound("jump.wav")
    hit_sound = pygame.mixer.Sound("hit.wav")
    item_sound = pygame.mixer.Sound("item.wav")
except:
    jump_sound = hit_sound = item_sound = None

# 하이스코어 파일
HIGH_SCORE_FILE = "highscore.txt"
if os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE,"r") as f:
        high_score = int(f.read())
else:
    high_score = 0

def save_highscore(score):
    global high_score
    if score > high_score:
        high_score = score
        with open(HIGH_SCORE_FILE,"w") as f:
            f.write(str(high_score))

def game_loop():
    # 공룡
    dino_w,dino_h = 40,40
    dino_x,dino_y = 50, HEIGHT - dino_h - 50
    dino_vel_y = 0
    gravity = 0.5
    is_jumping = False
    can_double_jump = False

    # 장애물
    obstacles = []
    spawn_time = 1500
    last_spawn = pygame.time.get_ticks()

    # 익룡
    pterodactyls = []
    ptero_spawn_time = 3000
    last_ptero = pygame.time.get_ticks()

    # 아이템
    items = []
    item_spawn_time = 5000
    last_item = pygame.time.get_ticks()

    # 땅
    ground_h = 20
    ground_x = 0
    ground_speed = 5

    # 구름
    clouds = []
    cloud_spawn_time = 3000
    last_cloud_spawn = pygame.time.get_ticks()

    # 점수/목숨
    score = 0
    lives = 3
    double_jump_active = False

    running = True
    while running:
        # 배경 낮/밤
        if score % 2000 < 1000:
            screen.fill(SKY_DAY)
        else:
            screen.fill(SKY_NIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not is_jumping:
                        dino_vel_y = -10
                        is_jumping = True
                        can_double_jump = True
                        if jump_sound: jump_sound.play()
                    elif can_double_jump and double_jump_active:
                        dino_vel_y = -10
                        can_double_jump = False
                        if jump_sound: jump_sound.play()

        # 공룡 점프
        dino_y += dino_vel_y
        dino_vel_y += gravity
        if dino_y >= HEIGHT - dino_h - ground_h:
            dino_y = HEIGHT - dino_h - ground_h
            is_jumping = False
            can_double_jump = False

        now = pygame.time.get_ticks()

        # 장애물 생성
        if now - last_spawn > spawn_time:
            type_obs = random.choice(["cactus","rock"])
            if type_obs == "cactus":
                obs_h = 40
                obs_w = 20
                color = GREEN
            else:
                obs_h = 30
                obs_w = 30
                color = GRAY
            obstacles.append({"rect": pygame.Rect(WIDTH, HEIGHT-obs_h-ground_h, obs_w, obs_h),
                              "color": color})
            last_spawn = now

        # 익룡 생성
        if now - last_ptero > ptero_spawn_time:
            y_pos = random.randint(50, 200)
            pterodactyls.append({"rect": pygame.Rect(WIDTH, y_pos, 40,20),
                                 "color": YELLOW,
                                 "speed": 7})
            last_ptero = now

        # 아이템 생성
        if now - last_item > item_spawn_time:
            y_pos = HEIGHT - ground_h - 20
            color = random.choice([RED,GREEN,BLUE])
            items.append({"rect": pygame.Rect(WIDTH, y_pos,20,20),"color":color})
            last_item = now

        # 장애물 이동 + 난이도 증가
        for obs in obstacles:
            obs["rect"].x -= ground_speed + score//200

        # 익룡 이동
        for ptero in pterodactyls:
            ptero["rect"].x -= ptero["speed"] + score//200

        # 아이템 이동
        for item in items:
            item["rect"].x -= ground_speed + score//200

        # 구름 생성
        if now - last_cloud_spawn > cloud_spawn_time:
            cloud_y = random.randint(50,150)
            cloud_size = random.randint(20,40)
            clouds.append({"x":WIDTH,"y":cloud_y,"size":cloud_size,"speed":random.uniform(1,3)})
            last_cloud_spawn = now

        # 구름 이동
        for cloud in clouds:
            cloud["x"] -= cloud["speed"]

        dino_rect = pygame.Rect(dino_x,dino_y,dino_w,dino_h)

        # 충돌 체크
        for obs in obstacles[:]:
            if dino_rect.colliderect(obs["rect"]):
                lives -= 1
                obstacles.remove(obs)
                if hit_sound: hit_sound.play()
                if lives<=0:
                    return score

        for ptero in pterodactyls[:]:
            if dino_rect.colliderect(ptero["rect"]):
                lives -= 1
                pterodactyls.remove(ptero)
                if hit_sound: hit_sound.play()
                if lives<=0:
                    return score

        for item in items[:]:
            if dino_rect.colliderect(item["rect"]):
                if item["color"] == RED:
                    lives += 1
                elif item["color"] == GREEN:
                    ground_speed = max(3, ground_speed-2)
                elif item["color"] == BLUE:
                    double_jump_active = True
                items.remove(item)
                if item_sound: item_sound.play()

        # 점수 증가
        score +=1

        # 그리기
        for cloud in clouds:
            x,y,s = cloud["x"], cloud["y"], cloud["size"]
            pygame.draw.circle(screen, WHITE,(int(x),y),s)
            pygame.draw.circle(screen, WHITE,(int(x+s),y+10),s)
            pygame.draw.circle(screen, WHITE,(int(x-s),y+10),s)

        ground_x -= ground_speed
        if ground_x <= -WIDTH:
            ground_x = 0
        pygame.draw.rect(screen,BROWN,(ground_x,HEIGHT-ground_h,WIDTH,ground_h))
        pygame.draw.rect(screen,BROWN,(ground_x+WIDTH,HEIGHT-ground_h,WIDTH,ground_h))

        pygame.draw.rect(screen,BLACK,dino_rect)

        for obs in obstacles:
            pygame.draw.rect(screen,obs["color"],obs["rect"])

        for ptero in pterodactyls:
            pygame.draw.rect(screen,ptero["color"],ptero["rect"])

        for item in items:
            pygame.draw.rect(screen,item["color"],item["rect"])

        # 점수/목숨
        score_text = font.render(f"점수: {score}",True,BLACK)
        lives_text = font.render(f"목숨: {lives}",True,RED)
        high_text = font.render(f"하이스코어: {high_score}",True,BLACK)
        screen.blit(score_text,(10,10))
        screen.blit(lives_text,(10,40))
        screen.blit(high_text,(10,70))

        pygame.display.flip()
        clock.tick(FPS)

def game_over_screen(score):
    save_highscore(score)
    screen.fill(SKY_DAY)
    text1 = big_font.render("게임 오버!", True, BLACK)
    text2 = font.render(f"점수: {score}", True, BLACK)
    text3 = font.render(f"스페이스바를 눌러 다시 시작", True, BLACK)

    screen.blit(text1,(WIDTH//2 - text1.get_width()//2, HEIGHT//2 -100))
    screen.blit(text2,(WIDTH//2 - text2.get_width()//2, HEIGHT//2 -30))
    screen.blit(text3,(WIDTH//2 - text3.get_width()//2, HEIGHT//2 +40))
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
