import pygame
import sys
import os

pygame.init()

# --- Seaded ---
SCREEN_W, SCREEN_H = 640, 480
FPS = 60

BALL_SIZE = 20
PAD_W, PAD_H = 120, 20
PAD_Y = int(SCREEN_H / 1.5)
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
PAD_SPEED = 3

MISS_COLOR = (200, 50, 50)
HIT_COLOR  = (80, 255, 160)
TEXT_COLOR = (240, 192, 64)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Ping-Pong")
clock = pygame.time.Clock()

font = pygame.font.SysFont("monospace", 22, bold=True)

script_dir = os.path.dirname(os.path.abspath(__file__))

# Laadi palli pilt
try:
    ball_img = pygame.image.load(os.path.join(script_dir, "ball-1.png")).convert_alpha()
    ball_img = pygame.transform.scale(ball_img, (BALL_SIZE, BALL_SIZE))
    use_ball_img = True
except Exception:
    use_ball_img = False

# Laadi aluse pilt
try:
    pad_img_raw = pygame.image.load(os.path.join(script_dir, "pad.png")).convert_alpha()
    pad_img = pygame.transform.scale(pad_img_raw, (PAD_W, PAD_H))
    use_pad_img = True
except Exception:
    use_pad_img = False

# --- Mängu olek ---
ball_x = float(SCREEN_W // 2)
ball_y = float(SCREEN_H // 3)
ball_vx = float(BALL_SPEED_X)
ball_vy = float(BALL_SPEED_Y)

pad_x = float((SCREEN_W - PAD_W) // 2)
pad_vx = float(PAD_SPEED)

score = 0
flash_timer = 0
game_over = False

def draw_background():
    screen.fill((30, 30, 60))
    grid_col = (40, 40, 80)
    for x in range(0, SCREEN_W, 40):
        pygame.draw.line(screen, grid_col, (x, 0), (x, SCREEN_H))
    for y in range(0, SCREEN_H, 40):
        pygame.draw.line(screen, grid_col, (0, y), (SCREEN_W, y))

def draw_ball():
    bx = int(ball_x - BALL_SIZE / 2)
    by = int(ball_y - BALL_SIZE / 2)
    if use_ball_img:
        screen.blit(ball_img, (bx, by))
    else:
        pygame.draw.circle(screen, (255, 100, 30), (int(ball_x), int(ball_y)), BALL_SIZE // 2)

def draw_pad():
    px = int(pad_x)
    if use_pad_img:
        screen.blit(pad_img, (px, PAD_Y))
    else:
        color = HIT_COLOR if flash_timer < 0 else (240, 192, 64)
        pygame.draw.rect(screen, color, (px, PAD_Y, PAD_W, PAD_H), border_radius=6)

def draw_score():
    color = MISS_COLOR if score < 0 else HIT_COLOR if score > 0 else TEXT_COLOR
    prefix = "+" if score > 0 else ""
    label = font.render(f"Skoor: {prefix}{score}", True, color)
    screen.blit(label, (12, 10))

def draw_flash():
    if flash_timer > 0:
        alpha = int(flash_timer / 20 * 80)
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, alpha))
        screen.blit(overlay, (0, 0))
    elif flash_timer < 0:
        alpha = int(-flash_timer / 10 * 60)
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((80, 255, 160, alpha))
        screen.blit(overlay, (0, 0))

def draw_game_over():
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    big_font = pygame.font.SysFont("monospace", 40, bold=True)
    small_font = pygame.font.SysFont("monospace", 18)
    txt1 = big_font.render("MÄNG LÄBI", True, (255, 80, 80))
    txt2 = small_font.render(f"Lõpptulemus: {score}", True, (240, 192, 64))
    txt3 = small_font.render("Vajuta R uuesti mängimiseks", True, (180, 180, 180))
    screen.blit(txt1, txt1.get_rect(center=(SCREEN_W//2, SCREEN_H//2 - 50)))
    screen.blit(txt2, txt2.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 10)))
    screen.blit(txt3, txt3.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 50)))

def reset():
    global ball_x, ball_y, ball_vx, ball_vy, pad_x, pad_vx, score, flash_timer, game_over
    ball_x = float(SCREEN_W // 2)
    ball_y = float(SCREEN_H // 3)
    ball_vx = float(BALL_SPEED_X)
    ball_vy = float(BALL_SPEED_Y)
    pad_x = float((SCREEN_W - PAD_W) // 2)
    pad_vx = float(PAD_SPEED)
    score = 0
    flash_timer = 0
    game_over = False

# --- Peaahel ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

    if not game_over:
        ball_x += ball_vx
        ball_y += ball_vy

        if ball_x - BALL_SIZE/2 <= 0:
            ball_x = BALL_SIZE/2
            ball_vx = abs(ball_vx)
        if ball_x + BALL_SIZE/2 >= SCREEN_W:
            ball_x = SCREEN_W - BALL_SIZE/2
            ball_vx = -abs(ball_vx)

        if ball_y - BALL_SIZE/2 <= 0:
            ball_y = BALL_SIZE/2
            ball_vy = abs(ball_vy)

        # Kokkupõrge alusega
        if (ball_vy > 0 and
                ball_y + BALL_SIZE/2 >= PAD_Y and
                ball_y + BALL_SIZE/2 <= PAD_Y + PAD_H + 6 and
                pad_x <= ball_x <= pad_x + PAD_W):
            ball_vy = -abs(ball_vy)
            ball_y = PAD_Y - BALL_SIZE/2
            rel = (ball_x - (pad_x + PAD_W/2)) / (PAD_W/2)
            ball_vx = rel * 6
            if abs(ball_vx) < 1:
                ball_vx = 1.0 if ball_vx >= 0 else -1.0
            score += 1
            flash_timer = -10

        # Miss
        if ball_y - BALL_SIZE/2 > SCREEN_H:
            score -= 1
            flash_timer = 20
            ball_x = float(SCREEN_W // 2)
            ball_y = float(SCREEN_H // 3)
            ball_vx = float(BALL_SPEED_X)
            ball_vy = float(BALL_SPEED_Y)
            if score <= -5:
                game_over = True

        # Alus liigub
        pad_x += pad_vx
        if pad_x <= 0:
            pad_x = 0; pad_vx = abs(pad_vx)
        if pad_x + PAD_W >= SCREEN_W:
            pad_x = SCREEN_W - PAD_W; pad_vx = -abs(pad_vx)

        if flash_timer > 0: flash_timer -= 1
        elif flash_timer < 0: flash_timer += 1

    draw_background()
    draw_flash()
    draw_pad()
    draw_ball()
    draw_score()
    if game_over:
        draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)