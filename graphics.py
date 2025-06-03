import pygame
import config

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
    # The width of the strip is determined by config.STRIP_WIDTH
    pygame.draw.rect(screen, color, (screen_x_pos, draw_start, config.STRIP_WIDTH, draw_end - draw_start))