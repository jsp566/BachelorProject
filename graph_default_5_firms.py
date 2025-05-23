import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pickle
import itertools


filename =  basename(__file__).replace('.py', '')



def main():
    # Start
    sessions = 100
    iterations = 10**7
    numb_firms = 5 
    parallel=True
    savedData = True



    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)
    SIMULATOR.fix_config(new_config)
    market= SIMULATOR.setup(new_config)
    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData)
    
    # Collusion Quotient:
    lengths = []
    collusion_quotients = []
    for i in range(sessions):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
        lengths.append(len(result))
        collusion_quotients.append(np.mean([state.collussion_quotient  for state in result], axis=1))
   


    plt.hist(lengths, bins=100)
    plt.xlabel('Length of session')
    plt.ylabel('Frequency')
    plt.title('Length of session')
    plt.savefig(config.create_filepath(filename + "_lengths"))

    plt.clf()

    min_length = min(lengths)
    max_length = max(lengths)


    for i in range(sessions):
        cq = np.array(collusion_quotients[i])
        if len(cq) < max_length:
            collusion_quotients[i] = np.append(cq, [np.mean(cq[-100:])]*(max_length - len(cq)))

    collusion_quotients = np.array(collusion_quotients)

    average_collusion_quotient = np.mean(collusion_quotients, axis=0)

    plt.plot(range(min_length), average_collusion_quotient[:min_length])
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient"))

    plt.clf()

    period = range(len(average_collusion_quotient))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient_full"))

    plt.clf()

    # Moving average
    ma100=  lib.moving_average(average_collusion_quotient, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100"))



if __name__ == "__main__":
    config.profile_main(main,filename)
