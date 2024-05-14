import random
import math

def to_normal(point, height=500):
    """
    Converts a point from Cartesian coordinates to screen coordinates (y-axis inverted).

    Args:
        point (tuple): A tuple representing the x and y coordinates of the point.
        height (int, optional): The height of the screen. Defaults to 500.

    Returns:
        tuple: A tuple representing the x and y coordinates in screen coordinates.
    """
    return point[0], height - point[1]

def create_points(theta, radius, density):
    """
    Generates a list of poi_nts evenly spaced around a circle. 

    Args:
        theta (float): The total angle to cover (in degrees).
        radius (float): The radius of the circle.
        density (float): The number of poi_nts per degree.

    Returns:
        list: A list of tuples representing the x and y coordinates of the poi_nts.
    """
    poi_nts = []
    current_angle = 0
    while current_angle < theta:
        poi_nts.append((radius * math.cos(math.radians(current_angle)), radius * math.sin(math.radians(current_angle))))
        current_angle += theta / density
    return poi_nts

def point_translation(origin, end_points):
    """
    Translates a point by adding the origin coordinates.

    Args:
        origin (tuple): A tuple representing the x and y coordinates of the origin.
        end_points (tuple): A tuple representing the x and y coordinates of the point to translate.

    Returns:
        tuple: A tuple representing the translated point's coordinates.
    """
    origin_x, origin_y = origin
    end_point_x, end_point_y = end_points
    return end_point_x + origin_x, end_point_y + origin_y

def point_rotation(origin, point, angle):
    """
    Rotates a point around an origin by a given angle.

    Args:
        origin (tuple): A tuple representing the x and y coordinates of the rotation origin.
        point (tuple): A tuple representing the x and y coordinates of the point to rotate.
        angle (float): The angle of rotation (in degrees).

    Returns:
        tuple: A tuple representing the rotated point's coordinates. 
    """
    origin_x, origin_y = to_normal(origin)
    point_x, point_y = to_normal(point)
    angle = math.radians(angle)
    rotated_x = origin_x + math.cos(angle) * (point_x - origin_x) - math.sin(angle) * (point_y - origin_y)
    rotated_y = origin_y + math.sin(angle) * (point_x - origin_x) + math.cos(angle) * (point_y - origin_y)
    return to_normal((rotated_x, rotated_y))

walls = []  # List to store wall objects (assuming wall class exists)

class Vision:
    """
    Class for handling vision calculations and generating vision lines. 
    """
    def __init__(self, vision_angle, vision_radius, vision_density):
        self.vision_angle = vision_angle
        self.vision_radius = vision_radius 
        self.vision_density = vision_density 
        self.position = (0, 0) 
        self.walls = []  # List to store wall objects within vision range

    def get_lines(self, position, walls, angle):
        """
        Generates vision lines based on the player's position, nearby walls, and viewing angle. 

        Args:
            position (tuple): The player's current position (x, y). 
            walls (list): A list of wall objects within vision range.
            angle (float): The player's viewing angle.

        Returns:
            list: A list of tuples, each representing a vision line with starting and ending coordinates. 
        """
        self.vision_lines = []
        for point in create_points(self.vision_angle, self.vision_radius, self.vision_density):
            player_x, player_y = position
            point = point_translation((player_x, player_y), point)  # Translate point relative to player
            point = point_rotation((player_x, player_y), point, self.vision_angle / 2)  # Rotate point based on vision angle 
            point = point_rotation((player_x, player_y), point, angle)  # Rotate based on player's viewing angle
            vision_line_end_x, vision_line_end_y = point
            vision_line = (player_x, player_y, vision_line_end_x, vision_line_end_y)

            # Check for intersections with walls and clip the vision line accordingly
            for wall in walls:
                clipped_line = wall.rect.clipline(vision_line)
                if clipped_line:
                    start_point, end_point = clipped_line
                    x1, y1 = start_point
                    vision_line = (player_x, player_y, x1, y1)

            self.vision_lines.append(vision_line)
        return self.vision_lines

    def get_intersect(self, position, walls, angle):
        """
        Calculates the intersection poi_nts of vision lines with walls. 

        Args:
            position (tuple): The player's current position (x, y).
            walls (list): A list of wall objects within vision range.
            angle (float): The player's viewing angle. 

        Returns:
            tuple: A tuple containing two lists: starting poi_nts of vision lines and their corresponding intersection poi_nts.
        """
        self.vision_line_start_points = []
        self.vision_line_end_points = []
        for point in create_points(self.vision_angle, self.vision_radius, self.vision_density):
            player_x, player_y = position
            point = point_translation((player_x, player_y), point) 
            point = point_rotation((player_x, player_y), point, self.vision_angle / 2) 
            point = point_rotation((player_x, player_y), point, angle)
            vision_line_end_x, vision_line_end_y = point
            vision_line = (player_x, player_y, vision_line_end_x, vision_line_end_y)
            start_line_point = (player_x, player_y)
            self.vision_line_start_points.append(start_line_point)
            end_line_point = (vision_line_end_x, vision_line_end_y)

            # Find the intersection point with the nearest wall 

            for wall in walls:
                clipped_line = wall.rect.clipline(vision_line)
                if clipped_line:
                    start_point, end_point = clipped_line
                    intersection_x, intersection_y = start_point
                    end_line_point = (intersection_x, intersection_y)

            self.vision_line_end_points.append(end_line_point)
        return self.vision_line_start_points, self.vision_line_end_points
    pass