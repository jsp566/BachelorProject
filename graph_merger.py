import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import copy


filename =  basename(__file__).replace('.py', '')

def new_session(market, iterations, start_period = 1, convergence = None):
        new_market = copy.deepcopy(market)
        before = new_market.simulate(iterations, start_period=start_period, convergence=convergence)
        new_market.merge(0,1)
        after = new_market.simulate(iterations, start_period=start_period, convergence=convergence)
        return before + after

def main():
    # Start
    sessions = 2
    iterations = 100000000
    numb_firms = 3
 


    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)

    market, results = SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=True, savedData=False, session= new_session)



    # Collusion Quotient:
    min_length = min(len(result) for result in results)
    collusion_quotients = [[state.collussion_quotient for state in result[:min_length]] for result in results]
    
    collusion_quotients = np.array(collusion_quotients)

    average_collusion_quotient = np.mean(collusion_quotients, axis=(0,2))

    period = range(len(average_collusion_quotient))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient"))


if __name__ == "__main__":
    config.profile_main(main,filename)
