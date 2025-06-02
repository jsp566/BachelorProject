import numpy as np
import random
from sortedcontainers import SortedDict


class Qlearning():
    '''
    Takes discount factor, learning rate, exploration rate
    '''
    def __init__(self, discount_factor, learning_rate, exploration_rate):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate

        self.Q = None
        self.Q_values = None


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

        initial_Q_values = {action: (action_profit_sums[action]) / ((1 - self.discount_factor) * action_counter) for action in action_space}

        self.Q = {state : {action : initial_Q_values[action] for action in action_space} for state in state_space}

        value_dict = {}
        for k, v in initial_Q_values.items():
            if v in value_dict:
                value_dict[v] += (k,)
            else:
                value_dict[v] = (k,)

        self.Q_values = {state: SortedDict(value_dict) for state in state_space}

    def get_action(self, state, t):
        '''
        Takes state
        Gives action
        '''
        explore = self.exploration_rate(t)

        if state is None:
            state = random.choice(list(self.Q.keys()))
        else:
            state = state.p
            
        if np.random.uniform(0, 1) < explore:
            action = random.choice(list(self.Q[state].keys()))
            
        else:
            action = self.best_action(state)

        return action
    
    def best_action(self, state):
        maxval, actions = self.Q_values[state].peekitem(-1)
        return random.choice(actions)

    def update_strategy(self, state, action, next_state, profit):
        '''
        Takes state, action, next state
        Updates Q values
        '''
        next_state_max_val, actions = self.Q_values[next_state.p].peekitem(-1)
        
        new_Q_val = (1 - self.learning_rate) * self.Q[state.p][action] + self.learning_rate * (profit + self.discount_factor * next_state_max_val)

        old_Q_val = self.Q[state.p][action]


        old_state_max_val, old_max_actions = self.Q_values[state.p].peekitem(-1)

        self.Q[state.p][action] = new_Q_val

        if len(self.Q_values[state.p][old_Q_val]) > 1:
            self.Q_values[state.p][old_Q_val] = tuple(k for k in self.Q_values[state.p][old_Q_val] if k != action)
        else:
            del self.Q_values[state.p][old_Q_val]

        if new_Q_val in self.Q_values[state.p]:
            self.Q_values[state.p][new_Q_val] += (action,)
        else:
            self.Q_values[state.p][new_Q_val] = (action,)

        new_state_max_val, new_max_actions = self.Q_values[state.p].peekitem(-1)

        update_to_best = old_max_actions != new_max_actions

        return update_to_best


    def merge(self, strategy):
        '''
        Takes another strategy
        Merges Q values
        '''
        if isinstance(strategy, Qlearning):
            new_Q = {}
            new_Q_values = {}

            for state in self.Q:
                new_Q[state] = {}
                new_Q_values[state] = SortedDict()

                for action in self.Q[state]:
                    for other_action in strategy.Q[state]:
                        new_action = action + other_action
                        new_value = (self.Q[state][action] + strategy.Q[state][other_action])
                        new_Q[state][new_action] = new_value
                        if new_value in new_Q_values[state]:
                            new_Q_values[state][new_value] += (new_action,)
                        else:
                            new_Q_values[state][new_value] = (new_action,)

    
            self.Q = new_Q

            self.Q_values = new_Q_values
