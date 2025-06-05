import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
from multiprocessing import Pool, cpu_count
import os
import pickle

filename =  basename(__file__).replace('.py', '')



def main():

    # Start
    demand_function_params = [(0.01,), (0.25,), (0.75,)]
    sessions = 100
    iterations = 10**7
    numb_firms = 2
    parallel=True
    savedData = True
    
    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)

    variations = {
        "demand_function_params": demand_function_params,
    }

    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData, variations=variations)
    
    collusion_quotients_list = []
    lengths_list = []
    ticks = [] #List to store average collusion quotients
    for mu in demand_function_params:
        collusion_quotients = []
        lengths = []
        for i in range(sessions):
            with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, f"(('demand_function_params', {mu}),)_" + str(i) + ".pkl"), 'rb') as f:
                result = pickle.load(f)
            
            collusion_quotients.append(np.mean([state.collussion_quotient  for state in result[-100000:]]))
            lengths.append(len(result))


        collusion_quotients = np.transpose(collusion_quotients)
        lengths = np.transpose(lengths)
        ticks.append(str(mu[0]))
        collusion_quotients_list.append(collusion_quotients)
        lengths_list.append(lengths)
    
    #plot
    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', filename)
    os.makedirs(save_dir, exist_ok=True)
    plt.figure(figsize=(10,5))
    plt.boxplot(collusion_quotients_list, showmeans=True)
    plt.xticks(range(1, len(ticks) + 1), ticks)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Horizontal product differentiation ($\mu$)')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_collusion_quotients_boxplot.png"))
    plt.clf()

    plt.figure(figsize=(10,5))
    plt.boxplot(lengths_list)
    plt.xticks(range(1, len(ticks) + 1), ticks)
    plt.ylabel('Length of session')
    plt.xlabel('Horizontal product differentiation ($\mu$)')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_lengths_boxplot.png"))
    plt.clf()

if __name__ == "__main__":
    config.profile_main(main,filename)
