import pygame
import config

def load_image(path, scale_factor=1.0, use_alpha=True):
    """Loads an image, scales it, and converts it for Pygame."""
    try:
        image = pygame.image.load(path)
        size = image.get_size()
        scaled_size = (int(size[0] * scale_factor), int(size[1] * scale_factor))
        image = pygame.transform.scale(image, scaled_size)
        return image.convert_alpha() if use_alpha else image.convert()
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        return None # Or raise an error, or return a placeholder surface

def init_screen():
    """Initializes the Pygame screen and returns it."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Raycaster Demo - WASD Movement, Arrow Key Rotation")
    return screen

def draw_background(screen):
    """Draws the ceiling and floor."""
    screen.fill(config.CEILING_COLOR)
    pygame.draw.rect(screen, config.FLOOR_COLOR, (0, config.SCREEN_HEIGHT // 2, config.SCREEN_WIDTH, config.SCREEN_HEIGHT // 2))

def draw_wall_strip(screen, screen_x_pos, draw_start, draw_end, color):
    """Draws a single vertical wall strip."""
    pygame.draw.rect(screen, color, (screen_x_pos, draw_start, config.STRIP_WIDTH, draw_end - draw_start))

def draw_weapon(screen, weapon_image, weapon_rect):
    """Draws the weapon on the screen."""
    if weapon_image and weapon_rect:
        screen.blit(weapon_image, weapon_rect)