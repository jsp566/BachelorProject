import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pickle
import itertools
import utils.graph_maker as graph_maker
import Classes.Strategies.Qlearning_one_price


filename =  basename(__file__).replace('.py', '')



def main():
    # Start
    sessions = 100
    iterations = 2* 10**6
    extra = 0.1
    numb_firms = 1
    numb_products = 2
    convergence = None
    parallel=True
    savedData = True
    strategy = Classes.Strategies.Qlearning_one_price.Qlearning


    new_config = config.create_config(sessions=sessions, iterations=iterations, extra=extra, numb_firms=numb_firms, numb_products=numb_products, convergence=convergence, strategy=strategy)


    market= SIMULATOR.setup(new_config)
    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData)
    graph_maker.make_graphs(filename, new_config, market)



if __name__ == "__main__":
    config.profile_main(main,filename)
