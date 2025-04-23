import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename


filename =  basename(__file__).replace('.py', '')



def main():
    # Start
    sessions = 2
    iterations = 10000000

    new_config = config.create_config(sessions=sessions, iterations=iterations)

    market, results = SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=False, savedData=False)


    # State frequency
    state_frec = {state: 0 for state in market.state_space}

    for result in results:
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
    min_length = min(len(result) for result in results)
    collusion_quotients = [[state.collussion_quotient for state in result[:min_length]] for result in results]
    
    collusion_quotients = np.array(collusion_quotients)

    average_collusion_quotient = np.mean(collusion_quotients, axis=(0,2))

    period = range(len(average_collusion_quotient))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient"))


if __name__ == "__main__":
    config.profile_main(main,filename)
