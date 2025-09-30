import pygame, sys, os

pygame.init()

# Settings
WIDTH, HEIGHT = 960, 540
FPS = 60
ASSETS = os.path.join(os.path.dirname(__file__), "assets")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Runner - Infinite Background")
clock = pygame.time.Clock()

# Load background
bg_path = os.path.join(ASSETS, "background.png")
if not os.path.isfile(bg_path):
    raise FileNotFoundError(f"Không tìm thấy {bg_path}, hãy để background.png trong thư mục assets/")
bg_image = pygame.image.load(bg_path).convert()
bg_image = pygame.transform.smoothscale(bg_image, (WIDTH, HEIGHT))
bg_width = bg_image.get_width()

# Load player sprites
run_frames = [
    pygame.image.load(os.path.join(ASSETS, "run1.png")).convert_alpha(),
    pygame.image.load(os.path.join(ASSETS, "run2.png")).convert_alpha()
]
jump_frame = pygame.image.load(os.path.join(ASSETS, "jump.png")).convert_alpha()

# Player state
player_x = 120
player_y = HEIGHT - 200
player_vy = 0
on_ground = True
run_index = 0.0
RUN_SPEED = 0.18

GRAVITY = 0.8
JUMP_POWER = -14

# Scroll world
scroll = 0.0
world_speed = 4.0

def draw_infinite_bg(surface, bg_surf, scroll_x):
    """Vẽ background cuộn vô hạn"""
    w = bg_surf.get_width()
    offset = int(scroll_x % w)
    x = -offset
    while x < WIDTH:
        surface.blit(bg_surf, (x, 0))
        x += w

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and on_ground:
        player_vy = JUMP_POWER
        on_ground = False

    # Physics
    player_vy += GRAVITY
    player_y += player_vy
    if player_y >= HEIGHT - 200:
        player_y = HEIGHT - 200
        player_vy = 0
        on_ground = True

    # Animation
    if on_ground:
        run_index += RUN_SPEED * (dt * 60)
        if run_index >= len(run_frames):
            run_index = 0.0
        player_image = run_frames[int(run_index)]
    else:
        player_image = jump_frame

    # Scroll background
    scroll += world_speed

    # Draw
    draw_infinite_bg(screen, bg_image, scroll)
    screen.blit(player_image, (player_x, int(player_y)))

    pygame.display.flip()

pygame.quit()
sys.exit()

