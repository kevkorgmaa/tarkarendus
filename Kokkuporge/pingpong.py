import pygame
import sys
import os

pygame.init()

# Seaded
SCREEN_W, SCREEN_H = 640, 480
FPS = 60

BALL_SIZE = 20
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

PAD_W, PAD_H = 120, 20
PAD_Y = int(SCREEN_H / 1.5)
PAD_SPEED = 3

BG_COLOR = (153, 204, 255)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("PingPong")
clock = pygame.time.Clock()

script_dir = os.path.dirname(os.path.abspath(__file__))

# Palli pilt
try:
    ball_img = pygame.image.load(
        os.path.join(script_dir, "ball-1.png")
    ).convert_alpha()
    ball_img = pygame.transform.scale(
        ball_img,
        (BALL_SIZE, BALL_SIZE)
    )
    use_ball_img = True
except:
    use_ball_img = False

# Platvormi pilt
try:
    pad_img_raw = pygame.image.load(
        os.path.join(script_dir, "pad.png")
    ).convert_alpha()
    pad_img = pygame.transform.scale(
        pad_img_raw,
        (PAD_W, PAD_H)
    )
    use_pad_img = True
except:
    use_pad_img = False

# Pall spawnib paremas ülemises nurgas
ball_x = float(SCREEN_W - BALL_SIZE)
ball_y = float(BALL_SIZE)

ball_vx = -float(BALL_SPEED_X)
ball_vy = float(BALL_SPEED_Y)

# Platvorm liigub edasi-tagasi
pad_x = float((SCREEN_W - PAD_W) // 2)
pad_vx = float(PAD_SPEED)


def draw_ball():
    bx = int(ball_x - BALL_SIZE / 2)
    by = int(ball_y - BALL_SIZE / 2)

    if use_ball_img:
        screen.blit(ball_img, (bx, by))
    else:
        pygame.draw.circle(
            screen,
            (255, 165, 0),
            (int(ball_x), int(ball_y)),
            BALL_SIZE // 2
        )


def draw_pad():
    if use_pad_img:
        screen.blit(pad_img, (int(pad_x), PAD_Y))
    else:
        pygame.draw.rect(
            screen,
            (139, 90, 43),
            (int(pad_x), PAD_Y, PAD_W, PAD_H),
            border_radius=6
        )


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Pall liigub
    ball_x += ball_vx
    ball_y += ball_vy

    # Vasak sein
    if ball_x - BALL_SIZE / 2 <= 0:
        ball_x = BALL_SIZE / 2
        ball_vx *= -1

    # Parem sein
    if ball_x + BALL_SIZE / 2 >= SCREEN_W:
        ball_x = SCREEN_W - BALL_SIZE / 2
        ball_vx *= -1

    # Ülemine sein
    if ball_y - BALL_SIZE / 2 <= 0:
        ball_y = BALL_SIZE / 2
        ball_vy *= -1

    # Alumine sein
    if ball_y + BALL_SIZE / 2 >= SCREEN_H:
        ball_y = SCREEN_H - BALL_SIZE / 2
        ball_vy *= -1

    # Platvorm liigub, kuid pall EI põrka sellelt
    pad_x += pad_vx

    if pad_x <= 0:
        pad_x = 0
        pad_vx *= -1

    if pad_x + PAD_W >= SCREEN_W:
        pad_x = SCREEN_W - PAD_W
        pad_vx *= -1

    screen.fill(BG_COLOR)

    draw_pad()
    draw_ball()

    pygame.display.flip()
    clock.tick(FPS)