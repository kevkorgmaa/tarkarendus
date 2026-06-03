import pygame, sys, random
pygame.init()

# värvid
red = [255, 0, 0]
lBlue = [153, 204, 255]

# ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Mäng")
clock = pygame.time.Clock()

# pall
ball_img = pygame.image.load("C:\\Users\\kevin.korgmaa\\PycharmProjects\\tarkarendus\\animeerimine\\ball.png")
ball_img = pygame.transform.scale(ball_img, [40, 40])  # väiksem pall
ball_w = ball_img.get_rect().width
ball_h = ball_img.get_rect().height

ballX = 0.0
ballY = 0.0
speedX = 3.0
speedY = 4.0

# langevad ruudud: [x, y, kiirus]
coords = []
for i in range(10):
    coords.append([
        random.randint(0, screenX - 20),
        random.randint(0, screenY),
        random.randint(1, 5)
    ])

gameover = False
while not gameover:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(lBlue)

    # pall liigub
    ballX += speedX
    ballY += speedY

    # põrkamine float-täpsusega, glitch parandatud
    if speedX > 0 and ballX >= screenX - ball_w:
        ballX = screenX - ball_w
        speedX = -speedX
    elif speedX < 0 and ballX <= 0:
        ballX = 0
        speedX = -speedX

    if speedY > 0 and ballY >= screenY - ball_h:
        ballY = screenY - ball_h
        speedY = -speedY
    elif speedY < 0 and ballY <= 0:
        ballY = 0
        speedY = -speedY

    screen.blit(ball_img, (int(ballX), int(ballY)))

    # langevad ruudud
    for i in range(len(coords)):
        pygame.draw.rect(screen, red, [coords[i][0], coords[i][1], 20, 20])
        coords[i][1] += coords[i][2]
        if coords[i][1] > screenY:
            coords[i][1] = random.randint(-40, -10)
            coords[i][0] = random.randint(0, screenX - 20)

    pygame.display.flip()

pygame.quit()