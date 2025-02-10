import numpy as np


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
        self.action_space = action_space
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
        if np.random.uniform(0, 1) < self.exploration_rate(state.t):
            index = np.random.randint(0,len(self.Q[state.state].keys())-1)
            return list(self.Q[state.state].keys())[index]
        else:
            best_actions = []

            max_val = np.max(self.Q[state.state].values())

            for action in self.Q[state.state].keys():
                if self.Q[state.state][action] == max_val:
                    best_actions.append(action)

            return np.random.choice(best_actions)


    def update_strategy(self, state, action, next_state, profit):
        '''
        Takes state, action, next state
        Updates Q values
        '''
        
        self.Q[state.state][action] = (1 - self.learning_rate) * self.Q[state.state][action] + self.learning_rate * (profit + self.discount_factor * self.Q[next_state.state][self.get_action(next_state)])
