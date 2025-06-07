import os
import pickle
import numpy as np
import utils.lib as lib
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import Classes.SIMULATOR as SIMULATOR
from multiprocessing import Pool, cpu_count
import random


# disjoint set node
class Node:
    def __init__(self, data):
        self.data = data
        self.parent = self

    def find(self):
        if self.parent != self:
            self.parent = self.parent.find()
        return self.parent

    def union(self, other):
        root1 = self.find()
        root2 = other.find()
        if root1 != root2:
            if root1.data < root2.data:
                root2.parent = root1
            else:
                root1.parent = root2

    


def combine_data(data, labels, colors):
    indexes = [Node(i) for i in range(len(data))]

    # group data that is close to each other
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if np.allclose(data[i], data[j], rtol=1e-3):
                indexes[i].union(indexes[j])
    
    parents = [indexes[i].find().data for i in range(len(indexes))]
    unique_parents = list(sorted(set(parents)))

    new_data = []
    new_labels = []
    new_colors = []

    # check if any of the data is close to each other
    for parent in unique_parents:
        indices = [i for i in range(len(parents)) if parents[i] == parent]
        if len(indices) == 1:
            i = indices[0]
            new_data.append(data[i])
            new_labels.append(labels[i])
            new_colors.append(colors[i])
        else:
            # collect data
            this_data = [data[i] for i in indices]
            this_labels = [labels[i] for i in indices]
            this_colors = [colors[i] for i in indices]
            
            # average data
            new_data.append(np.mean(this_data, axis=0))
            new_labels.append("\n& ".join(this_labels))
            # mix colors
            mixed_color = np.mean([mpl.colors.to_rgb(color) for color in this_colors], axis=0)
            new_colors.append(mpl.colors.to_hex(mixed_color))


    return new_data, new_labels, new_colors
    


def averaging(states, max_length, width, fun):
    results = np.zeros((max_length, width))
    for state in states:
        this = np.array([fun(s) for s in state])
        this = np.append(this, np.tile(np.mean(this[-100000:], axis=0), (max_length - len(this), 1)), axis=0)
        results += this / len(states)

    results = np.transpose(results)
    return results


def best_actions(file_index, config, foldername, states=None):
    if states is None:
        with open(os.path.join(os.getcwd(), 'Output', 'Data', foldername, str(file_index) + ".pkl"), 'rb') as f:
            states = pickle.load(f)
    market = SIMULATOR.setup(config)
    states = [market.state_space[state.p] for state in states]

    prices = [None] * len(market.products)

    for firm in market.firms:
        action = firm.strategy.best_action(states[0].p)
        for i in range(len(firm.products)):
            prices[firm.products[i].index] = action[i]

    p = tuple(prices)
    current_state = market.state_space[p]

    best_actions = [current_state]

    for i in range(1, len(states)):
        for firm in market.firms:
            action = firm.strategy.best_action(states[i-1].p)
            for j in range(len(firm.products)):
                prices[firm.products[j].index] = action[j]

        p = tuple(prices)
        current_state = market.state_space[p]

        best_actions.append(current_state)

        for j, firm in enumerate(market.firms):

            firm.strategy.update_strategy(states[i-1], states[i].actions[j], states[i], states[i].firm_profits[j])

    if foldername:
        filename = str(file_index) + ".pkl"
        with open(os.path.join(os.getcwd(), 'Output', 'Data Best Actions', foldername, filename), 'wb') as f:
            pickle.dump(best_actions, f)


        
def make_best_actions_data(foldername, config, states=None):
    best_action_dir = os.path.join(os.getcwd(), 'Output', 'Data Best Actions')
    os.makedirs(best_action_dir, exist_ok=True)
    dirname = os.path.join(best_action_dir, foldername)
    os.makedirs(dirname, exist_ok=True)
    inputparams = [(i, config, foldername, states) for i in range(config['sessions'])]

    with Pool(processes=8) as pool:
        pool.starmap(best_actions, inputparams)

def get_states(foldername, config):
    states = []
    for i in range(config['sessions']):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', foldername, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
        states.append(result)
    return states

