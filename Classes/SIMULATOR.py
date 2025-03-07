import Classes.MARKET as MARKET
import Classes.DEMAND as DEMAND

import Classes.FIRM as FIRM
import Classes.PRODUCT as PRODUCT

import copy
from multiprocessing import Pool, cpu_count
import time
import signal

import os
import pickle

import time

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


def session(market, iterations):
    new_market = copy.deepcopy(market)

    return new_market.simulate(iterations)


def simulate(config):

    market = setup(config)
    return market, market.simulate(config['iterations'])

def session(market, iterations):
    new_market = copy.deepcopy(market)

    return new_market.simulate(iterations)

def simulate_sessions(config, filename = None, parallel = True, savedData = False):
    market = setup(config)
    if savedData:  
        with open('Output/Data/' + filename + '/config.pkl', 'rb') as f:
            old_config = pickle.load(f)
        assert old_config == config, 'Configurations do not match'
        with open('Output/Data/' + filename + '/results.pkl', 'rb') as f:
            results = pickle.load(f)
    else:
        
        if parallel:
            with Pool(processes=cpu_count()) as pool:
                results = pool.starmap(session, [(market, config['iterations'])] * config['sessions'])
        else:
            results = []
            for i in range(config['sessions']):
                results.append(session(market, config['iterations']))

        if filename:
            os.makedirs('Output/Data/' + filename, exist_ok=True)

            # Save config
            with open('Output/Data/' + filename + '/config.pkl', 'wb') as f:
                pickle.dump(config, f)

            # Save market
            with open('Output/Data/' + filename + '/market.pkl', 'wb') as f:
                pickle.dump(market, f)

            # Save results
            with open('Output/Data/' + filename + '/results.pkl', 'wb') as f:
                pickle.dump(results, f)
    return market, results