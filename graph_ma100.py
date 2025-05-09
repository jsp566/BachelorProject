import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt

from os.path import basename
from multiprocessing import Pool, cpu_count
import cProfile
import pstats
import copy
import os
import pickle

filename =  basename(__file__).replace('.py', '')

def main():
    # Start
    sessions = 2
    iterations = 10**7
    numb_firms = 2
    parallel=True
    savedData = True

    

    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)

    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData)

    lengths = []
    for i in range(sessions):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
        lengths.append(len(result))

    min_length = min(lengths)
    # Collusion Quotient:
    

    collusion_quotients = []
    for i in range(sessions):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
        collusion_quotients.append([state.collussion_quotient for state in result[:min_length]])
    
    collusion_quotients = np.array(collusion_quotients)

    average_collusion_quotient = np.mean(collusion_quotients, axis=(0,2))
    ma100=  lib.moving_average(average_collusion_quotient, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))


    # Plot results
    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename))


if __name__ == "__main__":
    config.profile_main(main,filename)
