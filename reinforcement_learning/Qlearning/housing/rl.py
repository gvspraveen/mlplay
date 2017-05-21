# Simple Q learning implementation for learning a path from a random room to outside the house
# Based of : http://mnemstudio.org/path-finding-q-learning-tutorial.htm

from random import randint
import sys

# Hyper parameters
gamma = 0.9
epochs = 10000
print_progress_every = 100

# Inital State for prediction phase
initial_state = 0

# DONT MODIFY THIS
goal_state = 5

R = [
    [-1, -1, -1, -1, 0, -1],
    [-1, -1, -1, 0, -1, 100],
    [-1, -1, -1, 0, -1, -1],
    [-1, 0, 0, -1, 0, -1],
    [0, -1, -1, 0, -1, 100],
    [-1, 0, -1, -1, 0, 100],
]

Q = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

def print_no_newline(string):
    sys.stdout.write(string)
    sys.stdout.flush()

def next_possible_action(curr_state):
    all_actions = get_all_possible_actions(curr_state)
    ran = randint(0, len(all_actions)-1)
    return all_actions[ran]

def get_all_possible_actions(state):
    size = len(R[state])
    # Get all possible actions for current state (possible action is column number in current row where reward is not -1)
    return [index for index in range(size) if R[state][index] != -1]

# Learn method
def learn():
    for epoch in range(epochs):

        if epoch % print_progress_every == 0:
            print_no_newline(".")

        state = randint(0, len(R)-1)

        while True:
            next_action = next_possible_action(state)
            all_actions_for_next_index = get_all_possible_actions(next_action)

            max_action_index = -1

            for nai in all_actions_for_next_index:
                if max_action_index == -1:
                    max_action_index = nai
                elif Q[next_action][nai] > Q[next_action][max_action_index]:
                    max_action_index = nai

            Q[state][next_action] = R[state][next_action] + gamma * Q[next_action][max_action_index]
            state = next_action
            if state == len(R)-1:
                break

# Predict Path
def predict(initial_state):
    next_state = initial_state
    states = [str(initial_state)]
    while next_state != goal_state:
        # Find max action with highest Q reward
        reward = -sys.maxint - 1
        action = -1
        num_actions = len(Q[next_state])

        for action_index in range(num_actions):
            if Q[next_state][action_index] > reward:
                action = action_index
                reward = Q[next_state][action_index]

        next_state = action
        states.append(str(next_state))
        # print next_state, ": ", reward

    return states

if __name__ == '__main__':
    learn()
    print "\n######################### Learning ###################\n\n"
    for row in Q:
        print row

    print "\n######################### Predict Path from {} to {} ###################\n\n".format(initial_state, goal_state)
    states = predict(initial_state)
    print "Predicted path :"
    print "->".join(states)
