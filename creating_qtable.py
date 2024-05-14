

import pickle

# Initialize an empty dictionary to represent the Q-table
q_tab = {} 

# Open a file for writing in binary mode to store the seeker's Q-table
pickle_seeker = open("seeker_qtable.pickle", "wb")

# Dump the Q-table dictionary into the pickle file for the seeker
pickle.dump(q_tab, pickle_seeker)

# Close the seeker's pickle file
pickle_seeker.close()

# Open a file for writing in binary mode to store the hider's Q-table
pickle_hider = open("hider_qtable.pickle", "wb")

# Dump the Q-table dictionary (same as seeker) into the pickle file for the hider
pickle.dump(q_tab, pickle_hider) 

# Close the hider's pickle file
pickle_hider.close()