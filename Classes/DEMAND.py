import numpy as np


class DemandFunction():
    '''
    Takes function with P and A as arguments

    Given prices and product (state), gives share for each product
    '''
    
    def __init__(self, fun):
        self.fun = fun

    def get_shares(self, P, A):
        '''
        Takes prices and product (state)
        Gives share for product
        '''

        P = np.array(P)
        A = np.array(A)
        
        shares = self.fun(P, A)

        return shares



    