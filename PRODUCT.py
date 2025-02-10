



class Product():
    '''
    This class is used to create a product object. The product object has the following attributes:
    productindex: The product index of the product
    marginal_cost: The marginal cost of the product
    quality: The quality of the product
    '''

    def __init__(self, marginal_cost, quality):
        self.productindex = None
        self.marginal_cost = marginal_cost
        self.quality = quality
        self.pricerange = None


