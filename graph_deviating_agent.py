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
        ('assymetric2-2_one_price',None),
        ('3_firms',None),

        ('assymetric3-1_one_price',0),
        ('assymetric3-1_one_price',1),
        ('assymetric2-1-1_one_price',0),
        ('assymetric2-1-1_one_price',[1,2]),

        ('assymetric2-1_one_price_true_nash',0),
        ('assymetric2-1_one_price_true_nash',1),
        ('assymetric2-2_one_price_true_nash',None),
        ('assymetric3-1_one_price_true_nash',0),
        ('assymetric3-1_one_price_true_nash',1),
        ('assymetric2-1-1_one_price_true_nash',0),
        ('assymetric2-1-1_one_price_true_nash',[1,2]),

    ]
    # Make table
    df = pd.DataFrame(columns=['Product distribution', 'Deviating Firm', 'Action Index', 'Average Discounted Profit with Deviation', 'Average Discounted Profit without Deviation', 'Average Deviation Profit Gain (\%)', 'Frecuency of positive deviation profit gain (\%)'])
    other_df = pd.DataFrame(columns=['Product distribution', 'Deviating Firm', 'Action Index', 'Preshock Price Index', 'Frequency of Preshock Price Index (\%)', 'Average Discounted Profit with Deviation', 'Average Discounted Profit without Deviation', 'Average Deviation Profit Gain (\%)', 'Frecuency of positive deviation profit gain (\%)'])
    plt.figure(figsize=(10,5))
    for input_param in input_combinations:
        name, input_firm_index = input_param
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

    
        for action_index in range(numb_prices):
            
            all_states = []
            for f_index in real_firm_indexes:
            
                inputparams = [(i, output_dir, new_filename, f_index, action_index) for i in range(sessions)]
                with Pool(processes=cpu_count()-2) as pool:
                    result = pool.starmap(deviation_function, inputparams)
                all_states.append(result)

            # all_states: deviating agent, session index, period index, state


            deviation_prices = np.mean([[state.actions[firm_index] for state in states] for i, firm_index in enumerate(real_firm_indexes) for states in all_states[i]], axis=(0,2))
            deviation_nash_price = np.mean([market.TrueNash[product.index] for firm_index in real_firm_indexes for product in market.firms[firm_index].products])
            deviation_longrun_price = np.mean([states[0].actions[firm_index] for i, firm_index in enumerate(real_firm_indexes) for states in all_states[i]])

            non_deviation_prices = np.mean([[[state.actions[i] for i in range(len(market.firms)) if i != firm_index] for state in states] for i, firm_index in enumerate(real_firm_indexes) for states in all_states[i]], axis=(0,2,3))
            non_deviation_nash_price = np.mean([[market.TrueNash[product.index] for i in range(len(market.firms)) for product in market.firms[i].products if i != firm_index] for firm_index in real_firm_indexes])
            non_deviation_longrun_price = np.mean([[states[0].actions[i] for i in range(len(market.firms)) if i != firm_index] for i, firm_index in enumerate(real_firm_indexes) for states in all_states[i]])

            price_labels = [f'F{input_firm_index+1} (deviating)', 'Other Firm(s)']
            nash_labels = [f'F{input_firm_index+1} Nash Price', 'Nash Price']
            longrun_labels = [f'F{input_firm_index+1} Long Run Price', f'Long Run Price']
            colors = ['red', 'blue']



            pricedata, labels, colors = graph_maker.combine_data([deviation_prices, non_deviation_prices], price_labels, colors)
            for i in range(len(pricedata)):
                plt.plot(pricedata[i], marker='o',label=labels[i], color=colors[i])

            nashdata, nash_labels, nash_colors = graph_maker.combine_data([deviation_nash_price, non_deviation_nash_price], nash_labels, colors)
            for i in range(len(nashdata)):
                plt.axhline(y=nashdata[i], linestyle=':', label=nash_labels[i], color=nash_colors[i])

            longrun_data, longrun_labels, longrun_colors = graph_maker.combine_data([deviation_longrun_price, non_deviation_longrun_price], longrun_labels, colors)
            for i in range(len(longrun_data)):
                plt.axhline(y=longrun_data[i], linestyle='-.', label=longrun_labels[i], color=longrun_colors[i])

            plt.axhline(y=np.mean(market.Mono), linestyle='--', alpha = 0.75, label='Monopoly Price', color='black')

            plt.xlabel("Time")
            plt.ylabel("Price")
            plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
            plt.subplots_adjust(left=0.2, right=0.8, top=0.95)    
            plt.savefig(os.path.join(save_dir, f"{name}_{input_firm_index}_{action_index}.png"))
            plt.clf()

            # preshock price index
                        
            preshock_price_index = [sorted(list(market.firms[firm_index].products[0].pricerange)).index(states[0].actions[firm_index][0]) for i, firm_index in enumerate(real_firm_indexes) for states in all_states[i]]
            unique_preshock_price_index = sorted(list(set(preshock_price_index)))

            deviation_firm_state_profits = [[state.firm_profits[firm_index] for state in states] for i, firm_index in enumerate(real_firm_indexes) for states in all_states[i]]
            # discounted profit with no deviation
            no_deviation_profit = [session_profits[0]/ (1 - config.defaultconfig['discount_factor']) for session_profits in deviation_firm_state_profits]
            no_deviation_avg_profit = np.mean(no_deviation_profit)

            # discounted profit with deviation

            discounted_profits = []
            for session_profits in deviation_firm_state_profits:
                sum_profit = 0
                for i, profit in enumerate(session_profits[1:-1]):
                    sum_profit += profit * (config.defaultconfig['discount_factor'] ** i)
                sum_profit += session_profits[-1] * (config.defaultconfig['discount_factor'] ** (i+1)) / (1 - config.defaultconfig['discount_factor'])
                discounted_profits.append(sum_profit)
            deviation_avg_profit = np.mean(discounted_profits)
            df.loc[len(df)] = [
                name.replace('_', ' ').replace('one price', '').replace('half price', '').replace('assymetric', '').replace('2 firms', '1-1').replace('3 firms', '1-1-1'),
                input_firm_index + 1,
                action_index + 1,
                deviation_avg_profit,
                no_deviation_avg_profit,
                (deviation_avg_profit - no_deviation_avg_profit) / no_deviation_avg_profit * 100,
                np.mean([1 if discounted_profits[i] > no_deviation_profit[i] else 0 for i in range(len(discounted_profits))]) * 100
            ]
            for price_index in unique_preshock_price_index:
                preshock_price_freq = preshock_price_index.count(price_index) / len(preshock_price_index) * 100
                # get indexes of states where the preshock price index is equal to price_index
                indexes = [i for i, x in enumerate(preshock_price_index) if x == price_index]
                deviation_avg_profit = np.mean([discounted_profits[i] for i in indexes])
                no_deviation_avg_profit = np.mean([no_deviation_profit[i] for i in indexes])

                other_df.loc[len(other_df)] = [
                    name.replace('_', ' ').replace('one price', '(1P)').replace('half price', '(0.5P)').replace('assymetric', '').replace('2 firms', '1-1').replace('3 firms', '1-1-1'),
                    input_firm_index + 1,
                    action_index + 1,
                    price_index + 1,
                    preshock_price_freq,
                    deviation_avg_profit,
                    no_deviation_avg_profit,
                    (deviation_avg_profit - no_deviation_avg_profit) / no_deviation_avg_profit * 100,
                    np.mean([1 if discounted_profits[i] > no_deviation_profit[i] else 0 for i in indexes]) * 100
                ]
    df.to_latex(os.path.join(save_dir, 'deviating_agent_results.tex'), index=False, float_format="%.2f", escape=False)
    other_df.to_latex(os.path.join(save_dir, 'deviating_agent_other_results.tex'), index=False, float_format="%.2f", escape=False)


if __name__ == "__main__":
    config.profile_main(main,filename)
    
    