



class Firm():
    '''
    Takes list of products and a strategy

    Can set new prices for products
    '''
    
    def __init__(self, firmid, products, strategy):
        self.firmid = firmid
        self.products = products
        self.strategy = strategy
    
    def set_prices(self, state):
        '''
        Takes state
        Using strategy
        Sets prices for products
        '''
        pass

    def get_profit(self, state):
        '''
        Takes state
        Gives profit
        '''
        pass


    