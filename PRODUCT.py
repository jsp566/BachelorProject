



class Product():
    '''
    This class is used to create a product object. The product object has the following attributes:
    firmid: The firm id of the firm that produces the product
    productid: The product id of the product
    marginal_cost: The marginal cost of the product
    quality: The quality of the product
    pricerange: The price range of the product
    '''

    def __init__(self, firmid, productid, marginal_cost, quality, pricerange):
        self.firmid = firmid
        self.productid = productid
        self.marginal_cost = marginal_cost
        self.quality = quality
        self.price = None
        self.share = None

