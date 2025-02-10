
import itertools
import lib
import numpy as np
import STATE

class Market():
    '''
    Takes demand function
    
    Simulates market
    '''
    
    def __init__(self, demand_function):
        self.firms = []
        self.demand_function = demand_function
        self.next_firmid = 0
        self.next_productid = 0
        self.state = None
        self.state_space = None
        self.P = []
        self.A = []
        self.MC = []
        self.shares = []

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
        
        states = []

        if self.state == None:
            
            index = np.random.randint(0,len(self.state_space)-1)
            state = self.state_space[index]
            self.state = STATE.State(state)

        for period in range(num_periods):
            for firm in self.firms:
                firm.set_prices(self.state)

            self.P = [product.price for firm in self.firms for product in firm.products]
            self.A = [product.quality for firm in self.firms for product in firm.products]

            shares = self.demand_function.get_shares(self.P, self.A)

            i = 0

            for firm in self.firms:
                for product in firm.products:
                    product.share = shares[i]
                    i += 1

            new_state = STATE.State(tuple(self.P), self.state.t+1)

            for firm in self.firms:
                firm.update_strategy(self.state, new_state)

            
            states.append(new_state)
            self.state = new_state

        return states

    
    def set_state_space(self):
        '''
        Gives state space
        '''
        prices = []

        for firm in self.firms:
            for product in firm.products:
                prices.append(product.pricerange)
        
        self.state_space = list(itertools.product(*prices))
    
    def set_priceranges(self, num_prices, include_NE_and_Mono=True, extra=0.1):
        '''
        Takes number of prices
        Sets price ranges for products
        '''
        
        P0 = []
        A = []
        MC = []

        for firm in self.firms:
            for product in firm.products:
                P0.append(0)
                A.append(product.quality)
                MC.append(product.marginal_cost)

        P0 = np.array(P0)
        A = np.array(A)
        MC = np.array(MC)

        Nash = lib.Newton(P0, A, MC, self.demand_function.fun)
        Mono = lib.Monopoly_Prices(P0, A, MC, self.demand_function.fun)

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
