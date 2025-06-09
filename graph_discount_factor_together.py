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
    discount_factors = np.linspace(0.0, 1.0, 25, endpoint=False)
    output_dir = os.path.join(os.getcwd(), 'Output', 'Data')

    collusion_quotients_list = []
    lengths_list = []
    ticks = []
    file_exists = True

    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', filename)
    os.makedirs(save_dir, exist_ok=True)


    
    labels = ['2 firms', '3 firms', '2-1 products', '2-1 products (1P)']

    collusion_quotients_list = []
    lengths_list = []

    for j, name in enumerate(['', '_multifirm', '_multiproduct','_multiproduct_one_price']):
        new_filename = f"graph_discount_factor{name}"
        average_collusion_quotient = [] #List to store average collusion quotients
        average_length = []

        for gamma in discount_factors:
            gammacollusion_quotients = []
            gammalengths = []
            for i in range(sessions):
                with open(os.path.join(os.getcwd(), 'Output', 'Data', new_filename, f"(('discount_factor', {gamma}),)_" + str(i) + ".pkl"), 'rb') as f:
                    result = pickle.load(f)
                
                collussion_quotients = [state.collussion_quotient for state in result[-100000:]]
                length = len(result)
                
                gammacollusion_quotients.append(np.mean(collussion_quotients))
                gammalengths.append(length)

            average_collusion_quotient.append(np.mean(gammacollusion_quotients))
            average_length.append(np.mean(gammalengths))

        collusion_quotients_list.append(average_collusion_quotient)
        lengths_list.append(average_length)


    plt.figure(figsize=(10,5))
    for i, label in enumerate(labels):
        plt.plot(discount_factors, collusion_quotients_list[i], label=label)

    plt.ylabel('Collusion Quotient')
    plt.xlabel('Discount factor')
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_collusion_quotients.png"))
    plt.clf()

    plt.figure(figsize=(10,5))
    for i, label in enumerate(labels):
        plt.plot(discount_factors, lengths_list[i], label=label)

    plt.ylabel('Length of session')
    plt.xlabel('Discount factor')
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_lengths.png"))
    plt.clf()



if __name__ == "__main__":
    config.profile_main(main,filename)
    
    