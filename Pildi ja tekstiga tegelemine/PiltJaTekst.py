import pygame
import sys
import os

pygame.init()

LAIUS = 640
KORGUS = 480
aken = pygame.display.set_mode((LAIUS, KORGUS))
pygame.display.set_caption("Harjutamine")

VALGE = (255, 255, 255)
taust = pygame.image.load(os.path.join("C:\\Users\\kevin.korgmaa\\PycharmProjects\\tarkarendus\\Pildi ja tekstiga tegelemine\\bg_shop.jpg")).convert()
taust = pygame.transform.scale(taust, (LAIUS, KORGUS))

# Müüjar
muuja = pygame.image.load(os.path.join("C:\\Users\\kevin.korgmaa\\PycharmProjects\\tarkarendus\\Pildi ja tekstiga tegelemine\\seller.png")).convert_alpha()
muuja_laius = 260
muuja_korgus = int(muuja_laius * muuja.get_height() / muuja.get_width())
muuja = pygame.transform.scale(muuja, (muuja_laius, muuja_korgus))

# Jutumull
jutumull = pygame.image.load(os.path.join("C:\\Users\\kevin.korgmaa\\PycharmProjects\\tarkarendus\\Pildi ja tekstiga tegelemine\\chat.png")).convert_alpha()
jm_laius = 255
jm_korgus = int(jm_laius * jutumull.get_height() / jutumull.get_width())
jutumull = pygame.transform.scale(jutumull, (jm_laius, jm_korgus))

font = pygame.font.SysFont("Georgia", 20, bold=False)

nimi = "Kevin"

kell = pygame.time.Clock()

while True:
    for syndmus in pygame.event.get():
        if syndmus.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    aken.blit(taust, (0, 0))

    # Müüja
    muuja_x = 104
    muuja_y = KORGUS - muuja_korgus - 16
    aken.blit(muuja, (muuja_x, muuja_y))

    # Jutumull
    jm_x = 245
    jm_y = 66
    aken.blit(jutumull, (jm_x, jm_y))

    # Tekst jutumulli sisse
    tekst = font.render(f"Tere, olen {nimi}", True, VALGE)
    tekst_x = jm_x + (jm_laius - tekst.get_width()) // 2 - 10
    tekst_y = jm_y + (jm_korgus - tekst.get_height()) // 2 - 15
    aken.blit(tekst, (tekst_x, tekst_y))

    pygame.display.flip()
    kell.tick(60)