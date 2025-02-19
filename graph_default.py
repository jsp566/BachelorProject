import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import time
import matplotlib.pyplot as plt

from os.path import basename


def main():
    # Start
    market = SIMULATOR.setup(config.defaultconfig)
    nash = np.mean(market.get_nash_profits())
    mono = np.mean(market.get_monopoly_profits())

    times = 100
    iterations = 1000000

    state_frec = {state: 0 for state in market.state_space}

    sum_collusion_quotients = 0
    start = time.time()
    for i in range(times):
        
        states = market.simulate(iterations)

        # state frequency
        for state in states[-100000:]:
            state_frec[state.actions] += 1


        # Collusion Quotient:
        profits = np.array([state.profits for state in states])
        mean = np.mean(profits, axis=1)
        collusion_quotient = lib.get_collusion_quotient(mean, nash, mono)
        sum_collusion_quotients += collusion_quotient

        market.reset()
        
    end = time.time()
    print(f"Time: {end-start}s")

    # State frequency
    heatmap = np.zeros((len(market.firms[0].action_space), len(market.firms[1].action_space)))
    
    # Make indexes for heatmap
    indexes = {}
    market.firms[0].action_space.sort()
    market.firms[1].action_space.sort()

    for state in state_frec:
        index1 = market.firms[0].action_space.index(state[0])
        index2 = market.firms[1].action_space.index(state[1])
        indexes[state] = (index1, index2)

    for state, frec in state_frec.items():
        index1, index2 = indexes[state]
        heatmap[index1, index2] = frec

    heatmap = heatmap/np.sum(heatmap)

    plt.imshow(heatmap, cmap='hot_r', interpolation='nearest', origin='lower', extent=[market.firms[0].action_space[0][0], market.firms[0].action_space[-1][0], market.firms[1].action_space[0][0], market.firms[1].action_space[-1][0]])
    plt.colorbar()
    plt.ylabel('Firm 1 price')
    plt.xlabel('Firm 2 price')
    plt.figtext(0.15, 0.85, f"Total time: {end-start:.2f}s", fontsize=10)
    filename = "state_frec_" + basename(__file__)
    plt.savefig(config.create_filepath(filename))

    plt.clf()
    # Collusion Quotient:
    average_collusion_quotient = sum_collusion_quotients/times
    period = range(len(states))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.figtext(0.15, 0.85, f"Total time: {end-start:.2f}s", fontsize=10)
    filename = "collusion_quotient_" + basename(__file__)
    plt.savefig(config.create_filepath(filename))

if __name__ == "__main__":
    main()