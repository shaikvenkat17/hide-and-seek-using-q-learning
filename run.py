import os
# Importing necessary modules for policy, raycasting, level design, colors, walls, seeker and hider agents, pygame, pickle, and tkinter.

from policy import *
from raycast import *
from level import *
from colors import *
from walls import *
from Seeker import *
from Hider import *
import pygame
import pickle
import pygame.freetype 
import tkinter as tk

# Setting up the display window using tkinter to get screen dimensions.
############################################################################################################################
ro_ot = tk.Tk()
width = ro_ot.winfo_screenwidth()
height = ro_ot.winfo_screenheight()
# Screen_coordinates = (640,480)
si_ze = [width, height]
print(si_ze)
pygame.init()
scr_een = pygame.display.set_mode(si_ze)
os.environ["SDL_VIDEO_CENTERED"] = "0"
pygame.init()

# Defining font styles for the game. 
GAME_FONT = pygame.freetype.Font("font.ttf", 16)
GAME_FONT_LARGE = pygame.freetype.Font("font.ttf", 24)
pygame.display.set_caption("HIDE AND SEEK BY Q-LEARNING")
clock = pygame.time.Clock()
############################################################################################################################

# Parsing the level design.
parse_level(level)

# Initializing variables for episode count and escape flag.
esc = 0
episodes_count = 0
number_of_episodes = 50

# Main loop for running episodes.
while episodes_count < number_of_episodes and esc == 0:

    # Initializing hider and seeker agents.
    hider_no1 = Hider()     
    hider_no2 = Hider()
    hider_no3=Hider()
    seeker_number_1 = Seeker()
    hider_objs = [hider_no1, hider_no2, hider_no3]
    seeker_objs = [seeker_number_1]

    # Setting up variables for the game loop.
    runn_ing = True
    x = 0

    # Game loop for each episode.
    while runn_ing:
        clock.tick(60)

        # Handling events such as quitting, escaping, key presses, and mouse clicks.
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                runn_ing = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                runn_ing = False
                esc = 1
            if e.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    if pov_switch.collidepoint(e.pos):
                        x = (x + 1) % len(agent_lines)
                elif e.button == 3:
                    if pov_switch.collidepoint(e.pos):
                        x = (x - 1) % len(agent_lines)
                        pass
        ############################################################################################################################

        # Getting actions for each hider and seeker agent.
        hider_action_list = []
        for h in hider_objs:
            direction_of_hider, rotation_of_hider = h.agent_hider.get_action()
            h.act(direction_of_hider, rotation_of_hider)
            hider_action_list.append([direction_of_hider, rotation_of_hider])

        action_list_seeker = []
        for s in seeker_objs:
            direction_of_seeker, rotation_of_seeker = s.agent_seeker.get_action()
            s.act(direction_of_seeker, rotation_of_seeker)
            action_list_seeker.append([direction_of_seeker, rotation_of_seeker])

        # Getting coordinates of hiders and seekers. 
        hid_er_cords = get_cords(hider_objs)
        see_ker_cords = get_cords(seeker_objs)

        # Updating hider agents and their rewards based on actions and seeker positions. 
        hider_temp = []
        for h in hider_objs:
            hider_temp = hider_action_list.pop(0)
            direction_of_hider = hider_temp[0]
            hider_reward = h.reward(seeker_objs, see_ker_cords)
            h.agent_hider.update(direction_of_hider, hider_reward)

        # Updating seeker agents and their rewards based on actions and hider positions. 
        temp_seeker = []
        for s in seeker_objs:
            temp_seeker = action_list_seeker.pop(0)
            direction_of_seeker = temp_seeker[0]
            reward_of_seeker, catch = seeker_number_1.reward(hider_objs, hid_er_cords)
            if catch:
                hider_objs.remove(catch)
                del catch
            seeker_number_1.agent_seeker.update(direction_of_seeker, reward_of_seeker)

        
