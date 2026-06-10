import pygame
import time
import math
pygame.font.init()


def main():

    # pygame screen

    (screen_width, screen_height) = (900, 900)
    background_color = (0, 0, 0)
    pacman_image = pygame.image.load("pacman.png")
    pacman_image = pygame.transform.scale(pacman_image, (30, 30))

    red_image = pygame.image.load('red_ghost.png')
    red_image = pygame.transform.scale(red_image, (30, 30))

    blue_image = pygame.image.load('blue_ghost.png')
    blue_image = pygame.transform.scale(blue_image, (30, 30))

    orange_image = pygame.image.load('orange_ghost.png')
    orange_image = pygame.transform.scale(orange_image, (30, 30))

    pink_image = pygame.image.load('pink_ghost.png')
    pink_image = pygame.transform.scale(pink_image, (30, 30))

    background_image = pygame.image.load('pacman_map.jpeg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    pygame.display.set_caption("Pacman by CZ")
    screen = pygame.display.set_mode((screen_width, screen_height+50))
    screen.fill(background_color)
    screen.blit(background_image, (0,0))
    pygame.display.update()


    myfont = pygame.font.SysFont("monospace", 18)
    secondfont = pygame.font.SysFont("monospace", 30)




    grid = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
        [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
        [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0],
        [0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0],
        [0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,2,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,2,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,2,2,2,2,2,2,2,2,2,2,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
        [2,2,2,2,2,2,1,2,2,2,0,0,0,0,0,0,0,0,2,2,2,1,2,2,2,2,2,2,2,2,2],
        [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,2,2,2,2,2,2,2,2,2,2,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
        [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
        [0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0],
        [0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0],
        [0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0],
        [0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]

    stars_left = []

    # functions

    def x_crd(x):
        return (32 * x + 20)

    def y_crd(y):
        return (28.9 * y + 20)

    def update_screen():
        screen.fill(background_color)
        screen.blit(background_image, (0,0))
        draw_stars()

        for i in entities:
            i.display()

        pacman.display()

        label = myfont.render(f"Points: {pacman.points}" , 1, (255,255,255))
        screen.blit(label, (40, 915))

        pygame.display.update()


    def draw_stars():
        for i in stars_left:
            pygame.draw.circle(screen, (205, 205, 205), ((x_crd(i[0])), (y_crd(i[1]))), 5)

    def get_distance(a, b):
        d = math.sqrt((a[1]-b[1])*(a[1]-b[1])+(a[0]-b[0])*(a[0]-b[0]))
        return d

    def display_message(X):
        pygame.draw.rect(screen, (100, 100, 200), (300, 315, 300, 200))
        game_over_text = secondfont.render(f"You {X}!" , 1, (255,255,255))
        screen.blit(game_over_text, (385, 370))

        game_over_text1 = myfont.render(f"Press space to restart" , 1, (255,255,255))
        screen.blit(game_over_text1, (330, 420))
            
        pygame.display.update()



    def game_over():

        while True:
            for event in pygame.event.get():    
                if event.type == pygame.QUIT: 
                    quit()
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        main()

                    else:
                        print("Please press a valid Key")



    # Entity Class
    class entity():
        def __init__(self):
            self.next_x = [0,0]
            self.next_y = [0,0]
            self.moving = False

        def display(self):
            screen.blit(self.image, (x_crd(self.x) - 15, y_crd(self.y) - 15))


        def move(self):

            if self.x < -1:
                self.x = 28
            if self.x > 29:
                self.x = -1

            if self.moving == False:

                if grid[int(self.y) + self.next_y[1]][int(self.x) + self.next_x[1]] !=0:
                    self.next_x[0] = self.next_x[1]
                    self.next_y[0] = self.next_y[1]

                # Left or right
                if grid[int(self.y) + self.next_y[0]][int(self.x) + self.next_x[0]] !=0:
                    self.moving = True
                    self.count = 0


            if self.moving == True:


                self.x += self.next_x[0] / self.speed
                self.y += self.next_y[0] / self.speed

                self.x = round(self.x, 2)
                self.y = round(self.y, 2)

                self.count += 1

                if self.count == self.speed:
                    self.x = round(self.x)
                    self.y = round(self.y)
                    self.moving = False


    # pacman class
    class pacman(entity):
        def __init__(self, x, y):
            super().__init__()
            self.x = x
            self.y = y
            self.image = pacman_image
            self.speed = 8
            self.points = 0

        def eat(self):
            if (self.x, self.y) in stars_left:
                stars_left.remove((self.x, self.y))
                self.points += 10
            
            if not stars_left:
                display_message("Won")
                game_over()

    # Ghost class

    class ghost(entity):
        def __init__(self):
            super().__init__()
            self.target = [0,0]
            self.speed = 10

        def targeting(self):

            #pygame.display.update()

            # Detect closest spot to move towards target
            dist = 100

            self.next_y[1] = 0
            self.next_x[1] = 0

            # Left x=-1
            if get_distance((self.y, self.x-1), self.target) < dist and grid[int(self.y)][int(self.x-1)] !=0 and self.next_x[0] != 1:
                dist = get_distance((self.y, self.x-1), self.target)
                self.next_x[1] = -1
                self.next_y[1] = 0   

            # Right x=1
            if get_distance((self.y, self.x+1), self.target) < dist and grid[int(self.y)][int(self.x+1)] !=0 and self.next_x[0] != -1:
                dist = get_distance((self.y, self.x+1), self.target)
                self.next_x[1] = 1
                self.next_y[1] = 0  

            # Up y=1
            if get_distance((self.y+1, self.x), self.target) < dist and grid[int(self.y+1)][int(self.x)] !=0 and self.next_y[0] != -1:
                dist = get_distance((self.y+1, self.x), self.target)
                self.next_x[1] = 0
                self.next_y[1] = 1    

            # Down y=-1
            if get_distance((self.y-1, self.x), self.target) < dist and grid[int(self.y-1)][int(self.x)] !=0 and self.next_y[0] != 1:
                dist = get_distance((self.y-1, self.x), self.target)
                self.next_x[1] = 0
                self.next_y[1] = -1

            self.move()
            self.check_attack()

        def check_attack(self):
            if get_distance((self.x, self.y),(pacman.x, pacman.y)) < .6:
                display_message("Lost")
                game_over()

    # Blinky (Red)
    class Blinky(ghost):
        def __init__(self):
            super().__init__()
            self.image = red_image
            self.x, self.y = 1, 28
            self.color = (255,0,0)

        def target1(self):
            self.target = [pacman.y, pacman.x]
            self.targeting()

    # Pinky (Pink)
    class Pinky(ghost):
        def __init__(self):
            super().__init__()
            self.image = pink_image
            self.x, self.y = 1, 1
            self.color = (255,192,203)

        def target1(self):
            self.target = [pacman.y + (pacman.next_y[0]*4), pacman.x + (pacman.next_x[0]*4)]

            if pacman.next_y[0] == -1:
                self.target = [pacman.y + (pacman.next_y[0]*4), pacman.x -4]
            self.targeting()        

    # Inky (Cyan)
    class Inky(ghost):
        def __init__(self, blinky):
            super().__init__()
            self.image = blue_image
            self.x, self.y = 26, 26
            self.color = (0,70,100)
            self.blinky = blinky

        def target1(self):

            two_infront = [pacman.y + (pacman.next_y[0]*2), pacman.x + (pacman.next_x[0]*2)]

            vector = (two_infront[0] - self.blinky.y, two_infront[1] - self.blinky.x)

            self.target = [pacman.y + vector[0], pacman.x + vector[1]]

            self.targeting()             

    # Clyde (Orange)
    class Clyde(ghost):
        def __init__(self):
            super().__init__()
            self.image = orange_image
            self.x, self.y = 26, 1
            self.color = (255, 165,0)

        def target1(self):
            
            self.target = [pacman.y, pacman.x]
            
            if get_distance((self.x, self.y),(pacman.x, pacman.y)) < 8:
                self.target = (29, 1)

            self.targeting()     


    for index_y, y in enumerate(grid):
        for index_x, x in enumerate(y):
            if x == 1:
                pygame.draw.circle(screen, (205, 205, 205), ((x_crd(index_x)), (y_crd(index_y))), 5)
                pygame.display.update()

                stars_left.append((index_x,index_y))

    entities = []

    pacman = pacman(13, 17)
    pacman.display()

    ghost1 = Blinky()
    ghost1.display()
    entities.append(ghost1)

    ghost2 = Pinky()
    ghost2.display()
    entities.append(ghost2)

    ghost3 = Inky(ghost1)
    ghost3.display()
    entities.append(ghost3)

    ghost4 = Clyde()
    ghost4.display()
    entities.append(ghost4)

    running = True
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():    
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == pygame.KEYDOWN:

                pacman.next_y[1] = 0
                pacman.next_x[1] = 0
                
                if event.key == pygame.K_r:
                    pacman.display()
                elif event.key == pygame.K_a:
                    pacman.next_x[1] = -1
                elif event.key == pygame.K_d:
                    pacman.next_x[1] = 1
                elif event.key == pygame.K_w:
                    pacman.next_y[1] = -1
                elif event.key == pygame.K_s:
                    pacman.next_y[1] = 1
        
        pacman.move()
        for i in entities:
            i.target1()
        
        pacman.eat()
        update_screen()
        clock.tick(60)

        
if __name__ == "__main__":
    main()