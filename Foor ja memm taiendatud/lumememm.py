import pygame
import math
kolmnurk = [(150, 94), (150, 100), (163, 97)]
harjaPunktid = [
    (280, 255),
    (300, 245),
    (305, 260),
    (310, 275),
    (290, 285),
    (275, 275)
]
pygame.init()
pygame.display.set_caption("Lumememm - Kevin Kõrgmaa")
screen = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((173, 216, 230))
    # Keha
    pygame.draw.circle(screen, (255, 255, 255), (150, 220), 55)
    pygame.draw.circle(screen, (255, 255, 255), (150, 150), 40)
    pygame.draw.circle(screen, (255, 255, 255), (150, 90), 25)
    # Silmad
    pygame.draw.rect(screen, (0, 0, 0), (156, 85, 5, 5))
    pygame.draw.rect(screen, (0, 0, 0), (140, 85, 5, 5))
    # Nina
    pygame.draw.polygon(screen, (255, 165, 0), kolmnurk)
    # Käed
    pygame.draw.line(screen, (165, 42, 42), (188, 135), (210, 180), 5) #P
    pygame.draw.line(screen, (165, 42, 42), (112, 135), (90, 180), 5) #V
    # Nööbid
    pygame.draw.circle(screen, (0, 0, 0), (150, 220), 5)
    pygame.draw.circle(screen, (0, 0, 0), (150, 180), 5)
    pygame.draw.circle(screen, (0, 0, 0), (150, 140), 5)
    # Müts
    pygame.draw.ellipse(screen, (200, 0, 0), (125, 50, 50, 30))
    pygame.draw.rect(screen, (125, 125, 125), (125, 65, 50, 15))
    pygame.draw.circle(screen, (255, 255, 255), (150, 50), 6)
    # Hari
    pygame.draw.line(screen, (139, 69, 19), (210, 190), (210, 230), 7)
    pygame.draw.line(screen, (139, 69, 19), (210, 130), (210, 190), 7)
    for i in range(8):
        offset = i * 4 - 10
        pygame.draw.line(screen, (185, 135, 75),
                         (210 + offset, 230),
                         (200 + offset * 0.9, 235), 3)
    # Pilved
    pygame.draw.circle(screen, (255, 255, 255), (60, 50), 20)
    pygame.draw.circle(screen, (255, 255, 255), (80, 45), 25)
    pygame.draw.circle(screen, (255, 255, 255), (100, 50), 20)


    pygame.draw.circle(screen, (255, 255, 255), (220, 60), 22)
    pygame.draw.circle(screen, (255, 255, 255), (240, 55), 27)
    pygame.draw.circle(screen, (255, 255, 255), (260, 60), 22)


    pygame.draw.circle(screen, (255, 255, 255), (150, 30), 18)
    pygame.draw.circle(screen, (255, 255, 255), (165, 25), 22)
    pygame.draw.circle(screen, (255, 255, 255), (180, 30), 18)


    # Paike
    pygame.draw.circle(screen, (255, 255, 0), (300, 0), 40)
    pygame.draw.line(screen, (255, 255, 0), (250, 0), (205, 0), 3)
    pygame.draw.line(screen, (255, 255, 0), (265, 35), (232, 65), 3)
    pygame.draw.line(screen, (255, 255, 0), (300, 50), (300, 95), 3)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
