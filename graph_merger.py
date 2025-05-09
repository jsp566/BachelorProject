import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import copy
import pickle
import os

filename =  basename(__file__).replace('.py', '')


def new_session(i, market, iterations, start_period = 1, convergence = None, foldername = None, variation = None):
    new_market = copy.deepcopy(market)
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
    sessions = 2
    iterations = 10**7
    numb_firms = 3
    parallel=True
    savedData = True
    


    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)

    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData, session=new_session)
    # Collusion Quotient:

    lengths = []
    for i in range(sessions):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
        lengths.append(len(result))

    min_length = min(lengths)

    collusion_quotients = []
    for i in range(sessions):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
        collusion_quotients.append([state.collussion_quotient for state in result[:min_length]])
    
    collusion_quotients = np.array(collusion_quotients)

    average_collusion_quotient = np.mean(collusion_quotients, axis=(0,2))

    period = range(len(average_collusion_quotient))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient"))


if __name__ == "__main__":
    config.profile_main(main,filename)
