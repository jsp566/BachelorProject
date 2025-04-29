import Classes.MARKET as MARKET
import Classes.DEMAND as DEMAND

import Classes.FIRM as FIRM
import Classes.PRODUCT as PRODUCT

import copy
from multiprocessing import Pool, cpu_count
from functools import partial

import os
import pickle


def list_creator(input, numb):
    if type(input) == list:
        assert len(input) == numb, 'List must be of length numb'
        return input
    else:
        return [input] * numb


def fix_config(config):
    # check numb firms is int
    assert type(config['numb_firms']) == int, 'numb_firms must be an integer'

    # check numb products is int
    config['numb_products'] = list_creator(config['numb_products'], config['numb_firms'])

    config['strategy'] = list_creator(config['strategy'], config['numb_firms'])
    config['exploration_rate'] = list_creator(config['exploration_rate'], config['numb_firms'])
    config['exploration_rate_params'] = list_creator(config['exploration_rate_params'], config['numb_firms'])
    config['discount_factor'] = list_creator(config['discount_factor'], config['numb_firms'])
    config['learning_rate'] = list_creator(config['learning_rate'], config['numb_firms'])

    if type(config['quality']) != list:
        config['quality'] = [[config['quality']] * numb for numb in config['numb_products']]
    else:
        if type(config['quality'][0]) != list:
            config['quality'] = [config['quality']] * config['numb_firms']
        
    if type(config['marginal_cost']) != list:
        config['marginal_cost'] = [[config['marginal_cost']] * numb for numb in config['numb_products']]
    else:
        if type(config['marginal_cost'][0]) != list:
            config['marginal_cost'] = [config['marginal_cost']] * config['numb_firms']





def setup(config):
    fix_config(config)
    share = partial(config['demand_function'], **config['demand_function_params'])
    # check demand function is callable
    assert callable(share), 'Demand function must be callable'
    # check demand function is callable
    market = MARKET.Market(DEMAND.DemandFunction(share))

    for i in range(config['numb_firms']):
        exploration_rate = partial(config['exploration_rate'][i], **config['exploration_rate_params'][i])
        # check exploration rate is callable
        assert callable(exploration_rate), 'Exploration rate must be callable'

        firm  = FIRM.Firm(config['strategy'][i](config['discount_factor'][i], config['learning_rate'][i], exploration_rate))
        market.add_firm(firm)
        for j in range(config['numb_products'][i]):
            product = PRODUCT.Product(config['marginal_cost'][i][j], config['quality'][i][j])
            firm.add_product(product)

    market.set_priceranges(config['numb_prices'], config['include_NE_and_Mono'], config['extra'])
    return market


def session(market, iterations, start_period = 1, convergence = None):
    new_market = copy.deepcopy(market)

    return new_market.simulate(iterations, start_period=start_period, convergence=convergence)


def simulate(config):

    market = setup(config)
    return market, market.simulate(config['iterations'], start_period=config['start_period'], convergence=config['convergence'])


def simulate_sessions(config, filename = None, parallel = True, savedData = False, session = session):
    output_dir = os.path.join(os.getcwd(), 'Output', 'Data')

    market = setup(config)
    if savedData:  
        with open(os.path.join(output_dir, filename, 'config.pkl'), 'rb') as f:
            old_config = pickle.load(f)
        assert old_config == config, 'Configurations do not match'
        with open(os.path.join(output_dir, filename, 'results.pkl'), 'rb') as f:
            results = pickle.load(f)
    else:
        
        if parallel:
            with Pool(processes=cpu_count()) as pool:
                results = pool.starmap(session, [(market, config['iterations'], config['start_period'], config['convergence'])] * config['sessions'])
        else:
            results = []
            for i in range(config['sessions']):
                results.append(session(market, config['iterations'], start_period=config['start_period'], convergence=config['convergence']))

        if filename:
            os.makedirs(os.path.join(output_dir, filename), exist_ok=True)

            # Save config
            with open(os.path.join(output_dir, filename, 'config.pkl'), 'wb') as f:
                pickle.dump(config, f)

            # Save market
            with open(os.path.join(output_dir, filename, 'market.pkl'), 'wb') as f:
                pickle.dump(market, f)

            # Save results
            with open(os.path.join(output_dir, filename, 'results.pkl'), 'wb') as f:
                pickle.dump(results, f)
    return market, results