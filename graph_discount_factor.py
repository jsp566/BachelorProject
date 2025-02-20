import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
import time
from os.path import basename


def main():
    # Start
    discount_factors = np.linspace(0.0, 1.0, 20, endpoint=False)
    times = 25

    average_collusion_quotient = []
    sim_start = time.time()
    for gamma in discount_factors:
        print(f"gamma = {gamma}")
        new_config = config.create_config(discount_factor=gamma)
        sum_collusion_quotients = 0
        for i in range(times):
            print(f"i = {i}")
            start = time.time()

            market, states = SIMULATOR.simulate(new_config)


            profits = np.array([state.profits for state in states[-1000:]])

            mean = np.mean(profits)
            nash = np.mean(market.get_nash_profits())
            mono = np.mean(market.get_monopoly_profits())

            collusion_quotient = lib.get_collusion_quotient(mean, nash, mono)
            print(f"collusion_quotient = {collusion_quotient}")

            sum_collusion_quotients += collusion_quotient
            end = time.time()
            print(f"Time: {end-start}s")
        average_collusion_quotient.append(sum_collusion_quotients/times)

    sim_end = time.time()
    print(f"Total time: {sim_end-sim_start}s")
    
    #plot
    plt.plot(discount_factors, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Discount factor')
    plt.figtext(0.15, 0.85, f"Total time: {sim_end-sim_start:.2f}s", fontsize=10)
    
    filename = basename(__file__)
    plt.savefig(config.create_filepath(filename))

if __name__ == "__main__":
    main()
