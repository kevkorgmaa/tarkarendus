import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (40, 40, 40)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game difficulties (frames per second)
EASY = 8
MEDIUM = 12
HARD = 16
EXTREME = 20

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Python Snake')

# Fonts
font = pygame.font.SysFont('Arial', 25)
title_font = pygame.font.SysFont('Arial', 50)

# Clock to control game speed
clock = pygame.time.Clock()


def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_snake(snake_positions):
    # Draw snake body
    for i, position in enumerate(snake_positions):
        # Calculate rect coordinates
        x = position[0] * GRID_SIZE
        y = position[1] * GRID_SIZE

        # Use different shades of green for the snake body
        if i == 0:  # Head
            color = (0, 200, 0)  # Brighter green for the head
            # Draw a slightly rounded rectangle for the head
            pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))

            # Add eyes to the head
            eye_size = GRID_SIZE // 5
            # Determine eye positions based on direction
            if direction == UP:
                left_eye = (x + eye_size, y + eye_size)
                right_eye = (x + GRID_SIZE - 2 * eye_size, y + eye_size)
            elif direction == DOWN:
                left_eye = (x + eye_size, y + GRID_SIZE - 2 * eye_size)
                right_eye = (x + GRID_SIZE - 2 * eye_size, y + GRID_SIZE - 2 * eye_size)
            elif direction == LEFT:
                left_eye = (x + eye_size, y + eye_size)
                right_eye = (x + eye_size, y + GRID_SIZE - 2 * eye_size)
            elif direction == RIGHT:
                left_eye = (x + GRID_SIZE - 2 * eye_size, y + eye_size)
                right_eye = (x + GRID_SIZE - 2 * eye_size, y + GRID_SIZE - 2 * eye_size)
            else:  # Default (RIGHT)
                left_eye = (x + GRID_SIZE - 2 * eye_size, y + eye_size)
                right_eye = (x + GRID_SIZE - 2 * eye_size, y + GRID_SIZE - 2 * eye_size)

            pygame.draw.circle(screen, BLACK, left_eye, eye_size)
            pygame.draw.circle(screen, BLACK, right_eye, eye_size)

        else:  # Body
            # Create a gradient effect from darker to lighter green
            intensity = max(100, 180 - (i * 3))
            color = (0, intensity, 0)

            # Draw body segment with slightly rounded corners
            pygame.draw.rect(screen, color, (x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2), border_radius=2)


def draw_food(food_position):
    x = food_position[0] * GRID_SIZE
    y = food_position[1] * GRID_SIZE

    # Draw an apple-like shape
    # Main circle (red apple body)
    radius = GRID_SIZE // 2
    center = (x + radius, y + radius)
    pygame.draw.circle(screen, RED, center, radius)

    # Stem (brown)
    stem_color = (139, 69, 19)  # Brown
    pygame.draw.rect(screen, stem_color, (x + radius - 1, y, 2, radius // 2))

    # Shine/highlight (lighter red)
    highlight_color = (255, 150, 150)
    pygame.draw.circle(screen, highlight_color, (center[0] - 2, center[1] - 2), radius // 4)


def generate_food_position(snake_positions):
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        food_position = (x, y)

        # Make sure food doesn't appear on the snake
        if food_position not in snake_positions:
            return food_position


def is_collision_with_walls(position):
    x, y = position
    return (x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT)


def is_collision_with_self(snake_positions):
    head = snake_positions[0]
    return head in snake_positions[1:]


def reset_game():
    return [(5, 5), (4, 5), (3, 5)], RIGHT, generate_food_position([(5, 5), (4, 5), (3, 5)]), 0


def draw_score(score):
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))


def draw_game_over():
    game_over_text = font.render('Game Over! Press R to Restart', True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))


def draw_start_screen():
    title_font = pygame.font.SysFont('Arial', 50)
    instruction_font = pygame.font.SysFont('Arial', 25)

    title = title_font.render('PYTHON SNAKE', True, GREEN)
    select_difficulty = instruction_font.render('Select Difficulty:', True, WHITE)
    easy = instruction_font.render('1 - Easy', True, WHITE)
    medium = instruction_font.render('2 - Medium', True, WHITE)
    hard = instruction_font.render('3 - Hard', True, WHITE)
    extreme = instruction_font.render('4 - Extreme', True, WHITE)

    screen.blit(title, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 4))
    screen.blit(select_difficulty, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
    screen.blit(easy, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
    screen.blit(medium, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 30))
    screen.blit(hard, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 60))
    screen.blit(extreme, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 90))


def main():
    global direction  # Need this for the eyes in the snake head

    snake_positions, direction, food_position, score = reset_game()
    game_over = False
    game_started = False
    speed = MEDIUM  # Default difficulty

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not game_started:
                    # Select difficulty
                    if event.key == pygame.K_1:
                        speed = EASY
                        game_started = True
                    elif event.key == pygame.K_2:
                        speed = MEDIUM
                        game_started = True
                    elif event.key == pygame.K_3:
                        speed = HARD
                        game_started = True
                    elif event.key == pygame.K_4:
                        speed = EXTREME
                        game_started = True
                elif not game_over:
                    if event.key == pygame.K_UP and direction != DOWN:
                        direction = UP
                    elif event.key == pygame.K_DOWN and direction != UP:
                        direction = DOWN
                    elif event.key == pygame.K_LEFT and direction != RIGHT:
                        direction = LEFT
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        direction = RIGHT
                    # Pause game with spacebar
                    elif event.key == pygame.K_SPACE:
                        paused = True
                        while paused:
                            for pause_event in pygame.event.get():
                                if pause_event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_SPACE:
                                    paused = False

                            pause_text = font.render('PAUSED - Press SPACE to continue', True, WHITE)
                            screen.blit(pause_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
                            pygame.display.flip()
                            clock.tick(5)
                elif event.key == pygame.K_r:  # Restart game if R is pressed
                    snake_positions, direction, food_position, score = reset_game()
                    game_over = False
                    game_started = False

        # Fill the screen with black
        screen.fill(BLACK)

        if not game_started:
            # Draw start screen
            draw_start_screen()
        else:
            if not game_over:
                # Move the snake
                head_x, head_y = snake_positions[0]
                new_x, new_y = head_x + direction[0], head_y + direction[1]
                new_head = (new_x, new_y)

                # Check for collisions
                if is_collision_with_walls(new_head) or new_head in snake_positions[1:]:
                    game_over = True
                else:
                    snake_positions.insert(0, new_head)

                    # Check if snake has eaten the food
                    if new_head == food_position:
                        # Generate new food
                        food_position = generate_food_position(snake_positions)
                        score += 1

                        # Increase speed slightly with each food eaten
                        if score % 5 == 0 and speed < EXTREME + 5:
                            speed += 1
                    else:
                        # Remove the tail (snake didn't eat food, so it doesn't grow)
                        snake_positions.pop()

            # Draw the grid
            draw_grid()

            # Draw the food
            draw_food(food_position)

            # Draw the snake
            draw_snake(snake_positions)

            # Draw the score
            draw_score(score)

            # Draw game over message if game is over
            if game_over:
                draw_game_over()

        # Update the display
        pygame.display.flip()

        # Set the game speed based on difficulty and score
        clock.tick(speed)


if __name__ == "__main__":
    main()

