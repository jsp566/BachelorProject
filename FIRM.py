



class Firm():
    '''
    Takes list of products and a strategy

    Can set new prices for products
    '''
    
    def __init__(self, firmid, products, strategy):
        self.firmid = firmid
        self.products = products
        self.strategy = strategy
    
    def set_prices(self, state, market):
        '''
        Takes state and market
        Using strategy
        Sets prices for own products
        '''
        pass

    def get_profit(self, state):
        '''
        Takes state
        Gives profit
        '''
        profit = 0
        for product in state.products:
            if product.firmid == self.firmid:
                profit += (product.price - product.marginal_cost) * product.share
        
        return profit
                

    def get_action_space(self):
        '''
        Gives action space
        '''
        pass