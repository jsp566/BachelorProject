
import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pickle
import pandas as pd


filename =  basename(__file__).replace('.py', '')



def main():
    sessions = 100
    output_dir = os.path.join(os.getcwd(), 'Output', 'Data')
    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', filename)
    os.makedirs(save_dir, exist_ok=True)

    filenames = [
        '2_firms',
        '3_firms',
        '4_firms',
        '5_firms',
        'assymetric2-1-1_one_price',
        'assymetric2-1',
        'assymetric2-1_one_price',
        'assymetric2-1_one_price_true_nash',
        'assymetric2-2',
        'assymetric2-2_half_price',
        'assymetric2-2_one_price',
        'assymetric3-1_one_price',
        'mono',
        'mono_0_init_no_convergence',
        'mono_0_init_no_convergence_one_price',
        'mono_no_convergence',
        'mono_no_convergence_one_price',
        'mono_no_exploration',
    ]

    # Make table
    df = pd.DataFrame(columns=['Filename', 'Numb Firms', 'Numb Products', 'Avg Collusion Quotient', 'Avg Length'])

    for name in filenames:
        new_filename = f"graph_default_{name}"

        with open(os.path.join(output_dir, new_filename, '_config.pkl'), 'rb') as f:
            config = pickle.load(f)

        numb_firms = config['numb_firms']   
        product_distribution = config['numb_products']
        collusion_quotients = []
        lengths = []

        for i in range(sessions):
            with open(os.path.join(output_dir, new_filename, str(i) + ".pkl"), 'rb') as f:
                    result = pickle.load(f)
            collusion_quotients.append(np.mean([state.collussion_quotient  for state in result[-100000:]]))
            lengths.append(len(result))

        avg_collusion_quotient = np.mean(collusion_quotients)
        avg_length = np.mean(lengths)

        df.loc[len(df)] = [name, numb_firms, product_distribution, avg_collusion_quotient, avg_length]

    df.to_latex(os.path.join(save_dir, "result_table.tex"), index=False)



if __name__ == "__main__":
    config.profile_main(main,filename)
    
    