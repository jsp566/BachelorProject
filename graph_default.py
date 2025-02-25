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

def run_simulation(new_config, nash, mono,state_frec, maxit):
    """ Runs a single simulation and computes collusion quotient moving average. """
    market, states = SIMULATOR.simulate(new_config)

    local_state_frec = {state: 0 for state in market.state_space}
    for state in states[-100000:]:
        local_state_frec[state.actions] += 1

    # Extract and process profits
    profits = np.array([state.profits for state in states[-1000:]])
    mean= np.mean(profits, axis=1)

    # Compute collusion quotient
    collusion_quotient= lib.get_collusion_quotient(mean, nash, mono)
    market.reset()
    return collusion_quotient, local_state_frec




def main():
    # Start
    market = SIMULATOR.setup(config.defaultconfig)
    nash = np.mean(market.get_nash_profits())
    mono = np.mean(market.get_monopoly_profits())

    times = 1000
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

    closest_nash_0 = lib.find_closest(nash_prices[0], market.firms[0].action_space)
    closest_mono_0 = lib.find_closest(monopoly_prices[0], market.firms[0].action_space)
 

    plt.imshow(heatmap, cmap='hot_r', interpolation='nearest', origin='lower', extent=[market.firms[0].action_space[0][0], market.firms[0].action_space[-1][0], market.firms[1].action_space[0][0], market.firms[1].action_space[-1][0]])
    plt.text(closest_nash_0[0], closest_nash_0[0], 'N', color='blue', fontsize=12, fontweight='bold', ha='center', va='center')
    plt.text(closest_mono_0[0], closest_mono_0[0], 'M', color='green', fontsize=12, fontweight='bold', ha='center', va='center')
    plt.colorbar()

    plt.ylabel('Firm 1 price')
    plt.xlabel('Firm 2 price')
    plt.savefig(config.create_filepath("state_frec_" + filename))

    plt.clf()
    # Collusion Quotient:
    average_collusion_quotient = sum_collusion_quotients/times
    period = range(len(average_collusion_quotient))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath("collusion_quotient_" +filename))


if __name__ == "__main__":
    config.profile_main(main,filename)
