import numpy as np


class Qlearning():
    '''
    Takes state space, action space, reward function, discount factor, learning rate, exploration rate, and initial Q values
    '''
    def __init__(self, state_space, action_space, reward_function, discount_factor, learning_rate, exploration_rate, initial_Q):
        self.state_space = state_space
        self.action_space = action_space
        self.reward_function = reward_function
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.Q = initial_Q

    def get_action(self, state):
        '''
        Takes state
        Gives action
        '''
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(self.action_space)
        else:
            return np.argmax(self.Q[state])


    def update_Q(self, state, action, next_state):
        '''
        Takes state, action, next state
        Updates Q values
        '''
        
        reward = self.reward_function(state, action, next_state)

        self.Q[state, action] = (1 - self.learning_rate) * self.Q[state, action] + self.learning_rate * (reward + self.discount_factor * np.max(self.Q[next_state]))
