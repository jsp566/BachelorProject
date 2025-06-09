
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


def get_attributes(result, market):
    price_list = [[state.prices for state in states] for states in result]
    share_list = [[state.shares for state in states] for states in result]
    profit_list = [[state.profits for state in states] for states in result]
    collusion_quotient_list = [[state.collussion_quotient for state in states] for states in result]
    firm_share_list = [[state.firm_shares for state in states] for states in result]
    firm_profit_list = [[state.firm_profits for state in states] for states in result]
    attributes = {
         'prices': tuple(np.around(np.mean(price_list, axis=(0,1)), 3)),
         'avg_price': np.around(np.mean(price_list), 3),
         'shares': tuple(np.around(np.mean(share_list, axis=(0,1)), 3)),
         'avg_share': np.around(np.mean(share_list), 3),
         'profits': tuple(np.around(np.mean(profit_list, axis=(0,1)), 3)),
         'avg_profit': np.around(np.mean(profit_list), 3),
         'collusion_quotient': tuple(np.around(np.mean(collusion_quotient_list, axis=(0,1)), 3)),
         'avg_collusion_quotient': np.around(np.mean(collusion_quotient_list), 3),
         'other_collusion_quotient': np.around((np.mean(profit_list) - np.mean(market.get_nash_profits())) / (np.mean(market.get_monopoly_profits()) - np.mean(market.get_nash_profits())), 3),
         'firm_shares': tuple(np.around(np.mean(firm_share_list, axis=(0,1)), 3)),
         'avg_firm_share': np.around(np.mean(firm_share_list), 3),
         'firm_profits': tuple(np.around(np.mean(firm_profit_list, axis=(0,1)), 3)),
         'avg_firm_profit': np.around(np.mean(firm_profit_list), 3),
    }
    return attributes


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
        'assymetric2-1-1_one_price_true_nash',
        'assymetric2-1',
        'assymetric2-1_one_price',
        'assymetric2-1_one_price_true_nash',
        'assymetric2-2',
        'assymetric2-2_half_price',
        'assymetric2-2_one_price',
        'assymetric2-2_one_price_true_nash',
        'assymetric3-1_one_price',
        'assymetric3-1_one_price_true_nash',
        'mono',
        'mono_0_init_no_convergence',
        'mono_0_init_no_convergence_one_price',
        'mono_no_convergence',
        'mono_no_convergence_one_price',
        'mono_no_exploration',
        '2_firms_small_dif_qual',
        '2_firms_big_dif_qual',
    ]

    # Make table
    df = pd.DataFrame(columns=['Filename', 'Numb Firms', 'Numb Products', 'Avg Length', 'prices', 'avg_price', 'shares', 'avg_share', 'profits', 'avg_profit', 'collusion_quotient', 'avg_collusion_quotient', 'other_collusion_quotient', 'firm_shares', 'avg_firm_share', 'firm_profits', 'avg_firm_profit'])

    for name in filenames:
        new_filename = f"graph_default_{name}"

        with open(os.path.join(output_dir, new_filename, '_config.pkl'), 'rb') as f:
            config = pickle.load(f)
        market = SIMULATOR.setup(config)
        numb_firms = config['numb_firms']   
        product_distribution = config['numb_products']
        result = []
        lengths = []
        
        for i in range(sessions):
            with open(os.path.join(output_dir, new_filename, str(i) + ".pkl"), 'rb') as f:
                    states = pickle.load(f)
            result.append(states[-100000:])
            lengths.append(len(states))

        attributes = get_attributes(result, market)
        avg_length = np.mean(lengths)

        df.loc[len(df)] = [name, numb_firms, product_distribution, avg_length] + [attributes[key] for key in df.columns[4:]]

    df.to_latex(os.path.join(save_dir, "result_table.tex"), index=False)



if __name__ == "__main__":
    config.profile_main(main,filename)
    
    