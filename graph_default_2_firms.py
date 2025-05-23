import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pickle
import itertools


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
    

    # State frequency
    state_frec = {state: 0 for state in market.state_space}

    for i in range(sessions):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
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
 

    plt.imshow(heatmap, cmap='hot_r', interpolation='nearest', origin='lower', extent=[market.firms[0].action_space[0][0], market.firms[0].action_space[-1][0], market.firms[1].action_space[0][0], market.firms[1].action_space[-1][0]])
    plt.text(closest_nash_0[0], closest_nash_0[0], 'N', color='blue', fontsize=12, fontweight='bold', ha='center', va='center')
    plt.text(closest_mono_0[0], closest_mono_0[0], 'M', color='green', fontsize=12, fontweight='bold', ha='center', va='center')
    plt.colorbar()

    plt.ylabel('Firm 1 price')
    plt.xlabel('Firm 2 price')
    plt.savefig(config.create_filepath(filename + "_state_frec"))

    plt.clf()

    # Collusion Quotient:
    lengths = []
    collusion_quotients = []
    for i in range(sessions):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
        lengths.append(len(result))
        collusion_quotients.append([state.collussion_quotient for state in result])
    

    plt.hist(lengths, bins=100)
    plt.xlabel('Length of session')
    plt.ylabel('Frequency')
    plt.title('Length of session')
    plt.savefig(config.create_filepath(filename + "_lengths"))

    plt.clf()


    min_length = min(lengths)
    max_length = max(lengths)


    for cq in collusion_quotients:
        if len(cq) < max_length:
            cq.extend([np.mean(cq[-100:], axis=0)]*(max_length - len(cq)))
    
    
    collusion_quotients = np.array(collusion_quotients)

    average_collusion_quotient = np.mean(collusion_quotients, axis=(0,2))

    plt.plot(range(min_length), average_collusion_quotient[:min_length])
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient"))

    plt.clf()

    period = range(len(average_collusion_quotient))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient_full"))

    plt.clf()

    # Moving average
    ma100=  lib.moving_average(average_collusion_quotient, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100"))



if __name__ == "__main__":
    config.profile_main(main,filename)