def make_graphs(foldername, config, market, states=None, merger=False):
    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', foldername)
    os.makedirs(save_dir, exist_ok=True)

    
    
    multi_product = any([f > 1 for f in config['numb_products']]) and config['numb_firms'] > 1
    true_nash_cq = lib.get_collusion_quotient(market.get_true_nash_profits(), market.get_nash_profits(), market.get_monopoly_profits())
    true_nash_prices = market.get_true_nash_prices()
    monopoly_prices = market.get_monopoly_prices()

    line_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    best_action_data_exists = True


    print(f"{datetime.now()} Reading data from {foldername}...")
    if states is None:
        
        states = []
        best_action_states = []
        for i in range(config['sessions']):
            with open(os.path.join(os.getcwd(), 'Output', 'Data', foldername, str(i) + ".pkl"), 'rb') as f:
                result = pickle.load(f)
        
            states.append(result)
            try: 
                with open(os.path.join(os.getcwd(), 'Output', 'Data Best Actions', foldername, str(i) + ".pkl"), 'rb') as f:
                    result = pickle.load(f)
            except Exception as e:
                best_action_data_exists = False
                

            best_action_states.append(result)
    else:
        best_action_states = []
        best_action_data_exists = False
    print(f"{datetime.now()} Making graphs for {foldername}...")
    lengths = [len(state) for state in states]
    plt.figure(figsize=(10,5))
    plt.hist(lengths, bins=25)
    plt.xlabel('Length of session')
    plt.ylabel('Frequency')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, foldername + "_lengths.png"))

    plt.clf()

    min_length = min(lengths)
    max_length = max(lengths)

    fun = lambda s: s.collussion_quotient
    collusion_quotients = averaging(states, max_length, sum(config['numb_products']), fun)

    average_collusion_quotient = np.mean(collusion_quotients, axis=0)
    ma100=  lib.moving_average(average_collusion_quotient, 100)
    
    plt.plot(range(len(ma100)), ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, foldername + "_collusion_quotient_avg.png"))

    plt.clf()


    
    # Moving average cq for each product
    data = []
    labels = []
    colors = []


    for i in range(len(collusion_quotients)):
        ma100=  lib.moving_average(collusion_quotients[i], 100)

        if not multi_product:
            data.append(ma100)
            labels.append(f'Product {i+1}')
            colors.append(line_colors[i])
        else:
            data.append(ma100)
            labels.append(f'Product {i+1} (Firm {market.products[i].firm.index + 1})')
            colors.append(line_colors[i])

    data, labels, colors = combine_data(data, labels, colors)
    
    for i in range(len(data)):
        plt.plot(range(len(data[i])), data[i], alpha = 0.75, label=labels[i], color=colors[i])
    
    
    if multi_product:
        data = []
        labels = []
        colors = []
        for i in range(len(collusion_quotients)):
            data.append(true_nash_cq[i])
            labels.append(f'Nash Product {i+1}')
            colors.append(line_colors[i])
        data, labels, colors = combine_data(data, labels, colors)
        for i in range(len(data)):
            plt.axhline(y=data[i], linestyle='--', alpha = 0.75, label=labels[i], color=colors[i])

    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, foldername + "_collusion_quotient_products.png"))
    
    
    plt.clf()

    if multi_product:
        
        fun = lambda s: s.true_collussion_quotient
        true_collusion_quotients = averaging(states, max_length, sum(config['numb_products']), fun)

        average_collusion_quotient = np.mean(true_collusion_quotients, axis=0)
        ma100=  lib.moving_average(average_collusion_quotient, 100)

        plt.plot(range(len(ma100)), ma100)
        plt.ylabel('True Collusion Quotient')
        plt.xlabel('Period')
        plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
        plt.savefig(os.path.join(save_dir, foldername + "_true_collusion_quotient_avg.png"))

        plt.clf()
        
        # Moving average cq for each product
        data = []
        labels = []
        colors = []
        for i in range(len(true_collusion_quotients)):
            ma100=  lib.moving_average(true_collusion_quotients[i], 100)
            data.append(ma100)
            labels.append(f'Product {i+1} (Firm {market.products[i].firm.index + 1})')
            colors.append(line_colors[i])
            
        data, labels, colors = combine_data(data, labels, colors)
        for i in range(len(data)):
            plt.plot(range(len(data[i])), data[i], alpha = 0.75, label=labels[i], color=colors[i])
        
        plt.ylabel('True Collusion Quotient')
        plt.xlabel('Period')
        plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
        plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
        plt.savefig(os.path.join(save_dir, foldername + "_true_collusion_quotient_products.png"))
        plt.clf()


    
    fun = lambda s: s.prices
    prices = averaging(states, max_length, sum(config['numb_products']), fun)

    avg_prices = np.mean(prices, axis=0)
    ma100=  lib.moving_average(avg_prices, 100)

    plt.plot(range(len(ma100)), ma100)
    plt.ylabel('Prices')
    plt.xlabel('Period')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, foldername + "_prices_avg.png"))

    plt.clf()
    
    # Moving average cq for each product

    data = []
    labels = []
    colors = []


    for i in range(len(prices)):
        ma100=  lib.moving_average(prices[i], 100)

        if not multi_product:
            data.append(ma100)
            labels.append(f'Product {i+1}')
            colors.append(line_colors[i])
        else:
            data.append(ma100)
            labels.append(f'Product {i+1} (Firm {market.products[i].firm.index + 1})')
            colors.append(line_colors[i])

    data, labels, colors = combine_data(data, labels, colors)
    
    for i in range(len(data)):
        plt.plot(range(len(data[i])), data[i], alpha = 0.75, label=labels[i], color=colors[i])
    
    
    if multi_product:
        data = []
        labels = []
        colors = []
        for i in range(len(true_nash_prices)):
            data.append(true_nash_prices[i])
            labels.append(f'Nash Product {i+1}')
            colors.append(line_colors[i])
        data, labels, colors = combine_data(data, labels, colors)
        for i in range(len(data)):
            plt.axhline(y=data[i], linestyle='--', alpha = 0.75, label=labels[i], color=colors[i])

    plt.axhline(y=np.mean(monopoly_prices), linestyle='--', alpha = 0.75, label='Monopoly Price', color='black')
    plt.ylabel('Prices')
    plt.xlabel('Period')
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, foldername + "_prices_products.png"))
    
    
    plt.clf()

    if not merger:
        
        fun = lambda s: s.firm_profits
        profits = averaging(states, max_length, config['numb_firms'], fun)

        avg_profits = np.mean(profits, axis=0)
        ma100=  lib.moving_average(avg_profits, 100)

        plt.plot(range(len(ma100)), ma100)
        plt.ylabel('Profits')
        plt.xlabel('Period')
        plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
        plt.savefig(os.path.join(save_dir, foldername + "_profits_avg.png"))

        plt.clf()
        
        # Moving average cq for each product
        for i in range(len(profits)):
            ma100=  lib.moving_average(profits[i], 100)
            plt.plot(range(len(ma100)), ma100, alpha = 0.75, label=f'Firm {i+1}')
            

        plt.ylabel('Profits')
        plt.xlabel('Period')
        plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
        plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
        plt.savefig(os.path.join(save_dir, foldername + "_profits_firms.png"))
        plt.clf()

    if best_action_data_exists:        
        best_action_collusion_quotients = averaging(best_action_states, max_length, sum(config['numb_products']), fun)
        best_action_average_collusion_quotient = np.mean(best_action_collusion_quotients, axis=0)
        best_action_ma100=  lib.moving_average(best_action_average_collusion_quotient, 100)
        
        plt.plot(range(len(ma100)), ma100, label='Avg CQ', color='blue', alpha=0.75)
        plt.plot(range(len(best_action_ma100)), best_action_ma100, label='Best Action CQ', color='orange', alpha=0.75)
        plt.ylabel('Collusion Quotient')
        plt.xlabel('Period')
        plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
        plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
        plt.savefig(os.path.join(save_dir, foldername + "_collusion_quotient_avg_best_action.png"))

        plt.clf()
        
        # Moving average cq for each product
        data = []
        labels = []
        colors = []


        for i in range(len(collusion_quotients)):
            ma100=  lib.moving_average(collusion_quotients[i], 100)

            if not multi_product:
                data.append(ma100)
                labels.append(f'Product {i+1}')
                colors.append(line_colors[i])
            else:
                data.append(ma100)
                labels.append(f'Product {i+1} (Firm {market.products[i].firm.index + 1})')
                colors.append(line_colors[i])
            
        data, labels, colors = combine_data(data, labels, colors)
        
        for i in range(len(data)):
            plt.plot(range(len(data[i])), data[i], alpha = 0.75, label=labels[i], color=colors[i])
        data = []
        labels = []
        colors = []


        for i in range(len(best_action_collusion_quotients)):
            ma100=  lib.moving_average(best_action_collusion_quotients[i], 100)

            if not multi_product:
                data.append(ma100)
                labels.append(f'Product {i+1} Best Action')
                colors.append(line_colors[i])
            else:
                data.append(ma100)
                labels.append(f'Product {i+1} Best Action (Firm {market.products[i].firm.index + 1})')
                colors.append(line_colors[i])

        data, labels, colors = combine_data(data, labels, colors)
        
        for i in range(len(data)):
            plt.plot(range(len(data[i])), data[i], linestyle=':', alpha = 0.75, label=labels[i], color=colors[i])
        
        
        if multi_product:
            data = []
            labels = []
            colors = []
            for i in range(len(collusion_quotients)):
                data.append(true_nash_cq[i])
                labels.append(f'Nash Product {i+1}')
                colors.append(line_colors[i])
            data, labels, colors = combine_data(data, labels, colors)
            for i in range(len(data)):
                plt.axhline(y=data[i], linestyle='--', alpha = 0.75, label=labels[i], color=colors[i])

        plt.ylabel('Collusion Quotient')
        plt.xlabel('Period')
        plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
        plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
        plt.savefig(os.path.join(save_dir, foldername + "_collusion_quotient_products.png"))
        
        
        plt.clf()

    return states