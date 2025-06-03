#/usr/bin/env python3
import pygame
import math
import config
import map as game_map # Alias to avoid conflict with built-in map function
import graphics

# Player state
player_x = config.PLAYER_INITIAL_X
player_y = config.PLAYER_INITIAL_Y
player_angle = config.PLAYER_INITIAL_ANGLE

def main():
    global player_x, player_y, player_angle

    pygame.init()
    screen = graphics.init_screen()
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(config.FPS) / 1000.0 # Delta time in seconds, not used yet but good practice

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Handle Input ---
        keys = pygame.key.get_pressed()

        # Calculate intended movement vector components
        move_x_component = 0
        move_y_component = 0

        # Forward/Backward (W/S)
        if keys[pygame.K_w]:
            move_x_component += config.MOVE_SPEED * math.cos(player_angle)
            move_y_component += config.MOVE_SPEED * math.sin(player_angle)
        if keys[pygame.K_s]:
            move_x_component -= config.MOVE_SPEED * math.cos(player_angle)
            move_y_component -= config.MOVE_SPEED * math.sin(player_angle)

        # Strafe Left/Right (A/D)
        strafe_angle_rad = math.pi / 2 # 90 degrees
        if keys[pygame.K_a]: # Strafe Left
            move_x_component += config.MOVE_SPEED * math.cos(player_angle - strafe_angle_rad)
            move_y_component += config.MOVE_SPEED * math.sin(player_angle - strafe_angle_rad)
        if keys[pygame.K_d]: # Strafe Right
            move_x_component += config.MOVE_SPEED * math.cos(player_angle + strafe_angle_rad)
            move_y_component += config.MOVE_SPEED * math.sin(player_angle + strafe_angle_rad)

        # Rotation (Left/Right Arrow Keys)
        if keys[pygame.K_LEFT]:
            player_angle -= config.ROT_SPEED
        if keys[pygame.K_RIGHT]:
            player_angle += config.ROT_SPEED
        player_angle = (player_angle + 2 * math.pi) % (2 * math.pi) # Normalize angle to [0, 2*pi)

        # --- Collision Detection & Position Update ---
        # New potential positions based on intended movement
        potential_new_x = player_x + move_x_component
        potential_new_y = player_y + move_y_component
 
        # Check X-axis collision:
        # If the new x-position is valid (not in a wall), update player_x.
        # Otherwise, player_x remains unchanged for this component of movement.
        if 0 <= int(potential_new_x) < game_map.MAP_WIDTH and \
           0 <= int(player_y) < game_map.MAP_HEIGHT and \
           game_map.MAP_DATA[int(player_y)][int(potential_new_x)] == 0:
            player_x = potential_new_x

        # Check Y-axis collision (using the possibly updated player_x for the map check):
        # If the new y-position is valid (not in a wall), update player_y.
        # Otherwise, player_y remains unchanged for this component of movement.
        # This method allows "sliding" along walls.
        if 0 <= int(player_x) < game_map.MAP_WIDTH and \
           0 <= int(potential_new_y) < game_map.MAP_HEIGHT and \
           game_map.MAP_DATA[int(potential_new_y)][int(player_x)] == 0:
            player_y = potential_new_y

        # --- Rendering ---
        graphics.draw_background(screen)

        # Raycasting
        angle_increment = config.FOV / config.NUM_RAYS

        for i in range(config.NUM_RAYS):
            # Calculate the angle for the current ray
            ray_angle = player_angle - config.FOV / 2 + i * angle_increment
            ray_angle = (ray_angle + 2 * math.pi) % (2 * math.pi) # Normalize

            # Ray direction components
            ray_dir_x = math.cos(ray_angle)
            ray_dir_y = math.sin(ray_angle)

            # Current map cell the ray is in
            map_x_coord, map_y_coord = int(player_x), int(player_y)

            # Length of ray from current position to next x or y-side
            # delta_dist_x: distance ray travels to cross one x-grid line
            # delta_dist_y: distance ray travels to cross one y-grid line
            delta_dist_x = abs(1 / ray_dir_x) if ray_dir_x != 0 else float('inf')
            delta_dist_y = abs(1 / ray_dir_y) if ray_dir_y != 0 else float('inf')
            
            # step_x/step_y: direction to step in x/y-direction (+1 or -1)
            # side_dist_x/side_dist_y: length of ray from start to first x/y-side
            if ray_dir_x < 0:
                step_x = -1
                side_dist_x = (player_x - map_x_coord) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x_coord + 1.0 - player_x) * delta_dist_x

            if ray_dir_y < 0:
                step_y = -1
                side_dist_y = (player_y - map_y_coord) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y_coord + 1.0 - player_y) * delta_dist_y

            hit = 0  # Wall hit? (0 = no, 1 = yes, or wall type)
            side = 0 # Was a NS or a EW wall hit? (0 for X-side/vertical, 1 for Y-side/horizontal)

            # DDA (Digital Differential Analysis) loop
            # Max steps to prevent infinite loops in case of errors or open maps
            max_dda_steps = game_map.MAP_WIDTH + game_map.MAP_HEIGHT + 5
            current_dda_map_x, current_dda_map_y = map_x_coord, map_y_coord

            for _ in range(max_dda_steps):
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    current_dda_map_x += step_x
                    side = 0 # Hit an X-side (vertical wall)
                else:
                    side_dist_y += delta_dist_y
                    current_dda_map_y += step_y
                    side = 1 # Hit a Y-side (horizontal wall)

                # Check if ray is out of bounds
                if not (0 <= current_dda_map_x < game_map.MAP_WIDTH and 0 <= current_dda_map_y < game_map.MAP_HEIGHT):
                    hit = 0 # No wall hit, ray went out of map
                    break

                if game_map.MAP_DATA[current_dda_map_y][current_dda_map_x] > 0: # Hit a wall
                    hit = game_map.MAP_DATA[current_dda_map_y][current_dda_map_x] # Could be used for different wall types/textures
                    break

            if hit > 0:
                # Calculate Euclidean distance along the ray to the wall
                # The formula (map_coord - player_coord + (1 - step) / 2) / ray_dir_component
                # gives the length of the ray to the wall intersection.
                if side == 0: # Vertical wall hit
                    dist_along_ray = (current_dda_map_x - player_x + (1 - step_x) / 2) / ray_dir_x if ray_dir_x != 0 else float('inf')
                else: # Horizontal wall hit
                    dist_along_ray = (current_dda_map_y - player_y + (1 - step_y) / 2) / ray_dir_y if ray_dir_y != 0 else float('inf')

                # Correct fisheye effect:
                # Project the distance onto the vector perpendicular to the camera plane (view direction).
                # This is done by multiplying the ray's length by cos(angle between ray and player's direction vector).
                # The angle of the current ray relative to the player's direct line of sight:
                relative_ray_angle = ray_angle - player_angle
                # player_angle and ray_angle are normalized, so relative_ray_angle is generally small (within FOV).
                # math.cos will handle the angle correctly.

                projected_dist = dist_along_ray * math.cos(relative_ray_angle)

                # Prevent division by zero or extremely small projected distances (leading to overly tall walls)
                if projected_dist <= 0.001: projected_dist = 0.001

                # Calculate height of the wall slice on screen using the projected distance
                line_height = int(config.SCREEN_HEIGHT / projected_dist)

                # Calculate lowest and highest pixel to fill in current stripe
                draw_start = -line_height / 2 + config.SCREEN_HEIGHT / 2
                if draw_start < 0: draw_start = 0
                draw_end = line_height / 2 + config.SCREEN_HEIGHT / 2
                if draw_end >= config.SCREEN_HEIGHT: draw_end = config.SCREEN_HEIGHT - 1

                # Choose wall color (basic shading based on wall orientation)
                wall_color = config.SHADED_WALL_COLOR if side == 1 else config.BASE_WALL_COLOR

                # Draw the vertical strip representing the wall
                screen_x_pos = i * config.STRIP_WIDTH
                graphics.draw_wall_strip(screen, screen_x_pos, draw_start, draw_end, wall_color)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
