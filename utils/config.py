import numpy as np
import Classes.Qlearning as Qlearning
import os
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

defaultconfig = {"demand_function": Share,
                 "numb_firms": 2,

                 "strategy": Qlearning.Qlearning,
                 "exploration_rate": Calvani_Exploration_Rate, 
                 "discount_factor": 0.95, 
                 "learning_rate": 0.125, 

                 "numb_products": 1,  
                 "quality": 2, 
                 "marginal_cost": 1, 

                 "numb_prices": 15, 
                 "include_NE_and_Mono": False, 
                 "extra": 0.1,

                 "iterations": 1000000}


defaultconfig_3_firms = {"demand_function": Share,
                 "numb_firms": 3,

                 "strategy": Qlearning.Qlearning,
                 "exploration_rate": Calvani_Exploration_Rate, 
                 "discount_factor": 0.95, 
                 "learning_rate": 0.125, 

                 "numb_products": 1,  
                 "quality": 2, 
                 "marginal_cost": 1, 

                 "numb_prices": 15, 
                 "include_NE_and_Mono": False, 
                 "extra": 0.1,

                 "iterations": 1000000}
# Given memory of prices = 1

def create_config(**kwargs):
    config = defaultconfig.copy()
    config.update(kwargs)
    return config

def create_config_3(**kwargs):
    config = defaultconfig_3_firms.copy()
    config.update(kwargs)
    return config

def create_filepath(file):
    save_dir = 'Output'
    os.makedirs(save_dir, exist_ok=True)
    filename = file.replace('.py', '.png')
    filepath = os.path.join(save_dir, filename)
    return filepath
    
    

