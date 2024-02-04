import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_COLOR = (255, 255, 255)
BALL_SIZE = 20
BALL_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
FONT_COLOR = (255, 255, 255)
WINNING_SCORE = 5  # Set the winning score

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong")

# Game variables
paddle_left_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
paddle_right_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = random.choice([5, -5])
ball_speed_y = random.choice([3, -3])
paddle_speed = 8
score_left = 0
score_right = 0

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for rendering text
font = pygame.font.Font(None, 36)

# Function to draw the left paddle
def draw_paddle_left(y):
    pygame.draw.rect(screen, PADDLE_COLOR, (0, y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to draw the right paddle
def draw_paddle_right(y):
    pygame.draw.rect(screen, PADDLE_COLOR, (SCREEN_WIDTH - PADDLE_WIDTH, y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to draw the ball
def draw_ball(x, y):
    pygame.draw.circle(screen, BALL_COLOR, (x, y), BALL_SIZE)

# Function to display the score
def display_score():
    score_display = font.render(f"{score_left} - {score_right}", True, FONT_COLOR)
    screen.blit(score_display, (SCREEN_WIDTH // 2 - 50, 10))

# Function to display the winner
def display_winner(winner):
    winner_text = font.render(f"{winner} WINS!", True, FONT_COLOR)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the winner for 3 seconds
    reset_game()

# Function to reset the game
def reset_game():
    global score_left, score_right
    score_left = 0
    score_right = 0
    reset_ball()

# Function to reset the ball position and speed
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_speed_x = random.choice([5, -5])
    ball_speed_y = random.choice([3, -3])

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Move paddles based on keys
    if keys[pygame.K_w] and paddle_left_y > 0:
        paddle_left_y -= paddle_speed
    if keys[pygame.K_s] and paddle_left_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle_left_y += paddle_speed

    if keys[pygame.K_UP] and paddle_right_y > 0:
        paddle_right_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_right_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle_right_y += paddle_speed

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collisions with walls
    if ball_y - BALL_SIZE <= 0 or ball_y + BALL_SIZE >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Check for collisions with paddles
    if (
        (0 <= ball_x - BALL_SIZE <= PADDLE_WIDTH and paddle_left_y <= ball_y <= paddle_left_y + PADDLE_HEIGHT) or
        (SCREEN_WIDTH - PADDLE_WIDTH <= ball_x + BALL_SIZE <= SCREEN_WIDTH and
         paddle_right_y <= ball_y <= paddle_right_y + PADDLE_HEIGHT)
    ):
        ball_speed_x *= -1

    # Check for scoring
    if ball_x - BALL_SIZE <= 0:
        score_right += 1
        if score_right == WINNING_SCORE:
            display_winner("Player on the Right")
        else:
            reset_ball()

    if ball_x + BALL_SIZE >= SCREEN_WIDTH:
        score_left += 1
        if score_left == WINNING_SCORE:
            display_winner("Player on the Left")
        else:
            reset_ball()

    # Draw everything on the screen
    screen.fill(BACKGROUND_COLOR)
    draw_paddle_left(paddle_left_y)
    draw_paddle_right(paddle_right_y)
    draw_ball(int(ball_x), int(ball_y))
    display_score()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
