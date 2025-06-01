import numpy as np
import random
from sortedcontainers import SortedDict
import Classes.Strategies.Qlearning


class Qlearning(Classes.Strategies.Qlearning.Qlearning):
    '''
    Takes discount factor, learning rate, exploration rate
    '''

    def initialize(self, state_space, action_space, firmindex):
        '''
        Initializes strategy
        '''
        

        initial_Q_values = {action: 0 for action in action_space}

        self.Q = {state : {action : initial_Q_values[action] for action in action_space} for state in state_space}

        value_dict = {}
        for k, v in initial_Q_values.items():
            if v in value_dict:
                value_dict[v] += (k,)
            else:
                value_dict[v] = (k,)

        self.Q_values = {state: SortedDict(value_dict) for state in state_space}

