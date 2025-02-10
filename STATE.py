

class State():
    '''
    State class
    Tuple of prices 
    Tuple of shares
    Time period
    '''
    
    def __init__(self, prices, shares, profits, t=1):
        self.prices = prices
        self.shares = shares
        self.profits = profits
        self.t = t
        