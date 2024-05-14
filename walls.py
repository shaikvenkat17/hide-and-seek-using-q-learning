import pygame

walls = []  # List to store all Wall objects

class Wall(object):
    def __init__(self, pos):
        walls.append(self)  # Add newly created wall to the global list
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)  # Create a Rect object for the wall

# Parse the level string. W = wall, E = exit
def parse_level(level):
    x = y = 0  # Initialize x and y coordinates
    for row in level:  # Iterate over each row in the level string
        for col in row:  # Iterate over each character in the row
            if col == "W":
                Wall((x, y))  # Create a Wall object at the current position
            if col == "E":
                end_rect = pygame.Rect(x, y, 32, 32)  # Create a Rect object for the exit
            x += 32  # Move to the next column
        y += 32  # Move to the next row
        x = 0  # Reset x to the beginning of the row

# Get coordinates of a list of objects with 'rect' attribute
def get_cords(objects):
    colist = []  # Initialize a list to store coordinates
    for i in objects:
        ll = (i.rect.x, i.rect.y)  # Get the x and y coordinates of the object's rect
        colist.append(ll)  # Add the coordinates to the list
    return colist

# Rotate an image around its center
def rot_center(image, rect, angle):
    # Rotate the image by the given angle
    rotattion_image = pygame.transform.rotate(image, angle)
    # Get a new Rect object with the center at the same position as the original rect
    rotation_rect = rotattion_image.get_rect(center=rect.center)
    return rotattion_image, rotation_rect  # Return the rotated image and its rect