##############################################################
        # Drwaing in the scr_een
        # ... (previous code) ...

        # Filling the screen background with black color.
        scr_een.fill((0, 0, 0))

        # Loading and displaying the floor and sky images.
        floor = pygame.image.load('k.jpg', "r") #floor
        scr_een.blit(floor, (800, 400))
        floor = pygame.image.load('h.jpg', "r") #sky
        scr_een.blit(floor, (800, 0))

        # Drawing the walls on the screen.
        for wall in walls:
            pygame.draw.rect(scr_een, white, wall.rect)

        # Drawing the vision lines for each hider agent in light green color.
        for h in hider_objs:
            for line in h.vision:
                mx, my, px, py = line
                pygame.draw.aaline(scr_een, light_green, (mx, my), (px, py))

        # Drawing the vision lines for the seeker agent in light red color.
        for s in seeker_objs:
            for line in seeker_number_1.vision:
                mx, my, px, py = line
                pygame.draw.aaline(scr_een, light_red, (mx, my), (px, py))

        # Creating a button for switching the point of view.
        pov_switch = pygame.draw.rect(scr_een, (45, 43, 23), pygame.Rect(20, 780, 180, 100))
        eye = pygame.image.load('b.jpg', "r")
        scr_een.blit(eye, (20, 780))

        # Displaying the total number of games completed.
        text_surface, rect = GAME_FONT.render(f"Total Number of Games Completed  = {episodes_count}", white)
        scr_een.blit(text_surface, (350, 818))

        # Displaying the rewards for each hider agent.
        temp = 0
        for h in hider_objs:
            text_surface, rect = GAME_FONT.render(f" Green player Hider Rewards are {str(h.agent_hider.total_reward)[:6]}", light_green)
            scr_een.blit(text_surface, (700, 815+ temp))
            temp += 20

        # Displaying the rewards for the seeker agent.
        for s in seeker_objs:
            text_surface, rect = GAME_FONT.render(f" Red player Seeker Rewards are {str(s.agent_seeker.total_reward)[:6]}", cyan)
            scr_een.blit(text_surface, (1000, 818))

        # Drawing the rectangles for each hider and seeker agent.
        for h in hider_objs:
            pygame.draw.rect(scr_een, forest_green, h.rect)
        for s in seeker_objs:
            pygame.draw.rect(scr_een, red, s.rect)

        # Getting the lines for raycasting from the seeker's perspective.
        agent_lines = []
        # for h in hider_objs:
        #     h_lines = Raycast(h).get_lines()
        #     agent_lines.append(h_lines)
        # If you want to view the hiders view then uncomment above code and comment the seeker code below
        for s in seeker_objs:
            s_lines = Raycast(s).get_lines()
            agent_lines.append(s_lines)

        # Drawing the lines based on raycasting results with different colors for different orientations.
        px = 0
        color = (3, 73, 252)
        for l in agent_lines[x]:
            if l['orientation'] == 'v':
                color = (168, 168, 168)
            elif l['orientation'] == 'h':
                color = (107, 107, 107)
            elif l['orientation'] == 'e': 
                color = (0, 0, 0)
            elif l['orientation'] == 'i':
                px += 4
                pass

            pygame.draw.line(scr_een, color, (800 + px, 400 + l['length'] / 2),
                                (800 + px, 400 - l['length'] + l['length'] / 2), width=3)
            px += 2
            pygame.draw.line(scr_een, (0, 0, 0), (800 + px, 400 + l['length'] / 2),
                                (800 + px, 400 - l['length'] + l['length'] / 2), width=1)
            px += 2

        # Updating game state and episode count. 
        if seeker_number_1.game_no == seeker_number_1.game_prevno + 1:
            seeker_number_1.game_prevno = seeker_number_1.game_no
        if not hider_objs:
            episodes_count += 1
            runn_ing = False

        # Saving Q-tables for hiders and seekers after all episodes are completed. 
        if episodes_count == number_of_episodes:
            for s in seeker_objs:
                pickle_s = open("seeker_qtable.pickle", "wb")
                pickle.dump(s.agent_seeker.q_table, pickle_s)
                pickle_s.close()
            for h in hider_objs:
                pickle_h = open("hider_qtable.pickle", "wb")
                pickle.dump(h.agent_hider.q_table, pickle_h)
                pickle_h.close()
            print("Pickle updated")

        # Updating the display.
        pygame.display.flip()