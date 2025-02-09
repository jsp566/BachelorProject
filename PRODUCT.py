



class Product():
    '''
    Takes marginal costs and quality
    '''

    def __init__(self, firmid, productid, marginal_cost, quality):
        self.firmid = firmid
        self.productid = productid
        self.marginal_cost = marginal_cost
        self.quality = quality
        self.price = None
        self.share = None

