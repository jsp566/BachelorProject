

class State():
    '''
    State class
    Tuple of prices 
    Tuple of shares
    Time period
    '''
    
    def __init__(self, actions, prices, shares, profits, firm_shares, firm_profits):
        self.actions = actions
        self.prices = prices
        self.shares = shares
        self.profits = profits
        self.firm_shares = firm_shares
        self.firm_profits = firm_profits

    def __eq__(self, other):
        return self.actions == other.actions
    
    def __hash__(self):
        return hash(self.actions)
    
    def __str__(self):
        return str(self.actions)
        