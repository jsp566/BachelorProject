import Classes.MARKET as MARKET
import Classes.DEMAND as DEMAND

import Classes.FIRM as FIRM
import Classes.PRODUCT as PRODUCT

import copy
from multiprocessing import Pool, cpu_count
import itertools
import numpy as np
import os
import pickle
import numpy as np
from datetime import datetime

from copy import deepcopy

def list_creator(inputlist, numb):
    if type(inputlist) == tuple:
        assert len(inputlist) == numb, 'List must be of length numb'
        return inputlist
    else:
        return (inputlist,) * numb


def fix_config(config):
    share = config['demand_function'].set(config['demand_function_params'])
    # check demand function is callable
    assert callable(share), 'Demand function must be callable'
    # check numb firms is int
    assert type(config['numb_firms']) == int, 'numb_firms must be an integer'

    # check numb products is int
    config['numb_products'] = list_creator(config['numb_products'], config['numb_firms'])

    config['strategy'] = list_creator(config['strategy'], config['numb_firms'])
    if type(config['exploration_rate']) == tuple:
        assert len(config['exploration_rate']) == config['numb_firms'], 'List must be of length numb_firms'
    else:
        config['exploration_rate'] = tuple([config['exploration_rate']() for _ in range( config['numb_firms'])])

    if type(config['exploration_rate_params']) != tuple:
        config['exploration_rate_params'] = tuple([(config['exploration_rate_params'],) * numb for numb in config['numb_firms']])
    else:
        if type(config['exploration_rate_params'][0]) != tuple:
            config['exploration_rate_params'] = (config['exploration_rate_params'],) * config['numb_firms']


    config['discount_factor'] = list_creator(config['discount_factor'], config['numb_firms'])
    config['learning_rate'] = list_creator(config['learning_rate'], config['numb_firms'])

    if type(config['quality']) != tuple:
        config['quality'] = tuple([(config['quality'],) * numb for numb in config['numb_products']])
    else:
        if type(config['quality'][0]) != tuple:
            config['quality'] = (config['quality'],) * config['numb_firms']
    
    if type(config['marginal_cost']) != tuple:
        config['marginal_cost'] = tuple([(config['marginal_cost'],) * numb for numb in config['numb_products']])
    else:
        if type(config['marginal_cost'][0]) != tuple:
            config['marginal_cost'] = (config['marginal_cost'],) * config['numb_firms']
    for i in range(config['numb_firms']):
        exploration_rate = config['exploration_rate'][i].set(config['exploration_rate_params'][i])
        # check exploration rate is callable
        assert callable(exploration_rate), 'Exploration rate must be callable'





def setup(config):
    #fix_config(config)
    
    # check demand function is callable
    market = MARKET.Market(DEMAND.DemandFunction(config['demand_function']))

    for i in range(config['numb_firms']):
        exploration_rate = config['exploration_rate'][i]
        # check exploration rate is callable
        firm  = FIRM.Firm(config['strategy'][i](config['discount_factor'][i], config['learning_rate'][i], exploration_rate))
        market.add_firm(firm)
        for j in range(config['numb_products'][i]):
            product = PRODUCT.Product(config['marginal_cost'][i][j], config['quality'][i][j])
            firm.add_product(product)
    
    if 'true_nash' in config and config['true_nash']:
        market.set_priceranges(config['numb_prices'], config['include_NE_and_Mono'], config['extra'], True)
    else:
        market.set_priceranges(config['numb_prices'], config['include_NE_and_Mono'], config['extra'])
    return market


def session(i, config, iterations, start_period = 1, convergence = None, foldername = None, variation = None):
    new_market = setup(config)
    states, best_action_states = new_market.simulate(iterations, start_period=start_period, convergence=convergence)

    if foldername:
        filename = str(i) + ".pkl"
        if variation:

            filename = str(variation) + "_" + filename
            

        with open(os.path.join(os.getcwd(), 'Output', 'Data', foldername, filename), 'wb') as f:
            pickle.dump(states, f)
        
        with open(os.path.join(os.getcwd(), 'Output', 'Data Best Actions', foldername, filename), 'wb') as f:
            pickle.dump(best_action_states, f)
        
        with open(os.path.join(os.getcwd(), 'Output', 'Market', foldername, filename), 'wb') as f:
            pickle.dump(new_market, f)
    return

    


def simulate(config):

    market = setup(config)
    return market, market.simulate(config['iterations'], start_period=config['start_period'], convergence=config['convergence'])

