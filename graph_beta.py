import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import time
import matplotlib.pyplot as plt
from os.path import basename
import cProfile
import pstats
import pickle
import os

filename = basename(__file__).replace('.py', '')

def main():
    # Start
    alpha = 0.15
    betas = np.linspace(4*10**-7, 4*10**-6, 4, endpoint=False) #SET Beta values
    sessions = 100
    iterations = 10**8
    numb_firms = 3
    parallel=True
    savedData = True
    
    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)
    market= SIMULATOR.setup(new_config)
    variations = {
        "exploration_rate_params": [(beta,) for beta in betas]
    }

    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData, variations=variations)
    collusion_quotients_list = []
    lengths_list = []
    ticks = []
    for beta in betas:
        collusion_quotients = []
        lengths = []
        for i in range(sessions):
            with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, f"(('exploration_rate_params', ({beta},)),)_" + str(i) + ".pkl"), 'rb') as f:
                result = pickle.load(f)
            collusion_quotients.append(np.mean([state.collussion_quotient  for state in result[-100000:]]))
            lengths.append(len(result))

        collusion_quotients = np.transpose(collusion_quotients)
        lengths = np.transpose(lengths)
        ticks.append(str(beta))
        collusion_quotients_list.append(collusion_quotients)
        lengths_list.append(lengths)


    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', filename)
    os.makedirs(save_dir, exist_ok=True)
    plt.figure(figsize=(10,5))
    plt.boxplot(collusion_quotients_list, showmeans=True)
    plt.xticks(range(1, len(ticks) + 1), ticks)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Value of Beta')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_collusion_quotients.png"))
    plt.clf()

    plt.figure(figsize=(10,5))
    plt.boxplot(lengths_list)
    plt.xticks(range(1, len(ticks) + 1), ticks)
    plt.ylabel('Length of session')
    plt.xlabel('Number of firms')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_lengths.png"))
    plt.clf()

    
if __name__ == "__main__":
    config.profile_main(main,filename)