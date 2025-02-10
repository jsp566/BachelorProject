

class State():
    '''
    State class
    Tuple of prices 
    Tuple of shares
    Time period
    '''
    
    def __init__(self, prices, shares, t=0):
        self.t = 0
        self.prices = prices
        self.shares = shares
        