import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pickle
import itertools
import Classes.Strategies.Qlearning_one_price
import utils.graph_maker as graph_maker

filename =  basename(__file__).replace('.py', '')



def main():
    # Start
    sessions = 100
    iterations = 10**7
    numb_firms = 2
    numb_products = (2, 2)
    strategy = Classes.Strategies.Qlearning_one_price.Qlearning
    parallel=True
    savedData = True


    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms, numb_products=numb_products, strategy=strategy)

    market= SIMULATOR.setup(new_config)
    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData)
    
    graph_maker.make_graphs(filename, new_config, market)








if __name__ == "__main__":
    config.profile_main(main,filename)
