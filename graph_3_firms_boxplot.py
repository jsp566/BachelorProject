import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pickle


filename =  basename(__file__)


def main():
    sessions = 100
    iterations = 10**7
    firm_count = range(2, 6 )
    parallel=True
    savedData = True

    collusion_quotients_list = []
    ticks = []

    new_config = config.create_config(sessions=sessions, iterations=iterations)

    variations = {
        "numb_firms": firm_count,
    }

    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData, variations=variations)
    

    for numb_firms in firm_count:
        collusion_quotients = []
        for i in range(sessions):
            with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, f"(('numb_firms', {numb_firms}),)_" + str(i) + ".pkl"), 'rb') as f:
                result = pickle.load(f)
            collusion_quotients.append([state.collussion_quotient for state in result[-1000:]])   
        collusion_quotients = np.array(collusion_quotients)
        collusion_quotients = np.mean(collusion_quotients, axis=(1,2))
        collusion_quotients = np.transpose(collusion_quotients)
        ticks.append(str(numb_firms) + "firms")
        collusion_quotients_list.append(collusion_quotients)

    plt.boxplot(collusion_quotients_list)
    plt.xticks(range(1, len(ticks) + 1), ticks)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Number of firms')
    plt.savefig(config.create_filepath(filename + "_boxplot"))

if __name__ == "__main__":
    config.profile_main(main,filename)
    
    