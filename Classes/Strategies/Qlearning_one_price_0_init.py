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
        
        action_profit_sums = {action: 0 for action in action_space}
        action_counter = len(state_space)/len(action_space)

        for state in state_space:
            action = state_space[state].actions[firmindex]
            firmprofit = state_space[state].firm_profits[firmindex]

            action_profit_sums[action] += firmprofit

        # Redefine action_space

        unzipped_action_spaces = list(zip(*action_space))
        unzipped_action_spaces = [sorted(list(set(actions))) for actions in unzipped_action_spaces]

        action_space = [tuple([actions[i] for actions in unzipped_action_spaces]) for i in range(len(unzipped_action_spaces[0]))]


        initial_Q_values = {action: 0 for action in action_space}

        self.Q = {state : {action : initial_Q_values[action] for action in action_space} for state in state_space}

        value_dict = {}
        for k, v in initial_Q_values.items():
            if v in value_dict:
                value_dict[v] += (k,)
            else:
                value_dict[v] = (k,)

        self.Q_values = {state: SortedDict(value_dict) for state in state_space}

