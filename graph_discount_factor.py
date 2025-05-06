import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
from multiprocessing import Pool, cpu_count

filename =  basename(__file__).replace('.py', '')



def main():

    # Start
    discount_factors = np.linspace(0.0, 1.0, 10, endpoint=False)
    sessions = 2
    iterations = 10**7
    numb_firms = 2
    parallel=True

    average_collusion_quotient = [] #List to store average collusion quotients
    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)

    variations = {
        "discount_factor": discount_factors,
    }

    results = SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=False, variations=variations)
    
    for gamma in discount_factors:
        key = frozenset([("discount_factor", gamma)])
             
        collusion_quotients = [[state.collussion_quotient for state in result[-100000:]] for result in results]
        collusion_quotients = np.array(collusion_quotients)
        average_collusion_quotient.append(np.mean(collusion_quotients))

    #plot
    plt.plot(discount_factors, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Discount factor')
    plt.savefig(config.create_filepath(filename))


if __name__ == "__main__":
    config.profile_main(main,filename)
