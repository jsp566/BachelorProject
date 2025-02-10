
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
        self.products = []
        self.P = []
        self.A = []


    def add_firm(self, firm):
        '''
        Takes firm
        Adds firm to market
        '''
        firm.firmid = self.next_firmid
        firm.market = self
        self.next_firmid += 1
        self.firms.append(firm)

    def simulate(self, num_periods):
        '''
        Takes number of periods
        Simulates market
        '''
        
        states = []

        if self.state == None:
            for product in self.products:
                self.P[product.productid] = np.random.choice(product.pricerange)
            shares = self.demand_function.get_shares(self.P, self.A)
            self.state = STATE.State(tuple(self.P), tuple(shares))

        for period in range(num_periods):
            for firm in self.firms:
                firm.set_prices(self.state)
            
            
            shares = self.demand_function.get_shares(self.P, self.A)

            new_state = STATE.State(tuple(self.P), tuple(shares), self.state.t+1)

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
                P0.append(product.marginal_cost)
                A.append(product.quality)
                MC.append(product.marginal_cost)

        P0 = np.array(P0)
        A = np.array(A)
        MC = np.array(MC)

        Nash = lib.Newton(P0, A, MC, self.demand_function.fun)
        Mono = lib.Monopoly_Prices(P0, A, MC, self.demand_function.fun)

        more = extra * (Mono-Nash)
        print(more)

        start = Nash-more
        end = Mono+more

        i = 0
        for firm in self.firms:
            for product in firm.products:
                if include_NE_and_Mono:
                    pricerange = np.linspace(start[i], end[i], num_prices-2)
                    product.pricerange =  np.sort(np.concatenate(([Nash[i], Mono[i]], pricerange)))

                else:
                    product.pricerange = np.linspace(start[i], end[i], num_prices)
                i += 1


    def get_nash_prices(self):
        '''
        Gives Nash prices
        '''
        P0 = []
        A = []
        MC = []

        for firm in self.firms:
            for product in firm.products:
                P0.append(product.marginal_cost)
                A.append(product.quality)
                MC.append(product.marginal_cost)

        P0 = np.array(P0)
        A = np.array(A)
        MC = np.array(MC)

        return lib.Newton(P0, A, MC, self.demand_function.fun)
    
    def get_monopoly_prices(self):
        '''
        Gives monopoly prices
        '''
        P0 = []
        A = []
        MC = []

        for firm in self.firms:
            for product in firm.products:
                P0.append(product.marginal_cost)
                A.append(product.quality)
                MC.append(product.marginal_cost)

        P0 = np.array(P0)
        A = np.array(A)
        MC = np.array(MC)

        return lib.Monopoly_Prices(P0, A, MC, self.demand_function.fun)