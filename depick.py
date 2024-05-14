import pickle
pickle_in = open("hider_qtable.pickle","rb")
q_table = pickle.load(pickle_in)
print(q_table)