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
NUM_RAYS = SCREEN_WIDTH // 2
STRIP_WIDTH = SCREEN_WIDTH // NUM_RAYS

# Colors
CEILING_COLOR = (30, 30, 70)   # Dark blueish
FLOOR_COLOR = (70, 70, 70)     # Dark gray
BASE_WALL_COLOR = (139, 69, 19) # A brownish color (SaddleBrown)
# Shaded color for walls facing North/South to give a sense of depth
SHADED_WALL_COLOR = tuple(int(c * 0.7) for c in BASE_WALL_COLOR)

# Weapon Settings
PISTOL_IDLE_IMAGE_PATH = "pistol_idle.png"
PISTOL_FIRE_IMAGE_PATH = "pistol_fire.png"
PISTOL_SCALE_FACTOR = 0.5  # Adjust to fit your sprite size
PISTOL_Y_OFFSET = 10       # Vertical offset from the bottom of the screen
PISTOL_FIRE_DURATION_MS = 100 # Duration of the firing animation in milliseconds