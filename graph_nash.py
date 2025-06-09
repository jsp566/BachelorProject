import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pandas as pd
import pickle
import utils.graph_maker as graph_maker
from multiprocessing import Pool, cpu_count
from datetime import datetime

filename =  basename(__file__).replace('.py', '')


def deviating_agent(market, firm_index, action_index):
    states = [market.current_state]
    period = 10**7 +1

    prices = [None] * len(market.products)

    # set prices 
    for firm in market.firms:
        action = firm.get_action(market.current_state, period)
        for i in range(len(firm.products)):
            prices[firm.products[i].index] = action[i]

    # set deviating agent's price
    for product in market.firms[firm_index].products:
        prices[product.index] = product.pricerange[action_index]

    p = tuple(prices)

    new_state = market.state_space[p]
    for i in range(len(market.firms)):
        market.firms[i].update_strategy(market.current_state, new_state, new_state.firm_profits[i])

    market.current_state = new_state
    states.append(market.current_state)

    new_states, best_actions = market.simulate(num_periods=49, start_period=period+1, convergence=None)

    for state in new_states:
        states.append(state)

    return states


def deviation_function(i, output_dir, new_filename, firm_index, action_index):
    with open(os.path.join(output_dir, new_filename, str(i) + ".pkl"), 'rb') as f:
            market = pickle.load(f)
    states = deviating_agent(market, firm_index, action_index)
    return states


def parallel_function(session_index, numb_prices, output_dir, new_filename, firm_index, market):
    print(f"{datetime.now()} Session {session_index} Firm {firm_index}")
    inputparams = [(session_index, output_dir, new_filename, firm_index, action_index) for action_index in range(numb_prices)]

    all_states = [deviation_function(*params) for params in inputparams]


    # preshock price index
    preshock_price_index = sorted(list(market.firms[firm_index].products[0].pricerange)).index(all_states[0][0].actions[firm_index][0])

    

    # discounted profit with no deviation
    no_deviation_profit = all_states[0][0].firm_profits[firm_index]/ (1 - config.defaultconfig['discount_factor'])


    # discounted profit with deviation
    discounted_profits = []
    for states in all_states:
        profit = 0
        for i, state in enumerate(states[1:-1]):
            profit += state.firm_profits[firm_index] * (config.defaultconfig['discount_factor'] ** i)
        profit += states[-1].firm_profits[firm_index] * (config.defaultconfig['discount_factor'] ** (i+1)) / (1 - config.defaultconfig['discount_factor'])
        discounted_profits.append(profit)
    profitability = [profit > no_deviation_profit for profit in discounted_profits]
    is_nash = not any([profitability[i] and i != preshock_price_index for i in range(len(profitability))])


    return preshock_price_index, is_nash, profitability

