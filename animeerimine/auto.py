import pygame
import sys
import random
import os

pygame.init()

W, H = 640, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Rally Mäng")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("monospace", 28, bold=True)
font_small = pygame.font.SysFont("monospace", 15)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bg_img = pygame.image.load(os.path.join(BASE_DIR, "bg_rally.jpg")).convert()
bg_img = pygame.transform.scale(bg_img, (W, H))

red_img_raw = pygame.image.load(os.path.join(BASE_DIR, "f1_red.png")).convert_alpha()
blue_img_raw = pygame.image.load(os.path.join(BASE_DIR, "f1_blue.png")).convert_alpha()

CAR_W, CAR_H = 45, 90

red_img = pygame.transform.scale(red_img_raw, (CAR_W, CAR_H))
blue_img = pygame.transform.scale(blue_img_raw, (CAR_W, CAR_H))

blue_img = pygame.transform.rotate(blue_img, 180)
red_img  = pygame.transform.rotate(red_img, 180)

LANES = [198, 316, 438]


class BlueCar:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.x = LANES[self.lane]
        self.y = float(-CAR_H)
        self.speed = random.uniform(2.5, 4.0)

    def update(self):
        self.y += self.speed

    def done(self):
        return self.y > H + CAR_H

    def draw(self, surf):
        rect = blue_img.get_rect(center=(self.x, int(self.y)))
        surf.blit(blue_img, rect)


def draw_score(surf, score):
    text = font_big.render("Skoor: " + str(score), True, (255, 255, 255))
    bg = pygame.Surface((text.get_width() + 22, 42), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 170))
    surf.blit(bg, (8, 8))
    surf.blit(text, (19, 13))


def main():
    score = 0
    red_x = LANES[1]
    red_y = H - CAR_H // 2 - 10

    cars = []

    # Järgmine spawn: auto tekib alles kui eelmine on jõudnud piisavalt alla
    # (mõõdetud eelmise auto y järgi, mitte timeriga)
    spawn_threshold = H // 3  # uus auto tekib kui eelmine on ekraani ülemises kolmandikus

    # Esimene auto kohe
    cars.append(BlueCar())

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.blit(bg_img, (0, 0))

        # Uuenda autosid
        for car in cars:
            car.update()

        # Eemalda ekraanist väljunud autod
        before = len(cars)
        cars = [c for c in cars if not c.done()]
        score += (before - len(cars)) * 10

        # Spawni uus auto kui viimane on jõudnud piisavalt alla
        # ja ekraanil on vähem kui 2 autot
        if len(cars) < 2:
            # Viimane auto — kontrolli kas see on piisavalt all
            last_y = max((c.y for c in cars), default=-CAR_H)
            if last_y > spawn_threshold:
                cars.append(BlueCar())
                # Järgmise spawni lävi on jälle pool ekraani
                spawn_threshold = H // 3 + random.randint(-40, 40)

        # Joonista
        for car in cars:
            car.draw(screen)

        red_rect = red_img.get_rect(center=(red_x, red_y))
        screen.blit(red_img, red_rect)

        draw_score(screen, score)

        hint = font_small.render("ESC - välju", True, (220, 220, 220))
        screen.blit(hint, (W - hint.get_width() - 10, H - 22))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()