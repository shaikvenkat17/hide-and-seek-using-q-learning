from Player import *
import random
import math
from policy import *
import pickle


# Hider class inheriting from Player class
class Hider(Player):
    initial_positions = [(128, 128), (600, 128), (500, 100), (400, 200), (128, 240)]  # Possible starting positions

    def __init__(self):
        # super().__init__()
        rect = pygame.Rect(0, 0, 32, 32)  # Create a rectangle representing the hider
        rect.center = random.choice(Hider.initial_positions)  # Choose a random starting position
        self.rect = rect
        self.original_cords = [self.rect.x, self.rect.y]  # Store the initial position for distance calculations
        self.angle = 0  # Not used in the provided code
        self.checkwalls(850)  # Not defined in the provided code (assumably checks for wall proximity)
        self.orientation = 0  # Represents the hider's orientation (e.g., facing direction)
        self.movement_type = [1, 3][0]  # Not used in the provided code
        self.dist_covered = 0  # Distance covered from the starting point
        self.agent_hider = Policy(self)  # Create a Policy object for the hider (Q-learning agent)
        hider_pickle = open("hider_qtable.pickle","rb")  # Load a pre-trained Q-table from a pickle file
        self.agent_hider.q_table=pickle.load(hider_pickle)

    def distance_reward(self, seeker_cords):
        # Calculate the reward based on the distance from the seeker
        x = self.rect.x
        y = self.rect.y
        for i in seeker_cords:
            x1 = [x, y]
            x2 = [i[0], i[1]]
            dist = math.dist(x1, x2)  # Calculate the Euclidean distance
            if dist > 100:
                return dist / 1000  # Positive reward for being farther away
            else:
                return -0.01  # Negative reward for being closer

    def area_coverage(self):
        # Reward for covering more area (exploring the environment)
        self.dist_covered = self.distance()  # Calculate the distance from the starting point
        if self.dist_covered < 100:
            coverage_reward = - self.dist_covered / 1000  # Small penalty for not moving much
        else:
            coverage_reward = self.dist_covered / 1000  # Positive reward for covering more ground
        return coverage_reward

    def distance(self):
        # Calculate the Euclidean distance from the starting point
        x1 = self.original_cords
        x2 = [self.rect.x, self.rect.y]
        self.dist_covered = math.dist(x1, x2)
        return self.dist_covered

    def wall_collision(self):
        # Penalize collisions with walls
        wallinfo = self.is_wall_nearby()  # Not defined in the provided code, assumed to return wall proximity information
        wall_reward = 0
        for key in wallinfo:
            if wallinfo[key]:
                wall_reward = -0.001  # Penalty for being near a wall
        return wall_reward

    def reward(self, seeker_objs, seeker_cords):
        # Calculate the overall reward for the hider
        reward = -1  # Default negative reward
        co_list = []  # Not used in the provided code
        flag = 0  # Not used in the provided code

        # Vision-related code (not fully implemented in the provided snippet)
        self.v_startpoints, self.v_endpoints = Vision(45,180,50).get_intersect(self.rect.center, self.near_walls,
                                                                      self.orientation)

        seek_rew=0  # Reward related to seeker visibility
        for s in seeker_objs:
            for line in self.vision: 
                start = s.rect.clipline(line)  # Check if the seeker is within the hider's vision
                if start:
                    seek_rew = seek_rew -200  # Large penalty for seeing the seeker
                    print("Seeker at 12 , run away ", seek_rew)
                    break
        reward = seek_rew 

        reward += self.distance_reward(seeker_cords)  # Add distance-based reward
        reward += self.area_coverage()  # Add area coverage reward 
        reward += self.wall_collision()  # Add wall collision penalty
        return reward