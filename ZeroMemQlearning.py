import numpy as np


class ZeroMemQlearning():
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


        for action in action_space:
            self.Q[action] = 0.0

    
    def get_action(self, state):
        '''
        Takes state
        Gives action
        '''
        explore = self.exploration_rate(state.t)

        if np.random.uniform(0, 1) < explore:
            index = np.random.randint(0,len(self.Q.keys())-1)
            action = list(self.Q.keys())[index]
            
            return action
        else:
            best_actions = []

            max_val = max(self.Q.values())

            for action in self.Q.keys():
                if self.Q[action] == max_val:
                    best_actions.append(action)

            if len(best_actions) == 1:
                return best_actions[0]
            else:
                index = np.random.randint(0,len(best_actions)-1)
                return best_actions[index]


    def update_strategy(self, state, action, next_state, profit):
        '''
        Takes state, action, next state
        Updates Q values
        '''
        
        self.Q[action] = (1 - self.learning_rate) * self.Q[action] + self.learning_rate * (profit + self.discount_factor * self.Q[self.get_action(next_state)])
