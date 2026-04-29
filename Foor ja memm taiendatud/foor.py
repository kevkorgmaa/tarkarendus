import pygame
pygame.init()
pygame.display.set_caption("foor - Kevin Kõrgmaa")
screen = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # --- FOOR ---

    # Tulede ümber ristkülik (hall kast)
    pygame.draw.rect(screen, (80, 80, 80), (120, 50, 60, 175), border_radius=8)

    # Tuled
    pygame.draw.circle(screen, (255, 0, 0),   (150, 85),  22)
    pygame.draw.circle(screen, (255, 255, 0), (150, 140), 22)
    pygame.draw.circle(screen, (0, 255, 0),   (150, 195), 22)

    # Post
    pygame.draw.rect(screen, (120, 120, 120), (147, 225, 6, 40))

    # Postialus
    alus = [(135, 270), (150, 240), (165, 270)]
    pygame.draw.polygon(screen, (200, 200, 200), alus)

    # Eesti lipu värvid sees
    sinine = [(138, 268), (150, 244), (162, 268)]
    pygame.draw.polygon(screen, (0, 102, 204), sinine)

    must = [(140, 266), (150, 248), (160, 266)]
    pygame.draw.polygon(screen, (0, 0, 0), must)

    valge = [(142, 263), (150, 252), (158, 263)]
    pygame.draw.polygon(screen, (255, 255, 255), valge)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()