def main():
    sessions = 100
    numb_prices = 15
    
    data_dir = os.path.join(os.getcwd(), 'Output', 'Data')
    output_dir = os.path.join(os.getcwd(), 'Output', 'Market')
    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', filename)
    os.makedirs(save_dir, exist_ok=True)

    input_combinations = [
        ('2_firms',None),
        ('assymetric2-1_one_price',0),
        ('assymetric2-1_one_price',1),
        #('assymetric2-2_one_price',None),
        ('3_firms',None),
        #('assymetric3-1_one_price',0),
        #('assymetric3-1_one_price',1),
        #('assymetric2-1-1_one_price',0),
        #('assymetric2-1-1_one_price',[1,2]),

        ('assymetric2-1_one_price_true_nash',0),
        ('assymetric2-1_one_price_true_nash',1),
        #('assymetric2-2_one_price_true_nash',None),
        #('assymetric3-1_one_price_true_nash',0),
        #('assymetric3-1_one_price_true_nash',1),
        #('assymetric2-1-1_one_price_true_nash',0),
        #('assymetric2-1-1_one_price_true_nash',[1,2]),

    ]
    # Make table
    nash_df = pd.DataFrame(columns=['Product distribution', 'Deviating Firm', 'Nash Frequency (\%)'])
    pre_price_nash_df = pd.DataFrame(columns=['Product distribution', 'Deviating Firm', 'Preshock Price Index', 'Frequency of Preshock Price Index (\%)', 'Nash Frequency (\%)'])
    profitability_df = pd.DataFrame(columns=['Product distribution', 'Deviating Firm', 'Preshock Price Index', 'Frequency of Preshock Price Index (\%)', 'Nash Frequency (\%)', 'Action Index', 'Profitability Frequency (\%)'])
    plt.figure(figsize=(10,5))
    for input in input_combinations:
        name, input_firm_index = input
        print(f"{datetime.now()} {name}")
        new_filename = f"graph_default_{name}"
        with open(os.path.join(data_dir, new_filename, '_config.pkl'), 'rb') as f:
            old_config = pickle.load(f)
            SIMULATOR.fix_config(old_config)
        market = SIMULATOR.setup(old_config)

        

        if input_firm_index is not None:
            if isinstance(input_firm_index, list):
                real_firm_indexes = input_firm_index
                input_firm_index = real_firm_indexes[0]
            else:
                real_firm_indexes = [input_firm_index]
        else:
            input_firm_index = -1
            real_firm_indexes = list(range(len(market.firms)))
        input_params = [(session_index, numb_prices, output_dir, new_filename, firm_index, market) for firm_index in real_firm_indexes for session_index in range(sessions)]
        print(len(input_params), "input params")
        with Pool(processes=cpu_count()-2) as pool:
            results = pool.starmap(parallel_function, input_params)

        preshock_price_index_list = [result[0] for result in results]
        nash_list = [result[1] for result in results]
        profitability_list = [result[2] for result in results]
        

        unique_preshock_price_index = sorted(list(set(preshock_price_index_list)))
        nash_df.loc[len(nash_df)] = [
             name.replace('_', ' ').replace('one price', '').replace('half price', '').replace('assymetric', '').replace('2 firms', '1-1').replace('3 firms', '1-1-1'),
                input_firm_index + 1,
                np.mean(nash_list) * 100
        ]

        for preshock_price_index in unique_preshock_price_index:
            preshock_price_freq = preshock_price_index_list.count(preshock_price_index) / len(preshock_price_index_list) * 100
            indexes = [i for i, x in enumerate(preshock_price_index_list) if x == preshock_price_index]
            avg_nash = np.mean([nash_list[i] for i in indexes]) * 100
            pre_price_nash_df.loc[len(pre_price_nash_df)] = [
                name.replace('_', ' ').replace('one price', '').replace('half price', '').replace('assymetric', '').replace('2 firms', '1-1').replace('3 firms', '1-1-1'),
                input_firm_index + 1,
                preshock_price_index,
                preshock_price_freq,
                avg_nash
            ]

            for action_index in range(numb_prices):
                profitability_freq = np.mean([profitability_list[i][action_index] for i in indexes]) * 100
                profitability_df.loc[len(profitability_df)] = [
                    name.replace('_', ' ').replace('one price', '').replace('half price', '').replace('assymetric', '').replace('2 firms', '1-1').replace('3 firms', '1-1-1'),
                    input_firm_index + 1,
                    preshock_price_index,
                    preshock_price_freq,
                    avg_nash,
                    action_index + 1,
                    profitability_freq
                ]
    nash_df.to_latex(os.path.join(save_dir, 'deviating_agent_nash_results.tex'), index=False, float_format="%.2f", escape=False)
    pre_price_nash_df.to_latex(os.path.join(save_dir, 'deviating_agent_pre_price_nash_results.tex'), index=False, float_format="%.2f", escape=False)
    profitability_df.to_latex(os.path.join(save_dir, 'deviating_agent_profitability_results.tex'), index=False, float_format="%.2f", escape=False)

if __name__ == "__main__":
    config.profile_main(main,filename)
    
    