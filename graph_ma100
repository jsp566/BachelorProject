import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
import time
from os.path import basename


def main():
    # Start
    times = 25
    maxit = 1500000

    average_collusion_quotient = []
    new_config = config.create_config(iterations=maxit)
    sum_collusion_quotients = 0
    collusion_quotient_list = []
    sim_start = time.time()
        for i in range(times):
    
            market, states = SIMULATOR.simulate(new_config)
            profits = np.array([state.profits for state in states])
            profits = np.mean(profits, axis=1)
            nash = np.mean(market.get_nash_profits())
            mono = np.mean(market.get_monopoly_profits())

            for i in range(maxit):
                collusion_quotient = lib.get_collusion_quotient(profits[i], nash, mono)
                collusion_quotient_list.append(collusion_quotient)
            ma100 += np.array(lib.moving_average(collusion_quotient_list, 100))

    #linear space length of ma100
    repetitions = np.linspace(0, len(ma100), len(ma100))
    
    sim_end = time.time()

    print("Simulation time: ", sim_end - sim_start)
    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Discount factor')
    plt.figtext(0.15, 0.85, f"Total time: {sim_end-sim_start:.2f}s", fontsize=10)
    plt.show()
    filename = basename(__file__)
    plt.savefig(config.create_filepath(filename))


if __name__ == "__main__":
    main()