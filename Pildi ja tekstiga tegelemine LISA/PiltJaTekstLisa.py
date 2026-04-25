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

# ── Taustapilt ──────────────────────────────────────────────────────────────
taust = pygame.image.load(os.path.join(
    "C:\\Users\\admin\\Desktop\\progemine\\tarkarendus\\Pildi ja tekstiga tegelemine\\bg_shop.jpg"
)).convert()
taust = pygame.transform.scale(taust, (LAIUS, KORGUS))

# ── Müüja ───────────────────────────────────────────────────────────────────
muuja = pygame.image.load(os.path.join(
    "C:\\Users\\admin\\Desktop\\progemine\\tarkarendus\\Pildi ja tekstiga tegelemine\\seller.png"
)).convert_alpha()
muuja_laius = 260
muuja_korgus = int(muuja_laius * muuja.get_height() / muuja.get_width())
muuja = pygame.transform.scale(muuja, (muuja_laius, muuja_korgus))

# ── Jutumull ─────────────────────────────────────────────────────────────────
jutumull = pygame.image.load(os.path.join(
    "C:\\Users\\admin\\Desktop\\progemine\\tarkarendus\\Pildi ja tekstiga tegelemine\\chat.png"
)).convert_alpha()
jm_laius = 255
jm_korgus = int(jm_laius * jutumull.get_height() / jutumull.get_width())
jutumull = pygame.transform.scale(jutumull, (jm_laius, jm_korgus))

font = pygame.font.SysFont("Georgia", 20, bold=False)
nimi = "Kevin"

# ── 1. VIKK100 logo (vasak ülanurk) ─────────────────────────────────────────
PILT_DIR = os.path.dirname(os.path.abspath(__file__))

logo = pygame.image.load(os.path.join(PILT_DIR, "VIKK_logo.png")).convert_alpha()
logo_laius = 160
logo_korgus = int(logo_laius * logo.get_height() / logo.get_width())
logo = pygame.transform.scale(logo, (logo_laius, logo_korgus))
logo_x = 8
logo_y = 8

# ── 1.1. Kaarega tekst "TULEVIK 2050" ───────────────────────────────────────
kaare_font = pygame.font.SysFont("Georgia", 13, bold=True)
KAARE_TEKST = "TULEVIK 2050"
KAAR_VARV = (10, 60, 120)

kaare_cx = logo_x + logo_laius // 2
kaare_cy = logo_y + logo_korgus + 28
kaare_r  = 38
kaare_algus = 180                                        # alguspunkt kraadides
kaare_samm  = -160 / max(len(KAARE_TEKST) - 1, 1)      # negatiivne = vasakult paremale

def joonista_kaar_tekst(surface, tekst, font, color, cx, cy, radius, nurk_algus, nurk_samm):
    for i, taht in enumerate(tekst):
        nurk = nurk_algus + i * nurk_samm
        rad = math.radians(nurk)

        # Tähe asukoht kaarel
        tx = cx + radius * math.cos(rad)
        ty = cy + radius * math.sin(rad)

        # Joonista täht
        pind = font.render(taht, True, color)

        # Pööra täht kaare tangendiga kohakuti
        # pygame Y on alla = lahutame 90 (mitte ei liida)
        rot = nurk - 90
        pooratud = pygame.transform.rotate(pind, -rot)

        rect = pooratud.get_rect(center=(int(tx), int(ty)))
        surface.blit(pooratud, rect)
#2. Tort (laua peal)
tort = pygame.image.load(os.path.join(PILT_DIR, "tort_rgba.png")).convert_alpha()
tort_laius = 80
tort_korgus = int(tort_laius * tort.get_height() / tort.get_width())
tort = pygame.transform.scale(tort, (tort_laius, tort_korgus))
# Laud asub ekraani all-keskel; paiguta tort laua peale
tort_x = 330
tort_y = KORGUS - tort_korgus - 180     # 60px põhjast = laua pinna kõrgus

#3. Mõõk (seinal, paremal)
moook = pygame.image.load(os.path.join(PILT_DIR, "moook.png")).convert_alpha()
moook_laius = 110
moook_korgus = int(moook_laius * moook.get_height() / moook.get_width())
moook = pygame.transform.scale(moook, (moook_laius, moook_korgus))
moook = pygame.transform.rotate(moook, 130)
moook_x = LAIUS - moook_laius - 12
moook_y = 80                            # seinale, kõrgel

#Mängutsükkel
kell = pygame.time.Clock()

while True:
    for syndmus in pygame.event.get():
        if syndmus.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    aken.blit(taust, (0, 0))

    # Müüja (muutmata)
    muuja_x = 104
    muuja_y = KORGUS - muuja_korgus - 16
    aken.blit(muuja, (muuja_x, muuja_y))

    # Jutumull (muutmata)
    jm_x = 245
    jm_y = 66
    aken.blit(jutumull, (jm_x, jm_y))

    # Tekst jutumulli sisse (muutmata)
    tekst = font.render(f"Tere, olen {nimi}", True, VALGE)
    tekst_x = jm_x + (jm_laius - tekst.get_width()) // 2 - 10
    tekst_y = jm_y + (jm_korgus - tekst.get_height()) // 2 - 15
    aken.blit(tekst, (tekst_x, tekst_y))

    # 1. Logo (vasak ülanurk)
    aken.blit(logo, (logo_x, logo_y))

    # 1.1. Kaarega tekst "TULEVIK 2050"
    joonista_kaar_tekst(aken, KAARE_TEKST, kaare_font, KAAR_VARV,
                        kaare_cx, kaare_cy, kaare_r, kaare_algus, kaare_samm)

    # 2. Tort laua peal
    aken.blit(tort, (tort_x, tort_y))

    # 3. Mõõk seinal
    aken.blit(moook, (moook_x, moook_y))

    pygame.display.flip()
    kell.tick(60)