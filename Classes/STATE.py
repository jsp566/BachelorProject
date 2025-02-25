

class State():
    '''
    State class
    '''
    
    def __init__(self, actions, prices, shares, profits, collussion_quotient):
        self.actions = actions
        self.prices = prices
        self.shares = shares
        self.profits = profits
        self.collussion_quotient = collussion_quotient

        self.firm_shares = []
        self.firm_profits = []

        i = 0
        for action in self.actions:
            sum_shares = 0
            sum_profits = 0

            for price in action:
                sum_shares += self.shares[i]
                sum_profits += self.profits[i]
                i += 1
            
            self.firm_shares.append(sum_shares)
            self.firm_profits.append(sum_profits)


    def __eq__(self, other):
        return self.actions == other.actions
    
    def __hash__(self):
        return hash(self.actions)
    
    def __str__(self):
        return str(self.actions)
        