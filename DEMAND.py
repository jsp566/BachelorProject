import numpy as np


class DemandFunction():
    '''
    Takes function with P and A as arguments

    Given prices and product (state), gives share for each product
    '''
    
    def __init__(self, fun):
        self.fun = fun

    def get_share(self, state):
        '''
        Takes prices and product (state)
        Gives share for product
        '''
        
        P = []
        A = []

        for product in state.products:
            P.append(product.price)
            A.append(product.quality)

        P = np.array(P)
        A = np.array(A)

        shares = self.fun(P, A)

        for i, product in enumerate(state.products):
            product.share = shares[i]




    