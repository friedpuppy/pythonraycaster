import pygame
import config

# Dictionary to hold loaded game assets
game_assets = {}

def load_image(path, scale_factor=1.0, use_alpha=True, colorkey=None):
    """Loads an image, scales it, and converts it for Pygame."""
    try:
        image = pygame.image.load(path)
        size = image.get_size()
        scaled_size = (int(size[0] * scale_factor), int(size[1] * scale_factor))
        image = pygame.transform.scale(image, scaled_size)

        if use_alpha:
            image = image.convert_alpha()
        else:
            image = image.convert() # Convert first for non-alpha images
            if colorkey is not None: # Apply colorkey after conversion
                image.set_colorkey(colorkey)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        return None # Or raise an error, or return a placeholder surface

def load_spritesheet(path, frame_width, frame_height, num_frames, scale_factor=1.0, use_alpha=True):
    """Loads a horizontal spritesheet, extracts frames, scales them, and converts them."""
    frames = []
    try:
        spritesheet = pygame.image.load(path)
        sheet_width, sheet_height = spritesheet.get_size()

        if frame_width * num_frames > sheet_width or frame_height > sheet_height:
            print(f"Warning: Spritesheet dimensions may not match frame data for {path}")

        for i in range(num_frames):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = spritesheet.subsurface(rect)
            scaled_size = (int(frame_width * scale_factor), int(frame_height * scale_factor))
            scaled_frame = pygame.transform.scale(frame, scaled_size)
            frames.append(scaled_frame.convert_alpha() if use_alpha else scaled_frame.convert())
        return frames
    except pygame.error as e:
        print(f"Error loading spritesheet {path}: {e}")
        return [] # Return empty list on error

def load_animation_frames(frame_paths, scale_factor=1.0, use_alpha=True, colorkey=None):
    """Loads a sequence of images from a list of paths to be used as animation frames."""
    frames = []
    for path in frame_paths:
        image = load_image(path, scale_factor, use_alpha, colorkey)
        if image:
            frames.append(image)
        # If an image fails to load, load_image already prints an error.
    return frames

def load_all_assets():
    """Loads all game assets like textures and sprites."""
    global game_assets

    # Load Wall Texture
    game_assets['wall_texture'] = load_image(config.WALL_TEXTURE_PATH, scale_factor=1.0, use_alpha=False)
    if game_assets.get('wall_texture'):
        game_assets['wall_texture_width'] = game_assets['wall_texture'].get_width()
        game_assets['wall_texture_height'] = game_assets['wall_texture'].get_height()
        print(f"Wall texture '{config.WALL_TEXTURE_PATH}' loaded ({game_assets['wall_texture_width']}x{game_assets['wall_texture_height']}).")
    else:
        print(f"ERROR: Failed to load wall texture: {config.WALL_TEXTURE_PATH}")
        # Consider setting default dimensions or a placeholder texture if loading fails
        game_assets['wall_texture_width'] = 64 # Default fallback
        game_assets['wall_texture_height'] = 64 # Default fallback

    # Load Weapon Graphics
    game_assets['pistol_idle'] = load_image(
        config.PISTOL_IDLE_IMAGE_PATH,
        config.PISTOL_SCALE_FACTOR,
        use_alpha=False,
        colorkey=config.PISTOL_COLORKEY
    )
    game_assets['pistol_fire_frames'] = load_animation_frames(
        config.PISTOL_FIRE_FRAME_PATHS,
        scale_factor=config.PISTOL_SCALE_FACTOR,
        use_alpha=False,
        colorkey=config.PISTOL_COLORKEY
    )

def init_screen():
    """Initializes the Pygame screen and returns it."""
    # Attempt to enable VSync for smoother rendering and to prevent tearing
    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
        vsync=1  # Request VSync
    )
    pygame.display.set_caption("Raycaster Demo - WASD Movement, Arrow Key Rotation")
    return screen

def draw_background(screen):
    """Draws the ceiling and floor."""
    screen.fill(config.CEILING_COLOR)
    pygame.draw.rect(screen, config.FLOOR_COLOR, (0, config.SCREEN_HEIGHT // 2, config.SCREEN_WIDTH, config.SCREEN_HEIGHT // 2))

def draw_wall_strip(screen, screen_x_pos, draw_start_y, line_height_on_screen,
                      wall_hit_coord_on_segment, side_hit, ray_dir_x, ray_dir_y):
    """Draws a single textured vertical wall strip."""
    wall_texture = game_assets.get('wall_texture')
    wall_texture_width = game_assets.get('wall_texture_width', 64)
    wall_texture_height = game_assets.get('wall_texture_height', 64)

    if not wall_texture or line_height_on_screen <= 0:
        # Fallback to drawing solid color if texture not loaded or strip too small
        fallback_color = config.SHADED_WALL_COLOR if side_hit == 1 else config.BASE_WALL_COLOR
        pygame.draw.rect(screen, fallback_color, (screen_x_pos, draw_start_y, config.STRIP_WIDTH, line_height_on_screen))
        return

    # Calculate the x-coordinate on the texture
    tex_x = int(wall_hit_coord_on_segment * wall_texture_width)

    # Adjust tex_x for texture mirroring based on ray direction (Lodev's conditions)
    if side_hit == 0 and ray_dir_x > 0:
        tex_x = wall_texture_width - tex_x - 1
    if side_hit == 1 and ray_dir_y < 0:
        tex_x = wall_texture_width - tex_x - 1
    
    tex_x = max(0, min(tex_x, wall_texture_width - 1)) # Clamp tex_x

    # Get the 1-pixel wide column from the texture
    texture_column_rect = pygame.Rect(tex_x, 0, 1, wall_texture_height)
    texture_strip_original = wall_texture.subsurface(texture_column_rect)

    # Scale this strip to the calculated height on screen
    scaled_texture_strip = pygame.transform.scale(texture_strip_original, (config.STRIP_WIDTH, line_height_on_screen))

    # Blit the scaled strip
    screen.blit(scaled_texture_strip, (screen_x_pos, draw_start_y))

    # Apply shading for walls hit on Y-sides (horizontal walls)
    if side_hit == 1:
        shade_overlay = pygame.Surface((config.STRIP_WIDTH, line_height_on_screen), pygame.SRCALPHA)
        shade_overlay.fill((0, 0, 0, int(255 * (1.0 - config.WALL_TEXTURE_DARKEN_FACTOR)))) # Darken
        screen.blit(shade_overlay, (screen_x_pos, draw_start_y))

def draw_weapon(screen, weapon_image, weapon_rect):
    """Draws the weapon on the screen."""
    if weapon_image and weapon_rect:
        screen.blit(weapon_image, weapon_rect)