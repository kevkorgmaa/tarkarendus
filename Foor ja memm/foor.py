import pygame

pygame.init()
pygame.display.set_caption("Eesti foor - Kevin Kõrgmaa")
screen = pygame.display.set_mode((300, 380))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    #Postialus
    # Hall väline kolmnurk
    pygame.draw.polygon(screen, (70, 70, 75),[(65, 345), (235, 345), (150, 275)])
    # Eesti lipp
    # Horisontaalsed triibud ülevalt alla (sinine - must - valge)
    # Sinine (ülemine osa)
    pygame.draw.polygon(screen, (0, 114, 206), [
        (80, 295),
        (220, 295),
        (150, 278)
    ])
    # Must (keskmine osa)
    pygame.draw.polygon(screen, (0, 0, 0), [
        (76, 318),
        (224, 318),
        (150, 295)
    ])
    # Valge (alumine osa - kõige laiem)
    pygame.draw.polygon(screen, (255, 255, 255), [
        (70, 342),
        (230, 342),
        (150, 315)
    ])
    # Post
    # Kitsas post
    pygame.draw.rect(screen, (45, 45, 50), (142, 135, 16, 145))

    # Väike ühendus foorikasti ja posti vahel
    pygame.draw.rect(screen, (45, 45, 50), (138, 130, 24, 10))

    # Foori kast
    # Tumeda halli kast
    pygame.draw.rect(screen, (28, 28, 33), (102, 45, 96, 195), border_radius=18)

    # Tulede mustad raamid
    for y in [57, 117, 177]:
        pygame.draw.rect(screen, (18, 18, 22), (113, y, 74, 48), border_radius=10)

    # Tuled
    pygame.draw.circle(screen, (255, 40, 40), (150, 81), 19)   # punane
    pygame.draw.circle(screen, (255, 215, 0), (150, 141), 19)  # kollane
    pygame.draw.circle(screen, (0, 205, 55), (150, 201), 19)   # roheline

    # Tulede õhukesed ääred
    for y in [81, 141, 201]:
        pygame.draw.circle(screen, (50, 50, 55), (150, y), 19, 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()