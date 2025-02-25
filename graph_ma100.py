import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt

from os.path import basename
from multiprocessing import Pool, cpu_count
import cProfile
import pstats

filename = basename(__file__)


def run_simulation(new_config, nash, mono, maxit):
    """ Runs a single simulation and computes collusion quotient moving average. """
    market, states = SIMULATOR.simulate(new_config)

    # Extract and process profits
    profits = np.array([state.profits for state in states])
    profits = np.mean(profits, axis=1)

    # Compute collusion quotient
    collusion_quotient_list = [lib.get_collusion_quotient(profits[i], nash, mono) for i in range(maxit)]
    
    return lib.moving_average(collusion_quotient_list, 100)


def main():
    # Initialize
    market = SIMULATOR.setup(config.defaultconfig)
    nash = np.mean(market.get_nash_profits())
    mono = np.mean(market.get_monopoly_profits())

    times = 1000
    maxit = 2000000
    new_config = config.create_config(iterations=maxit)

    # Parallel processing
    with Pool(processes=cpu_count()) as pool:
        results = pool.starmap(run_simulation, [(new_config, nash, mono, maxit)] * times)

    # Aggregate results
    ma100 = np.sum(results, axis=0) / times
    print(ma100.shape)
    # Generate x-axis
    repetitions = np.linspace(0, len(ma100), len(ma100))


    # Plot results
    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    
    filename = basename(__file__)
    plt.savefig(config.create_filepath(filename))


if __name__ == "__main__":
    config.profile_main(main,filename)