# variations is a dict of settings, with variables and a list of values
def simulate_variations(config, variations, filename = None, parallel = True, savedData = False, session = session):
    fix_config(config)
    output_dir = os.path.join(os.getcwd(), 'Output', 'Data')
    best_action_dir = os.path.join(os.getcwd(), 'Output', 'Data Best Actions')
    market_dir = os.path.join(os.getcwd(), 'Output', 'Market')

    if savedData:
        try:
            with open(os.path.join(output_dir, filename, '_config.pkl'), 'rb') as f:
                old_config = pickle.load(f)
                fix_config(old_config)
            
            with open(os.path.join(output_dir, filename, '_variations.pkl'), 'rb') as f:
                old_variations = pickle.load(f)
        
            same = True
            if old_config != config:

                print(f"Configurations do not match, running simulation")
                same = False
                

            if list(old_variations.keys()) != list(variations.keys()):
                print(f"Variations do not match, running simulation")
                same = False

            if same:
                for key in variations.keys():
                    if not (np.array(variations[key]) == np.array(old_variations[key])).all():
                        same = False
                    if not same:
                        print(f"Variations do not match, running simulation")
   
            if same: 
                print(f"Configurations match, skipping simulation")
                return
        except Exception as e:
            print("No files to compare")
            print(f"Error: {e}")    
    os.makedirs(os.path.join(output_dir, filename), exist_ok=True)
    os.makedirs(os.path.join(best_action_dir, filename), exist_ok=True)
    os.makedirs(os.path.join(market_dir, filename), exist_ok=True)
    # simulate for all combinations of variations

    combinations = list(itertools.product(*[[(key, value) for value in variations[key]] for key in sorted(variations.keys())]))
    results = {}

    for combination in combinations:
        print(f"{datetime.now()} Simulating combination: {combination}")
        resultkey = []
        # create a copy of the config
        new_config = copy.deepcopy(config)
        for key, value in combination:
            assert key in new_config, f'Key {key} not in config'
            new_config[key] = value
            resultkey.append((key, value))
        resultkey = frozenset(resultkey)
        fix_config(new_config)
        
        if parallel:
            
            inputparams = [(i, new_config, new_config['iterations'], new_config['start_period'], new_config['convergence'], filename, combination) for i in range(new_config['sessions'])]

            with Pool(processes=cpu_count()) as pool:
                pool.starmap(session, inputparams)
        else:
            
            for i in range(new_config['sessions']):
                session(i, new_config, new_config['iterations'], start_period=new_config['start_period'], convergence=new_config['convergence'], foldername=filename, variation=combination)
    if filename:
        os.makedirs(os.path.join(output_dir, filename), exist_ok=True)
        try:
            # Save config
            with open(os.path.join(output_dir, filename, '_config.pkl'), 'wb') as f:
                pickle.dump(config, f)

            # Save variations
            with open(os.path.join(output_dir, filename, '_variations.pkl'), 'wb') as f:
                pickle.dump(variations, f)

        except Exception as e:
            print(f"Error saving data: {e}")
    return 



def simulate_sessions(config, filename = None, parallel = True, savedData = False, session = session, variations = None):
    fix_config(config)
    output_dir = os.path.join(os.getcwd(), 'Output', 'Data')
    best_action_dir = os.path.join(os.getcwd(), 'Output', 'Data Best Actions')
    market_dir = os.path.join(os.getcwd(), 'Output', 'Market')


    if variations:
        return simulate_variations(config, variations, filename=filename, parallel=parallel, savedData=savedData, session=session)

    if savedData:
        try:
            with open(os.path.join(output_dir, filename, '_config.pkl'), 'rb') as f:
                old_config = pickle.load(f)
                fix_config(old_config)
            
            if old_config == config:
                print(f"{datetime.now()} Configurations match, skipping simulation")
                return
        except:
            print(f"{datetime.now()} No files to compare")

    os.makedirs(os.path.join(output_dir, filename), exist_ok=True)
    os.makedirs(os.path.join(best_action_dir, filename), exist_ok=True)
    os.makedirs(os.path.join(market_dir, filename), exist_ok=True)
    print(f"{datetime.now()} Simulating sessions")
    if parallel:
        
        inputparams = [(i, config, config['iterations'], config['start_period'], config['convergence'], filename) for i in range(config['sessions'])]

        with Pool(processes=8) as pool:
            pool.starmap(session, inputparams)
    else:
        for i in range(config['sessions']):
            session(i, config, config['iterations'], config['start_period'], config['convergence'], filename)

    if filename:
        os.makedirs(os.path.join(output_dir, filename), exist_ok=True)
        try:
            # Save config
            with open(os.path.join(output_dir, filename, '_config.pkl'), 'wb') as f:
                pickle.dump(config, f)

        except Exception as e:
            print(f"Error saving data: {e}")

    return