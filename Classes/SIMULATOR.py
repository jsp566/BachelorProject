import Classes.MARKET as MARKET
import Classes.DEMAND as DEMAND

import Classes.FIRM as FIRM
import Classes.PRODUCT as PRODUCT

def setup(config):
    market = MARKET.Market(DEMAND.DemandFunction(config['demand_function']))

    for i in range(config['numb_firms']):
        firm  = FIRM.Firm(config['strategy'](config['discount_factor'], config['learning_rate'], config['exploration_rate']))
        market.add_firm(firm)
        for j in range(config['numb_products']):
            product = PRODUCT.Product(config['marginal_cost'], config['quality'])
            firm.add_product(product)

    market.set_priceranges(config['numb_prices'], config['include_NE_and_Mono'], config['extra'])
    return market



def simulate(config):
    market = MARKET.Market(DEMAND.DemandFunction(config['demand_function']))

    for i in range(config['numb_firms']):
        firm  = FIRM.Firm(config['strategy'](config['discount_factor'], config['learning_rate'], config['exploration_rate']))
        market.add_firm(firm)
        for j in range(config['numb_products']):
            product = PRODUCT.Product(config['marginal_cost'], config['quality'])
            firm.add_product(product)

    market.set_priceranges(config['numb_prices'], config['include_NE_and_Mono'], config['extra'])
    
    return market, market.simulate(config['iterations'])