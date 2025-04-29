import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename


filename =  basename(__file__)


def main():
    sessions = 1
    iterations = 10**7
    numb_firms = 2

    collusion_quotients_list = []


    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms, numb_products=2)
    market, results = SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=True, savedData=False)
    collusion_quotients = [[state.collussion_quotient for state in result[-100000:]] for result in results]
    collusion_quotients = np.array(collusion_quotients)
    collusion_quotients = np.mean(collusion_quotients, axis=(1,2))
    collusion_quotients = np.transpose(collusion_quotients)
    collusion_quotients_list.append(collusion_quotients)

    plt.boxplot(collusion_quotients_list)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Number of firms')
    plt.savefig(config.create_filepath(filename + "_boxplot"))

if __name__ == "__main__":
    config.profile_main(main,filename)
    
    