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

    # --- FOOR (vähendatud versioon) ---

    # Kast (väiksem)
    pygame.draw.rect(screen, (120, 120, 120), (147, 230, 6, 40))

    # Tuled (raadius väiksem)
    pygame.draw.circle(screen, (255, 0, 0), (150, 80), 25)
    pygame.draw.circle(screen, (255, 255, 0), (150, 140), 25)
    pygame.draw.circle(screen, (0, 255, 0), (150, 200), 25)

    # Post (lühem ja peenem)
    pygame.draw.rect(screen, (120, 120, 120), (147, 230, 6, 40))

    # Postialus (45° nurgad, väiksem)
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
pygame.quit()