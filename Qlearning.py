import numpy as np
import random
import lib



class Qlearning():
    '''
    Takes state space, action space, reward function, discount factor, learning rate, exploration rate, and initial Q values
    '''
    def __init__(self, discount_factor, learning_rate, exploration_rate):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.Q = None
        self.Market = None


    def initialize(self, state_space, action_space, Market):
        '''
        Initializes strategy
        '''
        self.Q = {}
        self.Market = Market
        
        self.no_of_firms = Market.get_no_of_firms()
        for state in state_space:
            self.Q[state] = {}
            for action in action_space:
                profit = self.discounted_price(state, action, action_space)
                self.Q[state][action] = profit

    
    def discounted_price(self, state, action, action_space):
        '''
        Takes state, action, next state
        Gives discounted profit
        '''
        profit = 0.0
        firms = self.no_of_firms
        actions = len(action_space)
        total_profit = 0.0

        for _ in range(actions):
            random_opponent_prices = [random.choice(action_space) for _ in self.Market.firms]
            prices = [action] + random_opponent_prices[1:]  # Firm sets its price, others random
            #shares = self.Market.demand_function.get_shares(prices, [self.Market.A for firm in self.Market.firms])
            
            firm_index = 0  # Assuming this is for the first firm
            total_profit = lib.Profit(np.array(prices), self.Market.A, np.array(self.Market.MC),  self.Market.demand_function.get_shares)
            sum_profit = np.sum(total_profit)
            #total_profit += (prices[firm_index] - self.Market.firms[firm_index].products[0].marginal_cost) * shares[firm_index]
        return sum_profit / ((1-self.discount_factor)*self.no_of_firms)
    

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
            max_val = max(self.Q[state.prices].values())

            best_actions = [action for action, value in self.Q[state.prices].items() if value == max_val]
            
            return random.choice(best_actions)
        

    def update_strategy(self, state, action, next_state, profit):
        '''
        Takes state, action, next state
        Updates Q values
        '''
        next_max_val = max(self.Q[next_state.prices].values())
        self.Q[state.prices][action] = (1 - self.learning_rate) * self.Q[state.prices][action] + self.learning_rate * (profit + self.discount_factor * next_max_val)
