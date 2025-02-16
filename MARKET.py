
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
        self.demand_function = demand_function

        self.firms = []

        self.state_space = None
        self.current_state = None

        self.products = None
        self.A = None
        self.MC = None

    def add_firm(self, firm):
        '''
        Takes firm
        Adds firm to market
        '''
        assert(firm.market == None)
        firm.market = self
        self.firms.append(firm)

    def setup(self):
        '''
        Sets up market
        '''

        self.products = [product for firm in self.firms for product in firm.products]

        self.A = []
        self.MC = []

        for product in self.products:
            self.A.append(product.quality)
            self.MC.append(product.marginal_cost)

        self.A = np.array(self.A)
        self.MC = np.array(self.MC)

    def set_priceranges(self, num_prices, include_NE_and_Mono=True, extra=0.1):
        '''
        Takes number of prices
        Sets price ranges for products
        '''
        self.setup()
        priceranges = lib.Make_Price_Ranges(self.MC, self.A, self.MC, self.demand_function.fun, num_prices, include_NE_and_Mono, extra)
        
        i = 0
        for firm in self.firms:
            for product in firm.products:
                product.pricerange = priceranges[i]
                i += 1

    def simulate(self, num_periods):
        '''
        Takes number of periods
        Simulates market
        '''

        if self.state_space == None:

            for firm in self.firms:
                firm.set_action_space()
            
            self.set_state_space()
            
            for firmindex in range(len(self.firms)):
                firm = self.firms[firmindex]
                firm.strategy.initialize(self.state_space, firm.action_space, firmindex)

        states = []

        if self.current_state == None:
            actions = tuple([firm.get_action(None, 0) for firm in self.firms])

            self.current_state = self.state_space[actions]

            states.append(self.current_state)


        for period in range(1, num_periods):
            actions = tuple([firm.get_action(self.current_state, period) for firm in self.firms])
            
            new_state = self.state_space[actions]

            
            for i in range(len(self.firms)):
                self.firms[i].update_strategy(self.current_state, new_state, new_state.firm_profits[i])

            self.current_state = new_state
            states.append(self.current_state)

        return states

    
    def set_state_space(self):
        '''
        Gives state space
        '''
        actions = []

        for firm in self.firms:
            actions.append(firm.action_space)
        
        state_space = list(itertools.product(*actions))

        self.state_space = {}

        for actions in state_space:
            state = self.create_state(actions)
            self.state_space[actions] = state

    def create_state(self, actions):
        '''
        Takes actions
        Creates state
        '''
        prices = np.array([price for action in actions for price in action])
        shares = self.demand_function.get_shares(prices, self.A)
        profits = (prices - self.MC) * shares

        firm_shares = []
        firm_profits = []

        i = 0
        for action in actions:
            sum_shares = 0
            sum_profits = 0
            for price in action:
                sum_shares += shares[i]
                sum_profits += profits[i]
                i += 1
            
            firm_shares.append(sum_shares)
            firm_profits.append(sum_profits)
        
        return STATE.State(actions, prices, shares, profits, firm_shares, firm_profits)

    def get_nash_prices(self):
        '''
        Gives Nash prices
        '''
        return lib.Newton(self.MC, self.A, self.MC, self.demand_function.fun)

    def get_nash_profits(self):
        '''
        Gives Nash profits
        '''
        P = np.array(self.get_nash_prices())
        return lib.Profit(P, self.A, self.MC, self.demand_function.fun) 
    
    def get_monopoly_prices(self):
        '''
        Gives monopoly prices
        '''
        return lib.Monopoly_Prices(self.MC, self.A, self.MC, self.demand_function.fun)

    def get_monopoly_profits(self):
        '''
        Gives monopoly profits
        '''
        P = np.array(self.get_monopoly_prices())
        return lib.Profit(P, self.A, self.MC, self.demand_function.fun) 
