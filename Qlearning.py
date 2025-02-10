import numpy as np
import random


class Qlearning():
    '''
    Takes state space, action space, reward function, discount factor, learning rate, exploration rate, and initial Q values
    '''
    def __init__(self, discount_factor, learning_rate, exploration_rate):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.Q = None


    def initialize(self, state_space, action_space):
        '''
        Initializes strategy
        '''
        self.Q = {}

        for state in state_space:
            self.Q[state] = {}
            for action in action_space:
                self.Q[state][action] = 0.0

    
    def get_action(self, state):
        '''
        Takes state
        Gives action
        '''
        explore = self.exploration_rate(state.t)

        if np.random.uniform(0, 1) < explore:
            action = random.choice(list(self.Q[state.prices].keys()))
            
            return action
        else:
            return self.best_action(state)
        
    def best_action(self, state):
        best_actions = []

        max_val = max(self.Q[state.prices].values())

        for action in self.Q[state.prices].keys():
            if self.Q[state.prices][action] == max_val:
                best_actions.append(action)

        return random.choice(best_actions)


    def update_strategy(self, state, action, next_state, profit):
        '''
        Takes state, action, next state
        Updates Q values
        '''
        
        self.Q[state.prices][action] = (1 - self.learning_rate) * self.Q[state.prices][action] + self.learning_rate * (profit + self.discount_factor * self.Q[next_state.prices][self.best_action(next_state)])
