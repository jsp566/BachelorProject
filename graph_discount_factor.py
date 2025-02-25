import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import cProfile
import pstats
import multiprocessing
from multiprocessing import Pool, cpu_count

filename =  basename(__file__)

def run_simulation(new_config, nash, mono, maxit):
    """ Runs a single simulation and computes collusion quotient moving average. """
    market, states = SIMULATOR.simulate(new_config)

    # Extract and process profits
    profits = np.array([state.profits for state in states[-1000:]])
    profits = np.mean(profits)

    # Compute collusion quotient
    collusion_quotient= lib.get_collusion_quotient(profits, nash, mono)
    
    return collusion_quotient

def main():
    # Start
    discount_factors = np.linspace(0.0, 1.0, 20, endpoint=False)
    times = 100
    maxit = 1000000
    market = SIMULATOR.setup(config.defaultconfig)
    nash = np.mean(market.get_nash_profits())
    mono = np.mean(market.get_monopoly_profits())


    average_collusion_quotient = []
    for gamma in discount_factors:
        new_config = config.create_config(discount_factor=gamma)
        sum_collusion_quotients = 0

        with Pool(processes=cpu_count()) as pool:
            results = pool.starmap(run_simulation, [(new_config, nash, mono, maxit)] * times)
        sum_collusion_quotients = np.sum(results)
        average_collusion_quotient.append(sum_collusion_quotients/times)

    #plot
    plt.plot(discount_factors, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Discount factor')
    plt.savefig(config.create_filepath(filename))


if __name__ == "__main__":
    config.profile_main(main,filename)
