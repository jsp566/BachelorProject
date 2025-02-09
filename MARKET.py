


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
        
        for period in range(num_periods):
            for firm in self.firms:
                firm.set_prices(self.state, self)

            
            
            new_state = self.update_state(self.state)

            self.demand_function.update_shares(self.state, new_state)

            for firm in self.firms:
                firm.strategy.update_strategy(self.state, new_state)

            self.state = new_state

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
        pass