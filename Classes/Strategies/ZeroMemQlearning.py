import numpy as np
import random


class ZeroMemQlearning():
    '''
    Takes state space, action space, reward function, discount factor, learning rate, exploration rate, and initial Q values
    '''
    def __init__(self, discount_factor, learning_rate, exploration_rate):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.action_space = None
        self.Q = None


    def initialize(self, state_space, action_space, firmindex):
        '''
        Initializes strategy
        '''
        self.Q = {}

        for action in action_space:
            self.Q[action] = 0.0

    
    def get_action(self, state, t):
        '''
        Takes state
        Gives action
        '''
        explore = self.exploration_rate(t)

        if np.random.uniform(0, 1) < explore:
            action = random.choice(list(self.Q.keys()))
            
            return action
        else:
            max_val = max(self.Q.values())

            best_actions = [action for action, value in self.Q.items() if value == max_val]
            
            return random.choice(best_actions)


    def update_strategy(self, state, action, next_state, profit):
        '''
        Takes state, action, next state
        Updates Q values
        '''
        next_max_val = max(self.Q.values())
        self.Q[action] = (1 - self.learning_rate) * self.Q[action] + self.learning_rate * (profit + self.discount_factor * next_max_val)
