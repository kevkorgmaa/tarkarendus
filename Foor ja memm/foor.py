import pygame
import sys

pygame.init()

# Aken
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Foor – Kevin Kõrgmaa")

# Värvid
BLACK = (0, 0, 0)
WHITE = (180, 180, 180)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Taust
screen.fill(BLACK)

# Foori korpus
pygame.draw.rect(screen, WHITE, (110, 20, 80, 260), 2)

# Tuled
pygame.draw.circle(screen, RED, (150, 70), 35)
pygame.draw.circle(screen, YELLOW, (150, 150), 35)
pygame.draw.circle(screen, GREEN, (150, 230), 35)

pygame.display.flip()

# Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()