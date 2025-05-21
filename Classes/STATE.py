

import numpy as np
import utils.lib as lib

class State():
    '''
    State class
    '''
    
    def __init__(self, prices, market):
        self.p = prices
        self.actions = tuple([tuple([prices[product.index] for product in firm.products]) for firm in market.firms])
        self.prices = np.array(prices)
        self.shares = market.demand_function.get_shares(self.prices, market.A)
        self.profits = (self.prices - market.MC) * self.shares
        self.collussion_quotient = lib.get_collusion_quotient(self.profits, market.get_nash_profits(), market.get_monopoly_profits())
        self.true_collussion_quotient = lib.get_collusion_quotient(self.profits, market.get_true_nash_profits(), market.get_monopoly_profits())

        self.firm_shares = []
        self.firm_profits = []

        for firm in market.firms:
            sum_shares = 0
            sum_profits = 0

            for product in firm.products:
                sum_shares += self.shares[product.index]
                sum_profits += self.profits[product.index]
            
            self.firm_shares.append(sum_shares)
            self.firm_profits.append(sum_profits)


    def __eq__(self, other):
        return self.p == other.p
    
    def __hash__(self):
        return hash(self.actions)
    
    def __str__(self):
        return str(self.actions)
        