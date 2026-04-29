import pygame
import sys
import os
import math

pygame.init()

LAIUS = 640
KORGUS = 480
aken = pygame.display.set_mode((LAIUS, KORGUS))
pygame.display.set_caption("Harjutamine")

VALGE = (255, 255, 255)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Taust
taust = pygame.image.load(os.path.join("C:\\Users\\kevin.korgmaa\\PycharmProjects\\tarkarendus\\Pildi ja tekstiga tegelemine\\bg_shop.jpg")).convert()
taust = pygame.transform.scale(taust, (LAIUS, KORGUS))

# Müüja
muuja = pygame.image.load(os.path.join("C:\\Users\\kevin.korgmaa\\PycharmProjects\\tarkarendus\\Pildi ja tekstiga tegelemine\\seller.png")).convert_alpha()
muuja_laius = 260
muuja_korgus = int(muuja_laius * muuja.get_height() / muuja.get_width())
muuja = pygame.transform.scale(muuja, (muuja_laius, muuja_korgus))

# Jutumull
jutumull = pygame.image.load(os.path.join("C:\\Users\\kevin.korgmaa\\PycharmProjects\\tarkarendus\\Pildi ja tekstiga tegelemine\\chat.png")).convert_alpha()
jm_laius = 255
jm_korgus = int(jm_laius * jutumull.get_height() / jutumull.get_width())
jutumull = pygame.transform.scale(jutumull, (jm_laius, jm_korgus))

font = pygame.font.SysFont("Georgia", 20)
nimi = "Kevin"

# Logo
vikk_raw = pygame.image.load(os.path.join("C:\\Users\\kevin.korgmaa\\PycharmProjects\\tarkarendus\\Pildi ja tekstiga tegelemine LISA\\VIKK_LOGO.jpg")).convert_alpha()
vikk_w = 560
vikk_h = int(vikk_raw.get_height() * (vikk_w / vikk_raw.get_width()))
vikk_logo = pygame.transform.scale(vikk_raw, (vikk_w, vikk_h))

logo_x = 10
logo_y = 10

# Tort
tort = pygame.image.load(os.path.join("C:\\Users\\kevin.korgmaa\\PycharmProjects\\tarkarendus\\Pildi ja tekstiga tegelemine LISA\\tort_rgba.png")).convert_alpha()
tort_laius = 80
tort_korgus = int(tort_laius * tort.get_height() / tort.get_width())
tort = pygame.transform.scale(tort, (tort_laius, tort_korgus))

tort_x = 330
tort_y = KORGUS - tort_korgus - 180

# Mõõk
moook = pygame.image.load(os.path.join("C:\\Users\\kevin.korgmaa\\PycharmProjects\\tarkarendus\\Pildi ja tekstiga tegelemine LISA\\moook.png")).convert_alpha()
moook_laius = 110
moook_korgus = int(moook_laius * moook.get_height() / moook.get_width())
moook = pygame.transform.scale(moook, (moook_laius, moook_korgus))
moook = pygame.transform.rotate(moook, 130)

moook_x = LAIUS - moook_laius - 12
moook_y = 80

# Mängutsükkel
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

    tekst = font.render(f"Tere, olen {nimi}", True, VALGE)
    tekst_x = jm_x + (jm_laius - tekst.get_width()) // 2 - 10
    tekst_y = jm_y + (jm_korgus - tekst.get_height()) // 2 - 15
    aken.blit(tekst, (tekst_x, tekst_y))

    # Logo
    aken.blit(vikk_logo, (logo_x, logo_y))

    # Tort
    aken.blit(tort, (tort_x, tort_y))

    # Mõõk
    aken.blit(moook, (moook_x, moook_y))

    pygame.display.flip()
    kell.tick(60)