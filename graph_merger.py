import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import pickle
import os
from copy import deepcopy
import graph_maker


filename =  basename(__file__).replace('.py', '')


def new_session(i, market, iterations, start_period = 1, convergence = None, foldername = None, variation = None):
    new_market = deepcopy(market)
    
    before = new_market.simulate(iterations, start_period=start_period, convergence=convergence)
    new_market.merge(0,1)
    after = new_market.simulate(iterations, start_period=start_period, convergence=convergence)
    if foldername:
        filename = str(i) + ".pkl"
        if variation:

            filename = str(variation) + "_" + filename
            
        with open(os.path.join(os.getcwd(), 'Output', 'Data', foldername, filename), 'wb') as f:
            pickle.dump(before + after, f)
    return


def main():
    # Start
    sessions = 100
    iterations = 10**7
    numb_firms = 3
    parallel=True
    savedData = True
    


    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)
    market= SIMULATOR.setup(new_config)
    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData, session=new_session)
    # Collusion Quotient:




    states = graph_maker.make_graphs(filename, new_config, market, merger = True)

    lengths = [len(result) for result in states]

    print("Getting mergers periods data")
    mergerperiods = [next(i for i, state in enumerate(result) if len(state.firm_profits) < numb_firms) for result in states]
    plt.hist(mergerperiods, bins=100)
    plt.xlabel('Periods until merger')
    plt.ylabel('Frequency')
    plt.title('Periods until merger')
    plt.savefig(config.create_filepath(filename + "_periods_before_merger"))

    plt.clf()

    plt.hist([lengths[i] - mergerperiods[i] for i in range(len(mergerperiods))], bins=100)
    plt.xlabel('Periods after merger')
    plt.ylabel('Frequency')
    plt.title('Periods after merger')
    plt.savefig(config.create_filepath(filename + "_periods_after_merger"))

    plt.clf()

    print("Calculating lengths of collusion quotients")
    

    new_states = [None] * sessions
    for i in range(sessions):
        new_states[i] = states[i][mergerperiods[i]-10**5:]

    graph_maker.make_graphs(filename + "_after_merger", new_config, market, states=new_states, merger=True)


if __name__ == "__main__":
    config.profile_main(main,filename)
