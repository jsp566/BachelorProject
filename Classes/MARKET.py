
import itertools
import utils.lib as lib
import numpy as np
import Classes.STATE as STATE

class Market():
    '''
    Takes demand function
    
    Simulates market
    '''
    
    def __init__(self, demand_function):
        self.demand_function = demand_function

        self.next_firm_index = 0
        self.firms = []

        self.next_product_index = 0
        self.products = []

        self.state_space = None
        self.current_state = None

        self.products = []
        self.A = None
        self.MC = None
        self.Nash = None
        self.Mono = None

    def add_firm(self, firm):
        '''
        Takes firm
        Adds firm to market
        '''
        assert(firm.market == None)
        firm.market = self
        firm.index = self.next_firm_index
        self.firms.append(firm)
        self.next_firm_index += 1

    def add_product(self, product):
        '''
        Takes product
        Adds product to market
        '''
        assert(product.market == None)
        product.market = self
        product.index = self.next_product_index
        self.products.append(product)
        self.next_product_index += 1

        
    def set_priceranges(self, num_prices, include_NE_and_Mono=True, extra=0.1):
        '''
        Takes number of prices
        Sets price ranges for products
        '''
        self.A = np.array([product.quality for product in self.products])
        self.MC = np.array([product.marginal_cost for product in self.products])
        self.Nash = lib.Newton(self.MC, self.A, self.MC, self.demand_function.fun)
        self.Mono = lib.Monopoly_Prices(self.MC, self.A, self.MC, self.demand_function.fun)

        priceranges = lib.Make_Price_Ranges(self.Nash, self.Mono, num_prices, include_NE_and_Mono, extra)
        
        i = 0
        for firm in self.firms:
            for product in firm.products:
                product.pricerange = priceranges[i]
                i += 1

        for firm in self.firms:
            firm.set_action_space()
        
        self.set_state_space()

        for firm in self.firms:
            firm.strategy.initialize(self.state_space, firm.action_space, firm.index)

    def set_state_space(self):
        '''
        Gives state space
        '''
        prices = []

        for product in self.products:
            prices.append(product.pricerange)
        
        state_space = list(itertools.product(*prices))

        self.state_space = {}

        for prices in state_space:
            state = STATE.State(prices, self)
            self.state_space[prices] = state


    def simulate(self, num_periods, start_period = 1, convergence = None):
        '''
        Takes number of periods
        Simulates market
        '''

        states = []
        converged = False
        similar_periods = 1

        if self.current_state is None:
            prices = [None] * len(self.products)
            for firm in self.firms:
                action = firm.get_action(None, 0)
                for i in range(len(firm.products)):
                    prices[firm.products[i].index] = action[i]

            prices = tuple(prices)

            self.current_state = self.state_space[prices]
            
            states.append(self.current_state)

        period = start_period
        while period < num_periods+start_period and not converged:

            prices = [None] * len(self.products)

            for firm in self.firms:
                action = firm.get_action(self.current_state, period)
                for i in range(len(firm.products)):
                    prices[firm.products[i].index] = action[i]

            prices = tuple(prices)

            new_state = self.state_space[prices]

            update_to_best = False
            for i in range(len(self.firms)):
                update_to_best |= self.firms[i].update_strategy(self.current_state, new_state, new_state.firm_profits[i])

            self.current_state = new_state
            states.append(self.current_state)
            period += 1
            if convergence is not None:

                
               
                
                # if similar to previous period then add and check if reached else reset and update
                if update_to_best:
                    similar_periods = 1
                else:
                    similar_periods += 1
                    if similar_periods >= convergence:
                        converged = True
                    


        return states

    def reset(self):
        '''
        Resets market
        '''
        self.current_state = None
        for firm in self.firms:
            firm.prev_action = None
            firm.strategy.initialize(self.state_space, firm.action_space, firm.index)

    def merge(self, firmindex1, firmindex2):
        # Move products
        for product in self.firms[firmindex2].products:
            product.firm = self.firms[firmindex1]
            self.firms[firmindex1].products.append(product)
        
        self.firms[firmindex2].products = []
    
        # make new actionspace
        self.firms[firmindex1].set_action_space()

        # update strategy if both are q learning
        self.firms[firmindex1].strategy.merge(self.firms[firmindex2].strategy)
        self.firms[firmindex2].strategy = None

        # Remove from firm list
        self.firms.pop(firmindex2)

        # remake firmids
        for i in range(len(self.firms)):
            self.firms[i].index = i

        self.next_firm_index -= 1
        

        # update state space to calculate new firm profits
        self.set_state_space()

        
        


    def get_nash_prices(self):
        '''
        Gives Nash prices
        '''
        if self.Nash is None:
            self.Nash = lib.Newton(self.MC, self.A, self.MC, self.demand_function.fun)
        return self.Nash

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
        if self.Mono is None:
            self.Mono = lib.Monopoly_Prices(self.MC, self.A, self.MC, self.demand_function.fun)
        return self.Mono

    def get_monopoly_profits(self):
        '''
        Gives monopoly profits
        '''
        P = np.array(self.get_monopoly_prices())
        return lib.Profit(P, self.A, self.MC, self.demand_function.fun)


 
