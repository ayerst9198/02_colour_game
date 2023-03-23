import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2D Platformer")

# Set up the game clock
clock = pygame.time.Clock()

# Set up the player
player_rect = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 50, 50)
player_color = pygame.Color('red')
player_speed = 5
player_jump = False
player_y_momentum = 0
player_coyote_time = 10

# Set up the platforms
platform_rects = [
    pygame.Rect(200, 400, 400, 50),
    pygame.Rect(0, 550, WINDOW_WIDTH, 50),
]
platform_color = pygame.Color('white')

# Set up the gravity
gravity = 0.3
max_fall_speed = 10
gravity_switch = False

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (not player_jump or player_coyote_time > 0):
                player_jump = True
                player_y_momentum = -12
                player_coyote_time = 0

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_rect.left > 0:
        player_rect.x -= player_speed
    elif keys[pygame.K_d] and player_rect.right < WINDOW_WIDTH:
        player_rect.x += player_speed

    # Handle player jumping
    if player_jump:
        player_y_momentum += gravity
        player_rect.y += player_y_momentum
        if player_y_momentum >= max_fall_speed:
            player_jump = False
            player_y_momentum = max_fall_speed
    elif player_coyote_time < 10:
        player_coyote_time += 1

    # Handle gravity
    if not player_jump:
        if gravity_switch:
            player_rect.y -= 5
        else:
            player_rect.y += 5
    for platform_rect in platform_rects:
        if player_rect.colliderect(platform_rect):
            if player_jump and player_y_momentum < 0:
                player_rect.top = platform_rect.bottom
                player_y_momentum = 0
                player_coyote_time = 0
            elif not player_jump and player_rect.bottom == platform_rect.top:
                gravity_switch = True
                player_rect.bottom = platform_rect.top
            else:
                if player_rect.bottom > platform_rect.top:
                    player_rect.bottom = platform_rect.top
                    player_y_momentum = 0
        else:
            gravity_switch = False

    # Draw the game
    window.fill((0, 0, 0))
    pygame.draw.rect(window, player_color, player_rect)
    for platform_rect in platform_rects:
        pygame.draw.rect(window, platform_color, platform_rect)
    pygame.display.flip()

    # Wait for next frame
    clock.tick(60)

# Clean up
pygame.quit()
