
import itertools
import numpy as np


class Firm():
    '''
    Takes a strategy

    Can set new prices for products
    '''
    
    def __init__(self, strategy):
        self.strategy = strategy

        self.index = None        
        self.market = None
        self.products = []

        self.action_space = None
        self.prev_action = None

    def add_product(self, product):
        '''
        Takes product
        Adds product to firm
        '''
        assert(product.firm == None)
        product.firm = self
        self.products.append(product)
        self.market.add_product(product) 


    
    
    def get_action(self, state, t):
        '''
        Takes state and market
        Using strategy
        Sets prices for own products
        '''
        action = self.strategy.get_action(state, t)
        self.prev_action = action
    
        return action
    
    def get_best_action(self, state):
        '''
        Takes state and market
        Using strategy
        Sets prices for own products
        '''
        action = self.strategy.best_action(state)
        return action

    def update_strategy(self, state, next_state, profit):
        '''
        Takes state, action, next state
        Updates strategy
        '''
        return self.strategy.update_strategy(state, self.prev_action, next_state, profit)            

    def set_action_space(self):
        '''
        Gives action space
        '''
        prices = []

        for product in self.products:
            prices.append(product.pricerange)

        self.action_space = list(itertools.product(*prices))
    

