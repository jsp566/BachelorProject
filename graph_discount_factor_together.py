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
    discount_factors = np.linspace(0.0, 1.0, 25, endpoint=False)
    output_dir = os.path.join(os.getcwd(), 'Output', 'Data')

    collusion_quotients_list = []
    lengths_list = []
    ticks = []
    file_exists = True

    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', filename)
    os.makedirs(save_dir, exist_ok=True)
    plt.figure(figsize=(10,5))
    for name in ['', '_multifirm', '_multiproduct']:
        new_filename = f"graph_discount_factor{name}"
        average_collusion_quotient = [] #List to store average collusion quotients
        for gamma in discount_factors:
            gammacollusion_quotients = []
            for i in range(sessions):
                with open(os.path.join(os.getcwd(), 'Output', 'Data', new_filename, f"(('discount_factor', {gamma}),)_" + str(i) + ".pkl"), 'rb') as f:
                    result = pickle.load(f)
                
                collussion_quotients = [state.collussion_quotient for state in result[-100000:]]
                gammacollusion_quotients.append(np.mean(collussion_quotients))
            average_collusion_quotient.append(np.mean(gammacollusion_quotients))
        plt.plot(discount_factors, average_collusion_quotient, label=name.replace('_', ' ').strip())

    plt.ylabel('Collusion Quotient')
    plt.xlabel('Discount factor')
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, filename + "_collusion_quotients.png"))


    
if __name__ == "__main__":
    config.profile_main(main,filename)
    
    