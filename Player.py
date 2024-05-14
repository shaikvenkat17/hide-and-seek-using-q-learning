from raycast import Raycast
import math
from walls import *
from vision import Vision, point_rotation

# Player class represents a general player in the game (base class for Hider and Seeker)
class Player():
    def __init__(self):
        rect = pygame.Rect(0, 0, 32, 32)  # Create a rectangle representing the player
        rect.center = (128, 128)  # Set the initial position
        self.rect = rect
        self.angle = 0  # Angle of orientation (not used in the provided code)
        self.checkwalls(850)  # Find nearby walls within a radius
        self.orientation = 0  # Discrete orientation (e.g., 0: up, 1: right, 2: down, 3: left)
        self.movement_type = [1, 3][0]  # Not used in the provided code
        self.dist_covered = 0  # Distance covered from the starting point
        self.vision = Vision(45,180,50).get_lines(self.rect.center, self.near_walls, self.orientation)  
        # Get lines representing the player's field of view
        self.render = Vision(45,1000,200).get_lines(self.rect.center, self.near_walls, self.angle)
        # Get lines for rendering the field of view (longer range)

    def move_axis(self, dx, dy):
        # Move the player along both x and y axes, checking for collisions
        self.move_single_axis(dx, dy)

    def move_single_axis(self, dx, dy):
        # Move the player along one axis at a time, handling collisions
        dx1, dy1 = dx, dy  # Not used in the provided code
        self.rect.x += dx  # Move horizontally
        self.rect.y += dy  # Move vertically

        # Check for collisions with walls
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; adjust position to avoid overlapping the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; adjust position
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; adjust position
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; adjust position
                    self.rect.top = wall.rect.bottom
        self.checkwalls(850)  # Update nearby walls after moving
        self.vision = Vision(45,180,50).get_lines(self.rect.center, self.near_walls, self.angle)  
        # Update field of view lines
        self.render = Vision(45,1000,200).get_lines(self.rect.center, self.near_walls, self.angle)
        # Update rendering lines

    def get_state(self):
        # Get the current state representation for the player
        head_position = (self.rect.x, self.rect.y)  # Player's position
        wall_info = tuple(self.is_wall_nearby().values())  # Information about nearby walls

        # Concatenate the position and wall information into a single state tuple
        return head_position + wall_info

    def is_wall_nearby(self):
        # Check for walls in each direction
        left, right, up, down = False, False, False, False
        dx = self.rect.x - 32  # Not used in the provided code
        dy = self.rect.y - 32  # Not used in the provided code

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; wall is to the left
                    left = "True"
                if dx < 0:  # Moving left; wall is to the right 
                    right = "True"
                if dy > 0:  # Moving down; wall is above
                    down = "True"
                if dy < 0:  # Moving up; wall is below
                    up = "True"
        return {
            "LEFT": left,
            "RIGHT": right,
            "UP": up,
            "DOWN": down
        }
    
  

    def act(self, direction, rotation):
        # Take an action based on the given direction and rotation
        is_boundary = self.is_wall_nearby()  # Check for walls
        if is_boundary[direction]:  # If there's a wall in the intended direction, do nothing
            pass
        else:
            self.move(direction, rotation)  # Otherwise, move in the specified direction

    def move(self, direction, rotation):
        # Move the player based on the direction and rotate if necessary
        if direction == "LEFT":
            self.move_axis(-25, 0)  # Move left
        if direction == "RIGHT":
            self.move_axis(25, 0)  # Move right
        if direction == "UP":
            self.move_axis(0, -25)  # Move up
        if direction == "DOWN":
            self.move_axis(0, 25)  # Move down

        if rotation == "l_rot":
            # Rotate left
            self.angle = (self.angle + 1) % 360  # Update angle (not used in the provided code)
            self.orientation = (self.orientation + 1) % 4  # Update discrete orientation
            self.vision = Vision(45,180,50).get_lines(self.rect.center, self.near_walls, self.angle)  # Update field of view
            Raycast(self).x_or_y()  # Not defined in the provided code, assumably related to raycasting for vision

        if rotation == "r_rot":
            # Rotate right
            self.angle = (self.angle - 1) % 360  # Update angle 
            self.orientation = (self.orientation - 1) % 4  # Update discrete orientation
            self.vision = Vision(45,180,50).get_lines(self.rect.center, self.near_walls, self.angle)  # Update field of view
            Raycast(self).x_or_y()  # Assumably related to raycasting

    def checkwalls(self, radius):  
        # Find nearby walls within a given radius from the player
        self.near_walls = []
        for wall in walls:
            if math.dist(self.rect.center, wall.rect.center) <= radius:
                self.near_walls.append(wall)
        pass  # No explicit return value, but the method updates self.near_walls