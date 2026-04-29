import pygame
import sys


def joonista_ruudustik(ekraan, ruudu_suurus=20, read=24, veerud=32, joone_varv=(255, 0, 0)):

    taustavärv = (144, 238, 144)  # heleroheline
    ekraan.fill(taustavärv)

    for rida in range(read + 1):
        y = rida * ruudu_suurus
        pygame.draw.line(ekraan, joone_varv, (0, y), (veerud * ruudu_suurus, y))

    for veerg in range(veerud + 1):
        x = veerg * ruudu_suurus
        pygame.draw.line(ekraan, joone_varv, (x, 0), (x, read * ruudu_suurus))


def main():
    pygame.init()
    ekraan = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Harjutamine")

    kell = pygame.time.Clock()

    while True:
        for sündmus in pygame.event.get():
            if sündmus.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if sündmus.type == pygame.KEYDOWN:
                if sündmus.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        joonista_ruudustik(
            ekraan,
            ruudu_suurus=20,
            read=24,
            veerud=32,
            joone_varv=(255, 0, 0)
        )

        pygame.display.flip()
        kell.tick(60)


if __name__ == "__main__":
    main()