import pygame
triangle = [(150, 94), (150, 100), (163, 97)]
pygame.init()
pygame.display.set_caption("Lumememm - Kevin Kõrgmaa")
screen = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 255, 255), (150, 220), 55)
    pygame.draw.circle(screen, (255, 255, 255), (150, 150), 40)
    pygame.draw.circle(screen, (255, 255, 255), (150, 90), 25)
    pygame.draw.rect(screen, (0, 0, 0), (156, 85, 5, 5))
    pygame.draw.rect(screen, (0, 0, 0), (140, 85, 5, 5))
    pygame.draw.polygon(screen, (255, 0, 0), triangle)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
