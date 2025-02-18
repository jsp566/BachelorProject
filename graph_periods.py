import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import time
import matplotlib.pyplot as plt

from os.path import basename


def main():
    # Start
    times = 50

    prices = []
    sum_collusion_quotients = 0
    start = time.time()
    for i in range(times):
        
        market, states = SIMULATOR.simulate(config.defaultconfig)

        prices.append([state.prices for state in states])
        profits = np.array([state.profits for state in states])
        mean = np.mean(profits, axis=1)
        nash = np.mean(market.get_nash_profits())

        mono = np.mean(market.get_monopoly_profits())

        collusion_quotient = lib.get_collusion_quotient(mean, nash, mono)

        sum_collusion_quotients += collusion_quotient
        
        
    average_collusion_quotient = sum_collusion_quotients/times



    period = range(len(states))

    end = time.time()
    print(f"Time: {end-start}s")

    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.figtext(0.15, 0.85, f"Total time: {end-start:.2f}s", fontsize=10)

    filename = basename(__file__)
    plt.savefig(config.create_filepath(filename))