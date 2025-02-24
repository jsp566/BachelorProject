import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt

from os.path import basename
from multiprocessing import Pool, cpu_count
import cProfile
import pstats



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
    market = SIMULATOR.setup(config.defaultconfig_3_firms)
    nash = np.mean(market.get_nash_profits())
    mono = np.mean(market.get_monopoly_profits())

    times = 1000
    maxit = 1500000
    new_config = config.create_config_3(iterations=maxit)

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
    plt.xlabel('Discount factor')
    
    filename = '3 firms' + basename(__file__)
    plt.savefig(config.create_filepath(filename))

def profile_main():
    cProfile.run('main()', 'restats')
    p = pstats.Stats('restats')
    p.strip_dirs().sort_stats('cumulative').print_stats(10)
    p.strip_dirs().sort_stats('calls').print_stats(30)
    
if __name__ == "__main__":
    profile_main()
