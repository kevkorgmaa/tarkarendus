import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hiir")

BG_COLOR = (173, 216, 230)
MAX_RINGS = 10       # pärast seda arvu läheb hard cap kehtima
MAX_RADIUS = 80      # hard cap — ükski ring ei lähe sellest suuremaks
BASE_RADIUS = 10
GROW_AMOUNT = 5

rings = []  # [x, y, radius, color]


def random_color():
    return (random.randint(30, 220), random.randint(30, 220), random.randint(30, 220))


def next_radius():
    """Iga uus ring on eelmisest GROW_AMOUNT võrra suurem."""
    if not rings:
        return BASE_RADIUS
    new_r = rings[-1][2] + GROW_AMOUNT
    # Hard cap pärast MAX_RINGS ringi
    if len(rings) >= MAX_RINGS:
        new_r = min(new_r, MAX_RADIUS)
    return new_r


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            rings.append([x, y, next_radius(), random_color()])

            if len(rings) > MAX_RINGS:
                rings.pop(0)

    screen.fill(BG_COLOR)

    for ring in rings:
        pygame.draw.circle(screen, ring[3], (ring[0], ring[1]), ring[2], 2)

    pygame.display.flip()
    clock.tick(60)