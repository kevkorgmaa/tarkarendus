import pygame
import time
import math

# Initialize pygame fonts
pygame.font.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900
EXTRA_HEIGHT = 50  # Additional space for UI elements
BACKGROUND_COLOR = (0, 0, 0)
STAR_COLOR = (205, 205, 205)
FPS = 60

# Asset paths
PACMAN_IMG_PATH = "images/pacman.png"
RED_GHOST_IMG_PATH = "images/red_ghost.png"
BLUE_GHOST_IMG_PATH = "images/blue_ghost.png"
ORANGE_GHOST_IMG_PATH = "images/orange_ghost.png"
PINK_GHOST_IMG_PATH = "images/pink_ghost.png"
MAP_IMG_PATH = "images/pacman_map.jpeg"

# Load and scale images
def load_image(path, size=(30, 30)):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

PACMAN_IMAGE = load_image(PACMAN_IMG_PATH)
RED_IMAGE = load_image(RED_GHOST_IMG_PATH)
BLUE_IMAGE = load_image(BLUE_GHOST_IMG_PATH)
ORANGE_IMAGE = load_image(ORANGE_GHOST_IMG_PATH)
PINK_IMAGE = load_image(PINK_GHOST_IMG_PATH)
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(MAP_IMG_PATH), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Setup fonts
SMALL_FONT = pygame.font.SysFont("monospace", 18)
LARGE_FONT = pygame.font.SysFont("monospace", 30)

# Grid for map boundaries (1: star, 0: wall, 2: power-up or other special tile)
GRID = [
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


# Utility Functions
def x_coord(grid_x: int) -> int:
    """Calculate the x coordinate for the grid position."""
    return 32 * grid_x + 20


def y_coord(grid_y: int) -> int:
    """Calculate the y coordinate for the grid position."""
    return int(28.9 * grid_y + 20)


def get_distance(a: tuple, b: tuple) -> float:
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def display_message(screen, message: str):
    """Show a message on the screen and wait for space key to restart."""
    overlay_rect = pygame.Rect(300, 315, 300, 200)
    pygame.draw.rect(screen, (100, 100, 200), overlay_rect)
    text_surface = LARGE_FONT.render(f"You {message}!", True, (255, 255, 255))
    screen.blit(text_surface, (385, 370))
    restart_text = SMALL_FONT.render("Press space to restart", True, (255, 255, 255))
    screen.blit(restart_text, (330, 420))
    pygame.display.update()


# Classes
class Entity:
    def __init__(self, x, y, image, speed: int = 8):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.moving = False
        # next direction: [current set, upcoming new command] - used to update changing directions fluidly
        self.next_dir = {'current': (0, 0), 'queued': (0, 0)}
        self.move_count = 0

    def display(self, screen):
        screen.blit(self.image, (x_coord(self.x) - 15, y_coord(self.y) - 15))

    def move(self, grid):
        # Wrap around logic
        if self.x < -1:
            self.x = 28
        if self.x > 29:
            self.x = -1

        if not self.moving:
            # Only update current direction if next queued is valid in grid
            next_queue = self.next_dir['queued']
            if grid[int(self.y) + next_queue[1]][int(self.x) + next_queue[0]] != 0:
                self.next_dir['current'] = next_queue

            # Start moving if next move is valid
            current = self.next_dir['current']
            if grid[int(self.y) + current[1]][int(self.x) + current[0]] != 0:
                self.moving = True
                self.move_count = 0

        if self.moving:
            dx, dy = self.next_dir['current']
            self.x += dx / self.speed
            self.y += dy / self.speed
            self.x = round(self.x, 2)
            self.y = round(self.y, 2)
            self.move_count += 1

            if self.move_count == self.speed:
                self.x = round(self.x)
                self.y = round(self.y)
                self.moving = False


class Pacman(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PACMAN_IMAGE, speed=8)
        self.points = 0

    def eat(self, stars, update_callback):
        # Use a list copy for stars in case removal is done inside iteration.
        if (self.x, self.y) in stars:
            stars.remove((self.x, self.y))
            self.points += 10

        if not stars:
            update_callback("Won")


class Ghost(Entity):
    def __init__(self, x, y, image, speed=10):
        super().__init__(x, y, image, speed)
        self.target = (0, 0)

    def targeting(self, grid, pacman):
        best_direction = (0, 0)
        min_distance = float("inf")
        # Reset queued direction
        self.next_dir['queued'] = (0, 0)

        # Check 4 directions: Left, Right, Up, Down with constraints based on last move
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            # Ensure within grid and not a wall (grid value != 0)
            if grid[int(new_y)][int(new_x)] != 0:
                # Avoid immediate reverse of movement
                if (dx, dy) == tuple(-x for x in self.next_dir['current']):
                    continue
                dist = get_distance((new_y, new_x), self.target)
                if dist < min_distance:
                    min_distance = dist
                    best_direction = (dx, dy)
        self.next_dir['queued'] = best_direction
        self.move(grid)
        self.check_attack(pacman)

    def check_attack(self, pacman):
        if get_distance((self.x, self.y), (pacman.x, pacman.y)) < 0.6:
            display_message(game_screen, "Lost")
            game_over()


# Specific Ghosts with unique targeting logic
class Blinky(Ghost):
    def __init__(self):
        super().__init__(1, 28, RED_IMAGE)
    
    def update_target(self, pacman):
        self.target = (pacman.y, pacman.x)
        

class Pinky(Ghost):
    def __init__(self):
        super().__init__(1, 1, PINK_IMAGE)
    
    def update_target(self, pacman):
        # Aim four steps ahead of pacman
        dx, dy = pacman.next_dir['current']
        self.target = (pacman.y + dy * 4, pacman.x + dx * 4)
        # Adjust for upward movement
        if pacman.next_dir['current'][1] == -1:
            self.target = (pacman.y - 4, pacman.x - 4)


class Inky(Ghost):
    def __init__(self, blinky):
        super().__init__(26, 26, BLUE_IMAGE)
        self.blinky = blinky

    def update_target(self, pacman):
        # Two steps in the current pacman direction
        dx, dy = pacman.next_dir['current']
        two_in_front = (pacman.y + dy * 2, pacman.x + dx * 2)
        vector = (two_in_front[0] - self.blinky.y, two_in_front[1] - self.blinky.x)
        self.target = (pacman.y + vector[0], pacman.x + vector[1])


class Clyde(Ghost):
    def __init__(self):
        super().__init__(26, 1, ORANGE_IMAGE)
    
    def update_target(self, pacman):
        self.target = (pacman.y, pacman.x)
        # If close to pacman, change target
        if get_distance((self.x, self.y), (pacman.x, pacman.y)) < 8:
            self.target = (29, 1)


# Global star list
stars_left = []


def initialize_stars(screen):
    """Generate stars based on GRID data."""
    global stars_left
    stars_left = []
    for row_index, row in enumerate(GRID):
        for col_index, value in enumerate(row):
            if value == 1:
                pygame.draw.circle(screen, STAR_COLOR, (x_coord(col_index), y_coord(row_index)), 5)
                stars_left.append((col_index, row_index))
    pygame.display.update()


def update_screen(screen, background, stars, pacman, ghosts):
    """Clear and redraw the screen including UI elements."""
    screen.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))
    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, (x_coord(star[0]), y_coord(star[1])), 5)

    # Draw ghosts
    for ghost in ghosts:
        ghost.display(screen)
    # Draw pacman
    pacman.display(screen)
    # Draw score
    score_text = SMALL_FONT.render(f"Points: {pacman.points}", True, (255, 255, 255))
    screen.blit(score_text, (40, SCREEN_HEIGHT + 15))
    pygame.display.update()


