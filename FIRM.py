
import itertools


class Firm():
    '''
    Takes a strategy

    Can set new prices for products
    '''
    
    def __init__(self, strategy):
        self.firmid = None
        self.products = []
        self.strategy = strategy
        self.next_productid = 0

    def add_product(self, product):
        '''
        Takes product
        Adds product to firm
        '''
        product.firmid = self.firmid
        product.productid = self.next_productid
        self.next_productid += 1
        self.products.append(product)
    
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
        prices = []

        for product in self.products:
            prices.append(product.pricerange)

        return list(itertools.product(*prices))

