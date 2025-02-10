
import itertools
import lib
import numpy as np

class Market():
    '''
    Takes demand function
    
    Simulates market
    '''
    
    def __init__(self, demand_function):
        self.firms = []
        self.demand_function = demand_function
        self.next_firmid = 0
        self.state = None

    def add_firm(self, firm):
        '''
        Takes firm
        Adds firm to market
        '''
        firm.firmid = self.next_firmid
        self.next_firmid += 1
        self.firms.append(firm)

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
    
    def set_priceranges(self, num_prices, include_NE_and_Mono=True, extra=0.1):
        '''
        Takes number of prices
        Sets price ranges for products
        '''
        
        MC = []
        A = []

        for firm in self.firms:
            for product in firm.products:
                MC.append(product.margin_cost)
                A.append(product.quality)

        MC = np.array(MC)
        A = np.array(A)

        Nash = lib.newton(MC, A, MC, self.demand_function.fun)
        Mono = lib.monopoly_prices(MC, A, MC, self.demand_function.fun)

        start = Nash*(1-extra)
        end = Mono*(1+extra)

        i = 0
        for firm in self.firms:
            for product in firm.products:
                if include_NE_and_Mono:
                    pricerange = np.linspace(start[i], end[i], num_prices-2)
                    product.pricerange =  np.sort(np.concatenate(([Nash[i], Mono[i]], pricerange)))

                else:
                    product.pricerange = np.linspace(start[i], end[i], num_prices)
                i += 1

