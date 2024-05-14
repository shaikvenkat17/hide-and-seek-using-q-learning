import random
import numpy
import operator

# Define possible actions and rotations for the agent
valid_action = ["LEFT", "RIGHT", "UP", "DOWN"]  
rot = ["r_rot", "l_rot"]

# Set the size of each grid cell in the environment (assuming a grid-based environment)
block_size = 32  

# Define the Policy class for the reinforcement learning agent
class Policy(object):
    # for all players

    def __init__(self, player):
        self.player = player  # Reference to the agent using this policy
        self.q_table = {}  # Stores Q-values for state-action pairs (key component of Q-learning)
        self.reward = 0  # Current reward obtained
        self.alpha = 0.3  # Learning rate (how much new information influences Q-values)
        self.gamma = 0.1  # Discount factor (values future rewards less than immediate ones)
        self.epsilon = 0.1  # Exploration rate (probability of choosing a random action)
        self.penalties = []  # List to store penalties (not used in the provided code)
        self.total_reward = 0.0  # Accumulated reward over time
        self.counts = 0.0  # Not used in the provided code


    def reset(self):
        self.reward = 0  # Reset the current reward at the beginning of each episode

    def get_action(self):
        max_q = 0  # Not used in the provided code
        self.state_unformatted = self.player.get_state()  # Get the agent's current state (e.g., position)
        self.curr_distance = self.player.distance()  # Calculate the distance from the starting point
        self.state = (
        self.state_unformatted[0], self.state_unformatted[1], round(self.curr_distance, 3), round(self.total_reward, 3))
        # Create a state representation using x, y, distance, and total reward


        if not self.state in self.q_table:
            self.q_table[self.state] = {ac: 0 for ac in valid_action}  
            # Initialize Q-values for a new state (all actions start with 0 value)
            print(self.q_table)

        action = random.choice(valid_action)  # Initially choose a random action
        rotation = random.choice(rot)  # Choose a random rotation

        # Exploration vs. exploitation
        if numpy.random.random() > self.epsilon:  # Exploit: choose the action with the highest Q-value
            if len(set(self.q_table[self.state].values())) == 1:  # If all actions have the same value, choose randomly
                pass
            else:
                action = max(self.q_table[self.state].items(), key=operator.itemgetter(1))[0]
                # Choose the action with the maximum Q-value
                print(action)
        return action, rotation  # Return the chosen action and rotation

    def update(self, action, reward):
        self.total_reward += reward  # Update the total reward
        print(self.total_reward)

        self.next_state_unformatted = self.player.get_state()  # Get the next state after taking the action
        self.curr_distance = self.player.distance()  # Calculate the new distance from the starting point
        self.next_state = (self.next_state_unformatted[0], self.next_state_unformatted[1], round(self.curr_distance, 3),
                           round(self.total_reward, 3))
        # Create a state representation for the next state

        if self.next_state not in self.q_table:
            self.q_table[self.next_state] = {ac: 0 for ac in valid_action}  
            # Initialize Q-values for the next state if it's not already in the Q-table 

        old_q_value = self.q_table[self.state][action]  # Get the Q-value for the current state-action pair

        next_max = max(self.q_table[self.next_state].values())  # Get the maximum Q-value for the next state

        new_q_value = (1 - self.alpha) * old_q_value + self.alpha * (
                reward + self.gamma * next_max)  
        # Update the Q-value using the Q-learning formula

        self.q_table[self.state][action] = new_q_value  # Update the Q-table with the new Q-value
        print("Agent.update(): state = {}".format(self.state)) 