
import itertools
import lib
import numpy as np

class Market():
    '''
    Takes list of firms and a demand function
    
    Simulates market
    '''
    
    def __init__(self, firms, demand_function):
        self.firms = firms
        self.demand_function = demand_function
        self.state = None

    def simulate(self, num_periods):
        '''
        Takes number of periods
        Simulates market
        '''
        
        prices = []

        for period in range(num_periods):
            for firm in self.firms:
                firm.set_prices(self.state, self)

            
            
            new_state = self.update_state(self.state)

            self.demand_function.update_shares(self.state, new_state)

            for firm in self.firms:
                firm.strategy.update_strategy(self.state, new_state)

            self.state = new_state

        return prices

    def update_state(self, state):
        '''
        Takes state
        Updates state
        '''
        pass

    
    def get_state_space(self):
        '''
        Gives state space
        '''
        prices = []

        for firm in self.firms:
            for product in firm.products:
                prices.append(product.pricerange)
        
        return list(itertools.product(*prices))
    
    def get_monopoly_prices(self):
        '''
        Gives monopoly prices
        '''
        MC = []
        A = []

        for firm in self.firms:
            for product in firm.products:
                MC.append(product.margin_cost)
                A.append(product.quality)
        
        MC = np.array(MC)
        A = np.array(A)

        return lib.monopoly_prices(MC, A, MC, self.demand_function.fun)

    def get_nash_prices(self):
        '''
        Gives Nash prices
        '''
        MC = []
        A = []

        for firm in self.firms:
            for product in firm.products:
                MC.append(product.margin_cost)
                A.append(product.quality)
        
        MC = np.array(MC)
        A = np.array(A)

        return lib.newton(MC, A, MC, self.demand_function.fun)
        