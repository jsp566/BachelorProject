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

def run_simulation(new_config, nash, mono,state_frec, maxit):
    """ Runs a single simulation and computes collusion quotient moving average. """
    market, states = SIMULATOR.simulate(new_config)

    local_state_frec = {state: 0 for state in market.state_space}
    for state in states[-100000:]:
        local_state_frec[state.actions] += 1

    # Extract and process profits
    profits = np.array([state.profits for state in states])
    mean= np.mean(profits, axis=1)

    # Compute collusion quotient
    collusion_quotient= lib.get_collusion_quotient(mean, nash, mono)
    market.reset()
    return collusion_quotient, local_state_frec


def find_closest(value, action_space):
    """Finds the closest value in the given sorted action space."""
    return min(action_space, key=lambda x: abs(x - value))


def main():
    # Start
    market = SIMULATOR.setup(config.defaultconfig)
    nash = np.mean(market.get_nash_profits())
    mono = np.mean(market.get_monopoly_profits())

    times = 8
    iterations = 1000000
    state_frec = {state: 0 for state in market.state_space}
    new_config = config.create_config(iterations=iterations)

    with Pool(processes=cpu_count()) as pool:
            results = pool.starmap(run_simulation, [(new_config, nash, mono,state_frec, iterations)] * times)
    collusion_quotients, state_frequencies = zip(*results)

    sum_collusion_quotients = np.sum(collusion_quotients,axis=0)


    # State frequency
    heatmap = np.zeros((len(market.firms[0].action_space), len(market.firms[1].action_space)))
    
    # Make indexes for heatmap
    indexes = {}
    market.firms[0].action_space.sort()
    market.firms[1].action_space.sort()

    for local_frec in state_frequencies:
        for state, count in local_frec.items():
            state_frec[state] += count
    
    for state in state_frec:
        index1 = market.firms[0].action_space.index(state[0])
        index2 = market.firms[1].action_space.index(state[1])
        indexes[state] = (index1, index2)

    for state, frec in state_frec.items():
        index1, index2 = indexes[state]
        heatmap[index1, index2] = frec

    heatmap = heatmap/np.sum(heatmap)

    monopoly_prices = market.get_monopoly_prices()
    nash_prices = market.get_nash_prices()

    closest_nash_0 = find_closest(nash_prices[0], market.firms[0].action_space)
    closest_nash_1 = find_closest(nash_prices[0], market.firms[1].action_space)
    closest_mono_0 = find_closest(monopoly_prices[0], market.firms[0].action_space)
    closest_mono_1 = find_closest(monopoly_prices[0], market.firms[1].action_space)
 

    plt.imshow(heatmap, cmap='hot_r', interpolation='nearest', origin='lower', extent=[market.firms[0].action_space[0][0], market.firms[0].action_space[-1][0], market.firms[1].action_space[0][0], market.firms[1].action_space[-1][0]])
    plt.text(closest_nash_0[0], closest_nash_0[0], 'N', color='blue', fontsize=12, fontweight='bold', ha='center', va='center')
    plt.text(closest_mono_0[0], closest_mono_0[0], 'M', color='green', fontsize=12, fontweight='bold', ha='center', va='center')
    plt.colorbar()

    plt.ylabel('Firm 1 price')
    plt.xlabel('Firm 2 price')
    filename = "state_frec_" + basename(__file__)
    plt.savefig(config.create_filepath(filename))

    plt.clf()
    # Collusion Quotient:
    average_collusion_quotient = sum_collusion_quotients/times
    period = range(iterations+1)
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    filename = "collusion_quotient_" + basename(__file__)
    plt.savefig(config.create_filepath(filename))


def profile_main():
    cProfile.run('main()', 'restats')
    p = pstats.Stats('restats')
    p.strip_dirs().sort_stats('cumulative').print_stats(10)
    p.strip_dirs().sort_stats('calls').print_stats(30)
if __name__ == "__main__":
    profile_main()
