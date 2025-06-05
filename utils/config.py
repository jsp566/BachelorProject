import numpy as np
import Classes.Strategies.Qlearning as Qlearning
import os
import io
import cProfile
import pstats
from datetime import datetime


# Demand function
class Share():
    def __init__(self):
        self.mu = None
        return None

    def set(self, params):
        self.mu = params[0]
        return self

    def __call__(self, P, A):
        numer = np.exp((A-P)/self.mu)
        denom = 1 + np.sum(numer)
        result = numer/denom
        return result
    
    def __eq__(self, other):
        return isinstance(other, Share)

# Exloration rates

class Calvani_Exploration_Rate():
    def __init__(self):
        self.beta = None
        return None
    
    def set(self, params):
        self.beta = params[0]
        return self

    def __call__(self, t):
        return np.exp(-self.beta*t)
    
    def __eq__(self, other):
        return isinstance(other, Calvani_Exploration_Rate)

defaultconfig = {# Simulation config
                 "sessions": 8,
                
                 "start_period": 1,
                 "iterations": 1000000,
                 "convergence": 100000,

                 # Market config  
                 "demand_function": Share(),
                 "demand_function_params": (0.25,), # Demand function parameters
                 "numb_firms": 2,

                 # Agent config
                 "numb_products": 1,
                 "strategy": Qlearning.Qlearning,
                 # Strategy config 
                 "exploration_rate": Calvani_Exploration_Rate,
                 "exploration_rate_params": (4 * 10**-6,), # Exploration rate parameters 
                 "discount_factor": 0.95, 
                 "learning_rate": 0.15, 

                 # Product config
                 "quality": 2, 
                 "marginal_cost": 1, 

                 # Price config (Product or Market?)
                 "numb_prices": 15, 
                 "include_NE_and_Mono": False, 
                 "extra": 0.1}
# Given memory of prices = 1


def create_config(**kwargs):
    config = defaultconfig.copy()
    for key, value in kwargs.items():
        if key in config:
            config[key] = value
        else:
            raise KeyError(f"Key '{key}' not found in default configuration.")
    
    fix_config(config)
    return config


def create_filepath(filename):
    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs')
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename + '.png')
    return filepath
    

def profile_main(main, filename):
    
    profiler = cProfile.Profile()
    print(f"{datetime.now()} Profiling {filename}")
    profiler.enable()
    main()
    profiler.disable()
    print(f"{datetime.now()} Profiling {filename} completed")

    save_dir = 'Output/Profiles'
    os.makedirs(save_dir, exist_ok=True)
    profile_name = filename + '_profile.txt'

    with open(os.path.join(save_dir, profile_name), 'w') as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.sort_stats('cumulative')
        stats.print_stats(50)
        stats.sort_stats('time')
        stats.print_stats(50)
        stats.sort_stats('calls')
        stats.print_stats(100)

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
