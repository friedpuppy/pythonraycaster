import math

# --- Constants ---
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Player initial settings
PLAYER_INITIAL_X = 3.5  # Initial x position (in grid units)
PLAYER_INITIAL_Y = 3.5  # Initial y position (in grid units)
PLAYER_INITIAL_ANGLE = math.pi / 4  # Initial viewing angle (radians)
FOV = math.pi / 3  # Field of View (e.g., 60 degrees)
MOVE_SPEED = 0.05 # Grid units per frame (adjust for faster/slower movement)
ROT_SPEED = 0.03  # Radians per frame (adjust for faster/slower rotation)
STRAFE_ANGLE = math.pi / 2 # 90 degrees for strafing

# Raycasting settings
# NUM_RAYS can be SCREEN_WIDTH for 1-pixel wide strips, or less for wider strips.
# Using SCREEN_WIDTH // 2 means each vertical strip will be 2 pixels wide.
NUM_RAYS = SCREEN_WIDTH # Cast one ray per screen column
STRIP_WIDTH = 1 # Each strip is 1 pixel wide

# Colors
CEILING_COLOR = (30, 30, 70)   # Dark blueish
FLOOR_COLOR = (70, 70, 70)     # Dark gray
BASE_WALL_COLOR = (139, 69, 19) # A brownish color (SaddleBrown)
# Shaded color for walls facing North/South to give a sense of depth
SHADED_WALL_COLOR = tuple(int(c * 0.7) for c in BASE_WALL_COLOR)

# Texture Settings
WALL_TEXTURE_PATH = "assets/textures/stonewall.png"
WALL_TEXTURE_DARKEN_FACTOR = 0.7 # How much to darken textures on 'shaded' sides

# Weapon Settings
PISTOL_IDLE_IMAGE_PATH = "assets/sprites/pistol_idle.png"
PISTOL_SCALE_FACTOR = 4.0  # Adjust to fit your sprite size
PISTOL_Y_OFFSET = 0       # Vertical offset from the bottom of the screen
PISTOL_COLORKEY = (152, 0, 136) # The #980088 color

# Pistol Firing Animation Settings
PISTOL_FIRE_FRAME_PATHS = [
    "assets/sprites/pistol_fire1.png",
    "assets/sprites/pistol_fire2.png",
    "assets/sprites/pistol_fire3.png",
    "assets/sprites/pistol_fire4.png"
]
PISTOL_FIRE_ANIMATION_SPEED_MS = 75 # Milliseconds each frame is displayed
