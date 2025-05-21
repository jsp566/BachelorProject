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
    firms = 2

    output_dir = os.path.join(os.getcwd(), 'Output', 'Data')

    collusion_quotients_list = []
    lengths_list = []
    ticks = []
    file_exists = True
    while file_exists:
        new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=firms)
        SIMULATOR.fix_config(new_config)
        new_filename = f"graph_default_{firms}_firms"
        try:
            with open(os.path.join(output_dir, new_filename, '_config.pkl'), 'rb') as f:
                old_config = pickle.load(f)
            assert old_config == new_config, f"Config mismatch: {old_config} != {new_config}"
        except:
            file_exists = False
            break
        collusion_quotients = []
        lengths = []
        for i in range(sessions):
            try:
                with open(os.path.join(output_dir, new_filename, str(i) + ".pkl"), 'rb') as f:
                    result = pickle.load(f)
            except:
                file_exists = False
                break
            collusion_quotients.append(np.mean([state.collussion_quotient  for state in result[-100000:]]))
            lengths.append(len(result))


        collusion_quotients = np.transpose(collusion_quotients)
        lengths = np.transpose(lengths)
        ticks.append(str(firms) + " firms")
        collusion_quotients_list.append(collusion_quotients)
        lengths_list.append(lengths)

        firms += 1

    plt.boxplot(collusion_quotients_list, showmeans=True)
    plt.xticks(range(1, len(ticks) + 1), ticks)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Number of firms')
    
    plt.savefig(config.create_filepath(filename + "_boxplot"))
    plt.clf()

    plt.boxplot(lengths_list)
    plt.xticks(range(1, len(ticks) + 1), ticks)
    plt.ylabel('Length of session')
    plt.xlabel('Number of firms')
    plt.savefig(config.create_filepath(filename + "_lengths_boxplot"))
    plt.clf()
if __name__ == "__main__":
    config.profile_main(main,filename)
    
    