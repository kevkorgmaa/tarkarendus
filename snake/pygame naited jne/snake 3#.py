import pygame
import random

W = 30
H = 30
S = 20

# pygame setup
pygame.init()
screen = pygame.display.set_mode((W * S, H * S))
clock = pygame.time.Clock()
running = True

# game setup
snake = [pygame.Vector2(W / 2, H / 2)]
vel = pygame.Vector2(1, 0)

key_vel = {
    pygame.K_RIGHT: pygame.Vector2(1, 0),
    pygame.K_DOWN: pygame.Vector2(0, 1),
    pygame.K_LEFT: pygame.Vector2(-1, 0),
    pygame.K_UP: pygame.Vector2(0, -1)
}

grow = 3

def place_food():
    global food_pos
    food_pos = pygame.Vector2(
        random.randrange(W),
        random.randrange(H)
    )
    while food_pos in snake:
        food_pos = pygame.Vector2(
            random.randrange(W),
            random.randrange(H)
        )

place_food()

while running:
    # poll for events
    vels = []
    for event in pygame.event.get():
        # pygame.QUIT = user closed window
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN and event.key in key_vel:
            vels += [key_vel[event.key]]

    for vel in vels or [vel]:
        # fill buffer with white
        screen.fill("white")

        new_head = snake[-1] + vel

        if new_head.x < 0:
            new_head.x = W - 1
        if new_head.x >= W:
            new_head.x = 0

        if new_head.y < 0:
            new_head.y = H - 1
        if new_head.y >= H:
            new_head.y = 0

        if new_head in snake:
            print("hit self")
            running = False
            break

        if new_head == food_pos:
            grow += 1
            place_food()

        snake.append(new_head)

        if grow > 0:
            grow -= 1
        else:
            snake.pop(0)

        for dot in snake:
            square = pygame.Rect(dot * S, (S, S))
            screen.fill("black", square)

        square = pygame.Rect(food_pos * S, (S, S))
        screen.fill("green", square)

        # copy buffer to screen
        pygame.display.flip()

        # limits FPS
        clock.tick(20)

pygame.quit()