def game_over():
    """Simple game over loop waiting for space to restart."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main()


def main():
    global game_screen
    pygame.display.set_caption("Pacman by CZ")
    game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + EXTRA_HEIGHT))
    game_screen.fill(BACKGROUND_COLOR)
    game_screen.blit(BACKGROUND_IMAGE, (0, 0))
    pygame.display.update()

    # Initialize stars on screen based on the GRID
    initialize_stars(game_screen)

    # Create player and ghosts
    player = Pacman(13, 17)
    blinky = Blinky()
    pinky = Pinky()
    inky = Inky(blinky)
    clyde = Clyde()
    ghosts = [blinky, pinky, inky, clyde]

    clock = pygame.time.Clock()
    
    # Game loop
    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # Reset queued direction for Pacman
                if event.key == pygame.K_a:
                    player.next_dir['queued'] = (-1, 0)
                elif event.key == pygame.K_d:
                    player.next_dir['queued'] = (1, 0)
                elif event.key == pygame.K_w:
                    player.next_dir['queued'] = (0, -1)
                elif event.key == pygame.K_s:
                    player.next_dir['queued'] = (0, 1)

        # Update pacman and ghost movements
        player.move(GRID)
        for ghost in ghosts:
            if isinstance(ghost, Blinky):
                ghost.update_target(player)
            elif isinstance(ghost, Pinky):
                ghost.update_target(player)
            elif isinstance(ghost, Inky):
                ghost.update_target(player)
            elif isinstance(ghost, Clyde):
                ghost.update_target(player)
            ghost.targeting(GRID, player)

        # Pacman eats stars and checks win condition
        player.eat(stars_left, lambda result: (display_message(game_screen, result), game_over()))
        # Update the screen graphics
        update_screen(game_screen, BACKGROUND_IMAGE, stars_left, player, ghosts)
        clock.tick(FPS)


if __name__ == "__main__":
    main()
