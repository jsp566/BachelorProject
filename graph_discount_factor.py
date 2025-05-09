import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
from multiprocessing import Pool, cpu_count
import os
import pickle

filename =  basename(__file__).replace('.py', '')



def main():

    # Start
    discount_factors = np.linspace(0.0, 1.0, 2, endpoint=False)
    sessions = 2
    iterations = 10**7
    numb_firms = 2
    parallel=True
    savedData = True
    
    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)

    variations = {
        "discount_factor": discount_factors,
    }

    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData, variations=variations)
    
    average_collusion_quotient = [] #List to store average collusion quotients
    for gamma in discount_factors:
        gammacollusion_quotients = []
        for i in range(sessions):
            with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, f"(('discount_factor', {gamma}),)_" + str(i) + ".pkl"), 'rb') as f:
                result = pickle.load(f)
            
            collussion_quotients = [state.collussion_quotient for state in result[-100000:]]
            gammacollusion_quotients.append(np.mean(collussion_quotients))
        average_collusion_quotient.append(np.mean(gammacollusion_quotients))

    #plot
    plt.plot(discount_factors, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Discount factor')
    plt.savefig(config.create_filepath(filename))


if __name__ == "__main__":
    config.profile_main(main,filename)
