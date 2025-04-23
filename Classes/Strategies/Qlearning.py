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
        self.best_actions = None


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
        
        self.best_actions = {}
        for state in self.Q:
            max_val = max(self.Q[state].values())
            self.best_actions[state] = tuple([action for action, value in self.Q[state].items() if value == max_val])

    
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
            action = random.choice(self.best_actions[state])
        
        return action
        

    def update_strategy(self, state, action, next_state, profit):
        '''
        Takes state, action, next state
        Updates Q values
        '''

        next_max_val = self.Q[next_state.p][self.best_actions[next_state.p][0]]

        new_Q_val = (1 - self.learning_rate) * self.Q[state.p][action] + self.learning_rate * (profit + self.discount_factor * next_max_val)
        
        # check if best actions need to be updated
        max_val = self.Q[state.p][self.best_actions[state.p][0]]

        if new_Q_val > self.Q[state.p][action]:
            # check if new Q value is the best action
            if new_Q_val > max_val:
                self.best_actions[state.p] = (action,)
            # check if new Q value is equal to the best action
            elif new_Q_val == max_val:
                self.best_actions[state.p] += (action,)

            
        elif new_Q_val < self.Q[state.p][action]:
            # check if old Q value was the best action
            if self.Q[state.p][action] == max_val: 
                # remove action from best actions
                self.best_actions[state.p] = tuple([a for a in self.best_actions[state.p] if a != action])
                # check if there are no best actions left
                if len(self.best_actions[state.p]) == 0:
                    # set new best action to the action with the highest Q value
                    self.Q[state.p][action] = new_Q_val
                    max_val = max(self.Q[state.p].values())
                    self.best_actions[state.p] = tuple([a for a in self.Q[state.p] if self.Q[state.p][a] == max_val])

        
        self.Q[state.p][action] = new_Q_val

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

            self.best_actions = {}
            for state in self.Q:
                max_val = max(self.Q[state].values())
                self.best_actions[state] = tuple([action for action, value in self.Q[state].items() if value == max_val])
