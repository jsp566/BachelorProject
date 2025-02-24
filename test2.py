import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import time
import matplotlib.pyplot as plt
from os.path import basename
import cProfile
import pstats

filename = basename(__file__)

def main():
    # Start
    market = SIMULATOR.setup(config.defaultconfig)
    nash = np.mean(market.get_nash_profits())
    mono = np.mean(market.get_monopoly_profits())

    times = 2
    maxit = 100000
    new_config = config.create_config(iterations=maxit)
    sum_collusion_quotients = 0
    average_collusion_quotient = []
    for i in range(times):
        market, states = SIMULATOR.simulate(new_config)

    # Extract and process profits
        profits = np.array([state.profits for state in states])
        profits = np.mean(profits, axis=1)

        # Compute collusion quotient
        collusion_quotient_list = [lib.get_collusion_quotient(profits[i], nash, mono) for i in range(maxit)]
    
    ma100 = lib.moving_average(collusion_quotient_list, 100)
    print(ma100.shape)
    # Generate x-axis
    repetitions = np.linspace(0, len(ma100), len(ma100))


    # Plot results
    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.title('Collusion Quotient over time')
    plt.savefig(config.create_filepath(filename))

if __name__ == "__main__":
    config.profile_main(main,filename)
