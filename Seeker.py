from Player import *
import random
import math
import pickle
from policy import *

# Seeker class inheriting from Player class
class Seeker(Player):
    initial_positions = [(280, 250), (400, 400), (250, 300), (500, 100), (620, 450)]  # Possible starting positions

    def __init__(self):
        # super().__init__()
        rect = pygame.Rect(0, 0, 32, 32)  # Create a rectangle representing the seeker
        rect.center = random.choice(Seeker.initial_positions)  # Choose a random starting position
        self.rect = rect
        self.original_cords = [self.rect.x, self.rect.y]  # Store the initial position for distance calculations
        self.angle = 0  # Not used in the provided code
        self.checkwalls(850)  # Not defined in the provided code (assumably checks for wall proximity)
        self.orientation = 0  # Represents the seeker's orientation (e.g., facing direction)
        self.movement_type = [1, 3][0]  # Not used in the provided code
        self.game_no = 0  # Tracks the number of games played (or rounds)
        self.game_prevno = 0  # Tracks the previous game number
        self.dist_covered = 0  # Distance covered from the starting point
        self.agent_seeker = Policy(self)  # Create a Policy object for the seeker (Q-learning agent)
        seeker_pickle = open("seeker_qtable.pickle","rb")  # Load a pre-trained Q-table from a pickle file
        self.agent_seeker.q_table=pickle.load(seeker_pickle)

    def distance_reward(self, hider_cords):
        # Calculate the reward based on the distance from the hider
        x = self.rect.x
        y = self.rect.y
        for i in hider_cords:
            x1 = [x, y]
            x2 = [i[0], i[1]]
            dist = math.dist(x1, x2)  # Calculate the Euclidean distance
            if dist > 100:
                return -0.01  # Small penalty for being far away
            else:
                return dist / 1000  # Positive reward for being closer

    def distance(self):
        # Calculate the Euclidean distance from the starting point
        x1 = self.original_cords
        x2 = [self.rect.x, self.rect.y]
        self.dist_covered = math.dist(x1, x2)
        return self.dist_covered

    def area_coverage(self):
        # Reward for covering more area (exploring the environment)
        self.dist_covered = self.distance()
        if self.dist_covered < 100:
            coverage_reward = - self.dist_covered / 1000  # Small penalty for not moving much
        else:
            coverage_reward = self.dist_covered / 1000  # Positive reward for covering more ground
        return coverage_reward

    def wall_collision(self):
        # Penalize collisions with walls
        wall_info = self.is_wall_nearby()  # Not defined in the provided code, assumed to return wall proximity information
        wall_reward = 0
        for key in wall_info:
            if wall_info[key]:
                wall_reward = -0.001  # Penalty for being near a wall
        return wall_reward

    def reward(self, hider_objs, hider_cords):
        # Calculate the overall reward for the seeker
        reward = -1  # Default negative reward
        co_list = []  # Not used in the provided code
        
        # Vision-related code (not fully implemented in the provided snippet)
        self.v_startpoints, self.v_endpoints = Vision(45,180,50).get_intersect(self.rect.center, self.near_walls,
                                                                      self.orientation)

        loser_hider = 0  # Not used in the provided code
        seek_rew = 0  # Reward related to finding the hider
        for h in hider_objs:
            for line in self.vision: 
                start = h.rect.clipline(line)  # Check if the hider is within the seeker's vision
                if start:
                    seek_rew = seek_rew + 1000  # Large reward for finding the hider
                    print("hey, they collided!!!!!!!!!!! ", seek_rew)
                    loser_hider = h  # Identify the found hider
                    self.game_prevno = self.game_no
                    self.game_no += 1  # Increment the game counter
                    break
        reward = seek_rew 

        reward += self.distance_reward(hider_cords)  # Add distance-based reward 
        reward += self.area_coverage()  # Add area coverage reward
        reward += self.wall_collision()  # Add wall collision penalty
        # print(reward)
        return reward, loser_hider  # Return the reward and the found hider (if any)