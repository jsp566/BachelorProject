import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pickle


filename =  basename(__file__).replace('.py', '')


def main():
    sessions = 100
    iterations = 10**7
    firms = 2

    output_dir = os.path.join(os.getcwd(), 'Output', 'Data')

    collusion_quotients_list = []
    lengths_list = []
    ticks = []
    file_exists = True
    for name in ['2_firms', 'assymetric2-1_one_price', 'assymetric2-1', 'assymetric2-2_one_price', 'assymetric2-2_half_price', 'assymetric2-2', 'assymetric3-1_one_price', 'assymetric2-1-1_one_price', '3_firms']:
        new_filename = f"graph_default_{name}"
        collusion_quotients = []
        lengths = []
        for i in range(sessions):
            try:
                with open(os.path.join(output_dir, new_filename, str(i) + ".pkl"), 'rb') as f:
                    result = pickle.load(f)
            except:
                
                break
            collusion_quotients.append(np.mean([state.collussion_quotient  for state in result[-100000:]]))
            lengths.append(len(result))


        collusion_quotients = np.transpose(collusion_quotients)
        lengths = np.transpose(lengths)
        ticks.append(name.replace('_', ' ').replace('one price', '(1P)').replace('half price', '(0.5P)').replace('assymetric', '').replace('2 firms', '1-1').replace('3 firms', '1-1-1'))
        collusion_quotients_list.append(collusion_quotients)
        lengths_list.append(lengths)

        firms += 1

    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', filename)
    os.makedirs(save_dir, exist_ok=True)
    plt.figure(figsize=(10,5))
    plt.boxplot(collusion_quotients_list, showmeans=True)
    plt.xticks(range(1, len(ticks) + 1), ticks)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Number of products')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_collusion_quotients.png"))
    plt.clf()

    plt.figure(figsize=(10,5))
    plt.boxplot(lengths_list)
    plt.xticks(range(1, len(ticks) + 1), ticks)
    plt.ylabel('Length of session')
    plt.xlabel('Number of products')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_lengths.png"))
    plt.clf()

    
if __name__ == "__main__":
    config.profile_main(main,filename)
    
    