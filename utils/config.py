import numpy as np
import Classes.Strategies.Qlearning as Qlearning
import os
import cProfile
import pstats

# Demand function
mu = 0.25
def Share(P, A):
    numer = np.exp((A-P)/mu)
    denom = 1 + np.sum(numer)
    result = numer/denom
    return result

# Exloration rates
beta = 4 * 10**-6
def Calvani_Exploration_Rate(t):
    return np.exp(-beta*t)

defaultconfig = {# Simulation config
                 "sessions": 8,
                 "iterations": 1000000,
                 "seed": 0,

                 # Market config  
                 "demand_function": Share,
                 "numb_firms": 2,

                 # Agent config
                 "numb_products": 1,
                 "strategy": Qlearning.Qlearning,
                 # Strategy config 
                 "exploration_rate": Calvani_Exploration_Rate, 
                 "discount_factor": 0.95, 
                 "learning_rate": 0.125, 

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
    config.update(kwargs)
    return config


def create_filepath(file):
    save_dir = 'Output/Graphs'
    os.makedirs(save_dir, exist_ok=True)
    filename = file.replace('.py', '')
    filepath = os.path.join(save_dir, filename + '.png')
    return filepath
    

def profile_main(main, filename):
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    profiler.dump_stats('profile.prof')
    profile_name = 'profile_' + filename.replace('.py', '.txt')
    with open(profile_name, 'w') as f:
        stats = pstats.Stats('profile.prof', stream=f)
        stats.sort_stats('cumulative')
        stats.print_stats(50)
        stats.sort_stats('time')
        stats.print_stats(50)
        stats.sort_stats('calls')
        stats.print_stats(100)


