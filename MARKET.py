
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
        self.next_productindex = 0
        self.current_state = None
        self.state_space = None
        self.products = []
        self.P = []
        self.A = []
        self.MC = []


    def add_firm(self, firm):
        '''
        Takes firm
        Adds firm to market
        '''
        firm.market = self
        self.firms.append(firm)

    def get_profits(self, shares):
        P = np.array(self.P)
        MC = np.array(self.MC)
        shares = np.array(shares)

        profits = (P - MC) * shares
        return profits
        
    def create_state(self, t=0):
        prices = tuple(self.P)
        shares = self.demand_function.get_shares(self.P, self.A)
        profits = self.get_profits(shares)

        return STATE.State(prices, tuple(shares), tuple(profits), t)

    def simulate(self, num_periods):
        '''
        Takes number of periods
        Simulates market
        '''

        if self.state_space == None:
            self.set_state_space()

            for firm in self.firms:
                firm.action_space = firm.set_action_space()
                firm.strategy.initialize(self.state_space, firm.action_space)

        states = []

        if self.current_state == None:
            for product in self.products:
                self.P[product.productindex] = np.random.choice(product.pricerange)
            
            self.current_state = self.create_state()
            states.append(self.current_state)


        for period in range(num_periods-1):
            for firm in self.firms:
                firm.set_prices(self.current_state)
            
            new_state = self.create_state(self.current_state.t+1)

            for firm in self.firms:
                firm.update_strategy(self.current_state, new_state)

            self.current_state = new_state
            states.append(self.current_state)

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
        Nash = self.get_nash_prices()
        Mono = self.get_monopoly_prices()

        more = extra * (Mono-Nash)

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

        P0 = np.array(self.MC)
        A = np.array(self.A)
        MC = np.array(self.MC)

        return lib.Newton(P0, A, MC, self.demand_function.fun)
    
    def get_nash_profits(self):
        '''
        Gives Nash profits
        '''
        P = np.array(self.get_nash_prices())
        A = np.array(self.A)
        MC = np.array(self.MC)
        shares = self.demand_function.get_shares

        profits = lib.Profit(P, A, MC, shares)
        return profits
    
    def get_monopoly_prices(self):
        '''
        Gives monopoly prices
        '''
        P0 = np.array(self.MC)
        A = np.array(self.A)
        MC = np.array(self.MC)

        return lib.Monopoly_Prices(P0, A, MC, self.demand_function.fun)
    
    def get_monopoly_profits(self):
        '''
        Gives monopoly profits
        '''
        P = np.array(self.get_monopoly_prices())
        A = np.array(self.A)
        MC = np.array(self.MC)
        shares = self.demand_function.get_shares

        profits = lib.Profit(P, A, MC, shares)
        return profits