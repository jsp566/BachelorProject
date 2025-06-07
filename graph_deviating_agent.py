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

    new_states, best_actions = market.simulate(num_periods=14, start_period=period+1, convergence=None)

    for state in new_states:
        states.append(state)

    return states


def main():
    sessions = 100
    numb_prices = 15
    new_config = config.create_config(sessions=sessions)
    output_dir = os.path.join(os.getcwd(), 'Output', 'Market')
    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', filename)
    os.makedirs(save_dir, exist_ok=True)

    input_combinations = [
        ('2_firms',0),
        ('assymetric2-1_one_price',0),
        ('assymetric2-1_one_price',1),
        ('assymetric2-2_one_price',0),
        ('3_firms',0),
        #('assymetric3-1_one_price',0),
        #('assymetric3-1_one_price',1),
        #('assymetric2-1-1_one_price',0),
        #('assymetric2-1-1_one_price',1),
    ]
    # Make table
    df = pd.DataFrame(columns=['Product distribution', 'Deviating Firm', 'Action Index', 'Average Discounted Profit with Deviation', 'Average Discounted Profit without Deviation', 'Average Deviation Profit Gain (\%)', 'Frecuency of positive deviation profit gain (\%)'])

    plt.figure(figsize=(10,5))
    for input in input_combinations:
        for action_index in range(numb_prices):
            name, firm_index = input
            new_filename = f"graph_default_{name}"
            all_states = []
            result = []
            for i in range(sessions):
                with open(os.path.join(output_dir, new_filename, str(i) + ".pkl"), 'rb') as f:
                        market = pickle.load(f)
                states = deviating_agent(market, firm_index, action_index)
                all_states.append(states)
                prices = [state.prices for state in states]
                result.append(prices)
            
            average_prices = np.mean(result, axis=0)
            

            pricedata = [[],[],[]]
            nashdata = [[],[],[]]
            longrun_data = [[],[],[]]


            for i in range(len(average_prices[0])):
                if market.products[i].firm.index == firm_index:
                    color = 'red'
                else:
                    color = 'blue'
                pricedata[0].append(average_prices[:, i])
                pricedata[1].append(f"P{i+1} F{market.products[i].firm.index} (deviating)")
                pricedata[2].append(color)

                nashdata[0].append(market.TrueNash[i])
                nashdata[1].append(f"P{i+1} Nash Price")
                nashdata[2].append(color)

                longrun_data[0].append(average_prices[0, i])
                longrun_data[1].append(f"P{i+1} Long Run Price")
                longrun_data[2].append(color)
            
            pricedata, labels, colors = graph_maker.combine_data(pricedata[0], pricedata[1], pricedata[2])
            for i in range(len(pricedata)):
                plt.plot(pricedata[i], marker='o',label=labels[i], color=colors[i])

            nashdata, nash_labels, nash_colors = graph_maker.combine_data(nashdata[0], nashdata[1], nashdata[2])
            for i in range(len(nashdata)):
                plt.axhline(y=nashdata[i], linestyle=':', label=nash_labels[i], color=nash_colors[i])

            longrun_data, longrun_labels, longrun_colors = graph_maker.combine_data(longrun_data[0], longrun_data[1], longrun_data[2])
            for i in range(len(longrun_data)):
                plt.axhline(y=longrun_data[i], linestyle='-.', label=longrun_labels[i], color=longrun_colors[i])

            plt.axhline(y=np.mean(market.Mono), linestyle='--', alpha = 0.75, label='Monopoly Price', color='black')

            plt.xlabel("Time")
            plt.ylabel("Price")
            plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
            plt.subplots_adjust(left=0.2, right=0.8, top=0.95)    
            plt.savefig(os.path.join(save_dir, f"{name}_{firm_index}_{action_index}.png"))
            plt.clf()

            # discounted profit with no deviation
            no_deviation_profit = [states[0].firm_profits[firm_index]/ (1 - config.defaultconfig['discount_factor']) for states in all_states]
            no_deviation_avg_profit = np.mean(no_deviation_profit)

            # discounted profit with deviation
            discounted_profits = []
            for states in all_states:
                profit = 0
                for i, state in enumerate(states[1:-1]):
                    profit += state.firm_profits[firm_index] * (config.defaultconfig['discount_factor'] ** i)
                profit += states[-1].firm_profits[firm_index] * (config.defaultconfig['discount_factor'] ** (i+1)) / (1 - config.defaultconfig['discount_factor'])
                discounted_profits.append(profit)
            deviation_avg_profit = np.mean(discounted_profits)
            df.loc[len(df)] = [
                name.replace('_', ' ').replace('one price', '(1P)').replace('half price', '(0.5P)').replace('assymetric', '').replace('2 firms', '1-1').replace('3 firms', '1-1-1'),
                firm_index + 1,
                action_index + 1,
                deviation_avg_profit,
                no_deviation_avg_profit,
                (deviation_avg_profit - no_deviation_avg_profit) / no_deviation_avg_profit * 100,
                np.mean([1 if discounted_profits[i] > no_deviation_profit[i] else 0 for i in range(len(discounted_profits))]) * 100
            ]
    df.to_latex(os.path.join(save_dir, 'deviating_agent_results.tex'), index=False, float_format="%.2f", escape=False)


if __name__ == "__main__":
    config.profile_main(main,filename)
    
    