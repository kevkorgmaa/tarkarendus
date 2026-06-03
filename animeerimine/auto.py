import pygame
import sys
import random
import os

pygame.init()  # käivitab pygame'i

# akna mõõdud
W, H = 640, 480
screen = pygame.display.set_mode((W, H))  # loob akna
pygame.display.set_caption("Rally Mäng")  # akna pealkiri

clock = pygame.time.Clock()  # FPS kontroll
font_big = pygame.font.SysFont("monospace", 28, bold=True)  # suur font
font_small = pygame.font.SysFont("monospace", 15)  # väike font

# leiab faili kausta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# taustapildi laadimine
bg_img = pygame.image.load(os.path.join(BASE_DIR, "bg_rally.jpg")).convert()
bg_img = pygame.transform.scale(bg_img, (W, H))  # sobitab ekraanile

# autode pildid
red_img_raw = pygame.image.load(os.path.join(BASE_DIR, "f1_red.png")).convert_alpha()
blue_img_raw = pygame.image.load(os.path.join(BASE_DIR, "f1_blue.png")).convert_alpha()

# auto suurus
CAR_W, CAR_H = 45, 90

# muudab pildid väiksemaks
red_img = pygame.transform.scale(red_img_raw, (CAR_W, CAR_H))
blue_img = pygame.transform.scale(blue_img_raw, (CAR_W, CAR_H))

# 3 raja keskpunktid vastavalt taustapildile
# tee: x=148 kuni x=492, kriipsud x=248 ja x=384 juures
LANES = [198, 316, 438]

blue_img = pygame.transform.rotate(blue_img, 180)
red_img  = pygame.transform.rotate(red_img, 180)

# vastaste auto klass
class BlueCar:
    def __init__(self, lane_idx, start_y):
        self.lane = lane_idx          # millises reas
        self.x = LANES[lane_idx]      # x määratakse üks kord, ei muutu
        self.y = float(start_y)       # y asukoht
        self.speed = random.uniform(2.0, 4.0)  # suvaline kiirus

    def update(self):
        self.y += self.speed  # liigub alla

        # kui jõuab ekraanist välja — tagasi üles, SAMA raja peal
        if self.y > H + CAR_H:
            self.y = float(random.randint(-150, -CAR_H))
            self.speed = random.uniform(2.0, 4.0)
            return True  # annab märku skooriks
        return False

    def draw(self, surf):
        rect = blue_img.get_rect(center=(self.x, int(self.y)))
        surf.blit(blue_img, rect)


# skoori kuvamine
def draw_score(surf, score):
    text = font_big.render("Skoor: " + str(score), True, (255, 255, 255))

    # poolläbipaistev taust
    bg = pygame.Surface((text.get_width() + 22, 42), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 170))

    surf.blit(bg, (8, 8))
    surf.blit(text, (19, 13))


# põhimäng
def main():
    score = 0  # algskoor

    # mängija auto algasukoht — keskmises rajas
    red_x = LANES[1]
    red_y = H - CAR_H // 2 - 10

    # üks auto igale rajale
    blue_cars = []
    for i in range(3):
        start_y = -CAR_H - i * 150
        blue_cars.append(BlueCar(i, start_y))

    running = True
    while running:
        clock.tick(60)  # 60 FPS

        # sündmused
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # taust
        screen.blit(bg_img, (0, 0))

        # vastaste autod
        for car in blue_cars:
            reached_bottom = car.update()
            if reached_bottom:
                score += 10  # lisa punkte
            car.draw(screen)

        # mängija auto
        red_rect = red_img.get_rect(center=(red_x, red_y))
        screen.blit(red_img, red_rect)

        # skoor
        draw_score(screen, score)

        # väike tekst alla
        hint = font_small.render("ESC - välju", True, (220, 220, 220))
        screen.blit(hint, (W - hint.get_width() - 10, H - 22))

        pygame.display.flip()  # uuendab ekraani

    pygame.quit()
    sys.exit()


# käivitab mängu
if __name__ == "__main__":
    main()