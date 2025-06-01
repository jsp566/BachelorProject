import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pickle
import itertools
import graph_maker

filename =  basename(__file__).replace('.py', '')



def main():
    # Start
    sessions = 100 
    iterations = 10**7
    extra = 0.1
    parallel=True
    savedData = True

    new_config = config.create_config(sessions=sessions, iterations=iterations, extra=extra)

    market= SIMULATOR.setup(new_config)
    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData)
    
    states = graph_maker.make_graphs(filename, new_config, market)


    # State frequency
    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', filename)
    state_frec = {state: 0 for state in market.state_space}

    for result in states:
        for state in result[-100000:]:
            state_frec[state.p] += 1

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

    monopoly_prices = market.get_monopoly_prices()
    nash_prices = market.get_nash_prices()

    closest_nash_0 = lib.find_closest(nash_prices[0], market.firms[0].action_space)
    closest_mono_0 = lib.find_closest(monopoly_prices[0], market.firms[0].action_space)
 
    plt.figure(figsize=(10,5))
    plt.imshow(heatmap, cmap='hot_r', interpolation='nearest', origin='lower', extent=[market.firms[0].action_space[0][0], market.firms[0].action_space[-1][0], market.firms[1].action_space[0][0], market.firms[1].action_space[-1][0]])
    plt.text(closest_nash_0[0], closest_nash_0[0], 'N', color='blue', fontsize=12, fontweight='bold', ha='center', va='center')
    plt.text(closest_mono_0[0], closest_mono_0[0], 'M', color='green', fontsize=12, fontweight='bold', ha='center', va='center')
    plt.colorbar()

    plt.ylabel('Firm 1 price')
    plt.xlabel('Firm 2 price')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_state_frec.png"))

    plt.clf()




if __name__ == "__main__":
    config.profile_main(main,filename)
