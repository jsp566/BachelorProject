import numpy as np
import random


class Qlearning():
    '''
    Takes discount factor, learning rate, exploration rate
    '''
    def __init__(self, discount_factor, learning_rate, exploration_rate):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate

        self.Q = None


    def initialize(self, state_space, action_space, firmindex):
        '''
        Initializes strategy
        '''
        
        action_profit_sums = {action: 0 for action in action_space}
        action_counter = {action: 0 for action in action_space}

        for state in state_space:
            action = state_space[state].actions[firmindex]
            firmprofit = state_space[state].firm_profits[firmindex]

            action_profit_sums[action] += firmprofit
            action_counter[action] += 1

        self.Q = {}

        for state in state_space:
            self.Q[state] = {}
            for action in action_space:
                self.Q[state][action] = (action_profit_sums[action]) / ((1 - self.discount_factor) * action_counter[action])

    
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
            max_val = max(self.Q[state].values())

            best_actions = [action for action, value in self.Q[state].items() if value == max_val]
            
            action = random.choice(best_actions)
        
        return action
        

    def update_strategy(self, state, action, next_state, profit):
        '''
        Takes state, action, next state
        Updates Q values
        '''

        next_max_val = max(self.Q[next_state.p].values())

        self.Q[state.p][action] = (1 - self.learning_rate) * self.Q[state.p][action] + self.learning_rate * (profit + self.discount_factor * next_max_val)

    def merge(self, strategy):
        '''
        Takes another strategy
        Merges Q values
        '''
        if isinstance(strategy, Qlearning):
            new_Q = {}
            
            for state in self.Q:
                new_Q[state] = {}

                for action in self.Q[state]:
                    for other_action in strategy.Q[state]:
                        new_action = action + other_action
                        new_Q[state][new_action] = (self.Q[state][action] + strategy.Q[state][other_action])
    
            self.Q = new_Q
                    
        
