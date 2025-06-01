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
    numb_firms = 4
    parallel=True
    savedData = True

    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)
    SIMULATOR.fix_config(new_config)
    market= SIMULATOR.setup(new_config)
    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData)
    
    states = graph_maker.make_graphs(filename, new_config, market)

    # Special graph
    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', filename)
    collusion_quotients = [[state.collussion_quotient for state in result] for result in states]

    converged = []
    not_converged = []

    for cq in collusion_quotients:
        mean_cq = np.mean(cq[-100000:])
        if len(cq) < iterations:
            converged.append(mean_cq)
        else:
            not_converged.append(mean_cq)
    plt.figure(figsize=(10,5))
    plt.boxplot([converged,not_converged], showmeans=True)
    plt.xticks([1, 2], ['Converged', 'Not Converged'])
    plt.ylabel('Collusion Quotient')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_boxplot.png"))
    plt.clf()





if __name__ == "__main__":
    config.profile_main(main,filename)
