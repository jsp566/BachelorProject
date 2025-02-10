
import itertools
import numpy as np


class Firm():
    '''
    Takes a strategy

    Can set new prices for products
    '''
    
    def __init__(self, strategy):
        self.market = None
        self.firmid = None
        self.products = []
        self.strategy = strategy
        self.action_space = None
        self.prev_action = None

    def add_product(self, product):
        '''
        Takes product
        Adds product to firm
        '''
        product.firmid = self.firmid
        product.productid = self.market.next_productid
        self.market.next_productid += 1
    
        self.products.append(product)
        self.market.products.append(product)
        
        self.market.P.append(None)
        self.market.A.append(product.quality)
        self.market.MC.append(product.marginal_cost)
    
    def set_prices(self, state):
        '''
        Takes state and market
        Using strategy
        Sets prices for own products
        '''
        action = self.strategy.get_action(state)
        self.prev_action = action

        i = 0
        for product in self.products:
            self.market.P[product.productid] = action[i]
            i += 1

    def get_profit(self, state):
        '''
        Takes state
        Gives profit
        '''
        profit = 0

        for product in self.products:
            index = product.productid
            profit += state.profits[index]
        
        return profit
                
    def update_strategy(self, state, new_state):
        '''
        Takes state, next state
        Updates strategy
        '''
        profit = self.get_profit(new_state)
        self.strategy.update_strategy(state, self.prev_action, new_state, profit)

    def set_action_space(self):
        '''
        Gives action space
        '''
        prices = []

        for product in self.products:
            prices.append(product.pricerange)

        self.action_space = list(itertools.product(*prices))
    

