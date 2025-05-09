import numpy as np
import Classes.Strategies.Qlearning as Qlearning
import os
import io
import cProfile
import pstats

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
                 "exploration_rate": Calvani_Exploration_Rate(),
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
        
    return config


def create_filepath(filename):
    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs')
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename + '.png')
    return filepath
    

def profile_main(main, filename):
    profiler = cProfile.Profile()
    
    profiler.enable()
    main()
    profiler.disable()
    
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


