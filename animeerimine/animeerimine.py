import pygame, sys

pygame.init()

# värvid
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
pink = [255, 153, 255]
lGreen = [153, 255, 153]
lBlue = [153, 204, 255]

# ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Animeerimine")
screen.fill(lBlue)

# graafika laadimine
ball = pygame.image.load("ball.png")

width = ball.get_width()
height = ball.get_height()

scale_factor = 0.3  # 30% suurusest
ball = pygame.transform.scale(ball, (int(width * scale_factor), int(height * scale_factor)))


# kiirus ja asukoht
posX, posY = 0, 0

gameover = False
while not gameover:
    # mängu sulgemine ristist
    events = pygame.event.get()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    # pildi lisamine ekraanile
    screen.blit(ball, (posX, posY))

    # graafika kuvamine ekraanil
    pygame.display.flip()

pygame.quit()