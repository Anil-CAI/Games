import pygame
import math
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Default background color
current_background_color = (255, 255, 255)

# Background music
mixer.music.load(r"D:\games\space_war\music\bgsound.mp3")
mixer.music.play(-1)

# Laser sound
laser_sound = mixer.Sound(r"D:\games\space_war\music\laser.wav")

# Explosion sound
explosion_sound = mixer.Sound(r"D:\games\space_war\music\explosion.wav")

# Title & Icon
pygame.display.set_caption("Space Fire")
icon = pygame.image.load(r"D:\\games\\space_war\\images\\logo1.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load(r"D:/games/space_war/images/space-invaders.png")
player_img = pygame.transform.scale(player_img, (64, 64))
player_x = 370
player_y = 480
player_x_change = 0

def draw_player(x, y):
    screen.blit(player_img, (x, y))

# Enemy
enemy_imgs = []
enemy_positions = []
enemy_speeds = []
num_of_enemies = 5
current_level = 1

def init_enemies(level):
    global enemy_imgs, enemy_positions, enemy_speeds
    enemy_imgs = []
    enemy_positions = []
    enemy_speeds = []
    for _ in range(num_of_enemies + level):  # Increase enemies as level increases
        enemy_img = pygame.image.load(r"D:/games/space_war/images/asteroid.png")
        enemy_img = pygame.transform.scale(enemy_img, (64, 64))
        enemy_imgs.append(enemy_img)
        enemy_positions.append([random.randint(0, SCREEN_WIDTH - 64), random.randint(50, 150)])
        enemy_speeds.append([random.choice([-0.5 * level, 0.5 * level]), 40])

def draw_enemy(x, y, i):
    screen.blit(enemy_imgs[i], (x, y))

# Bullet
bullet_img = pygame.image.load(r"D:/games/space_war/images/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (32, 32))
bullet_x = 0
bullet_y = player_y
bullet_speed = 10
bullet_state = 'ready'

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))

# Explosion effect
explosion_img = pygame.image.load(r"D:/games/space_war/images/explosion.png")
explosion_img = pygame.transform.scale(explosion_img, (64, 64))

def draw_explosion(x, y):
    screen.blit(explosion_img, (x, y))

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

def show_score():
    score_text = font.render(f"Score: {score_value}  Level: {current_level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))

# Collision Detection
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27

# Initialize enemies
init_enemies(current_level)

# Main Game Loop
running = True
explosion_timer = -1
explosion_position = (0, 0)
while running:
    # Update background color
    screen.fill(current_background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key press events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                laser_sound.play()
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        # Key release events
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    player_x = max(0, min(player_x, SCREEN_WIDTH - 64))

    # Enemy movement
    for i in range(len(enemy_positions)):
        enemy_x, enemy_y = enemy_positions[i]
        enemy_x += enemy_speeds[i][0]

        # Bounce enemy off edges
        if enemy_x <= 0 or enemy_x >= SCREEN_WIDTH - 64:
            enemy_speeds[i][0] *= -1
            enemy_y += enemy_speeds[i][1]

        # Check for game over
        if enemy_y >= player_y:
            for j in range(len(enemy_positions)):
                enemy_positions[j][1] = SCREEN_HEIGHT + 100
            game_over()
            running = False

        # Collision detection
        if is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
            explosion_sound.play()
            bullet_y = player_y
            bullet_state = 'ready'
            score_value += 1
            explosion_timer = pygame.time.get_ticks() + 500
            explosion_position = (enemy_x, enemy_y)
            enemy_positions[i] = [random.randint(0, SCREEN_WIDTH - 64), random.randint(50, 150)]

        enemy_positions[i] = [enemy_x, enemy_y]
        draw_enemy(enemy_x, enemy_y, i)

    # Level up logic
    if score_value > 0 and score_value % 20 == 0:
        current_level = score_value // 20 + 1
        init_enemies(current_level)
        score_value += 1  # Prevent repeated triggering of level-up

    # Bullet movement
    if bullet_state == 'fire':
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_y = player_y
            bullet_state = 'ready'

    # Draw explosion if active
    if explosion_timer > 0 and pygame.time.get_ticks() < explosion_timer:
        draw_explosion(*explosion_position)

    # Draw player and score
    draw_player(player_x, player_y)
    show_score()

    pygame.display.update()

pygame.quit()
