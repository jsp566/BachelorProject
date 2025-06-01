import os
import pickle
import numpy as np
import utils.lib as lib
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime

def averaging(states, max_length, width, fun):
    results = np.zeros((max_length, width)) 
    for state in states:
        this = np.array([fun(s) for s in state])
        this = np.append(this, np.tile(np.mean(this[-100000:], axis=0), (max_length - len(this), 1)), axis=0)
        results += this / len(states)

    results = np.transpose(results)
    return results


def make_graphs(foldername, config, market, states=None, merger=False):
    save_dir = os.path.join(os.getcwd(), 'Output', 'Graphs', foldername)
    os.makedirs(save_dir, exist_ok=True)
    
    multi_product = any([f > 1 for f in config['numb_products']]) and config['numb_firms'] > 1
    true_nash_cq = lib.get_collusion_quotient(market.get_true_nash_profits(), market.get_nash_profits(), market.get_monopoly_profits())
    true_nash_prices = market.get_true_nash_prices()
    monopoly_prices = market.get_monopoly_prices()

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']


    print(f"{datetime.now()} Reading data from {foldername}...")
    if states is None:
        
        states = []
        for i in range(config['sessions']):
            with open(os.path.join(os.getcwd(), 'Output', 'Data', foldername, str(i) + ".pkl"), 'rb') as f:
                result = pickle.load(f)
        
            states.append(result)

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
    plt.figure(figsize=(10,5))
    plt.plot(range(len(ma100)), ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, foldername + "_collusion_quotient_avg.png"))

    plt.clf()
    plt.figure(figsize=(10,5))
    # Moving average cq for each product
    for i in range(len(collusion_quotients)):
        ma100=  lib.moving_average(collusion_quotients[i], 100)

        if not multi_product:
            plt.plot(range(len(ma100)), ma100, alpha = 0.75, label=f'Product {i+1}', color=colors[i])
        else:
            plt.plot(range(len(ma100)), ma100, alpha = 0.75, label=f'Product {i+1} (Firm {market.products[i].firm.index + 1})', color=colors[i])
            plt.axhline(y=true_nash_cq[i], linestyle='--', alpha = 0.75, label=f'Nash Product {i+1}', color=colors[i])
    
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, foldername + "_collusion_quotient_products.png"))
    
    
    plt.clf()

    if multi_product:
        plt.figure(figsize=(10,5))
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
        plt.figure(figsize=(10,5))
        # Moving average cq for each product
        for i in range(len(true_collusion_quotients)):
            ma100=  lib.moving_average(true_collusion_quotients[i], 100)

            if not multi_product:
                plt.plot(range(len(ma100)), ma100, alpha = 0.75, label=f'Product {i+1}', color=colors[i])
            else:
                plt.plot(range(len(ma100)), ma100, alpha = 0.75, label=f'Product {i+1} (Firm {market.products[i].firm.index + 1})', color=colors[i])
        plt.ylabel('True Collusion Quotient')
        plt.xlabel('Period')
        plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
        plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
        plt.savefig(os.path.join(save_dir, foldername + "_true_collusion_quotient_products.png"))
        plt.clf()
    plt.figure(figsize=(10,5))
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
    plt.figure(figsize=(10,5))
    # Moving average cq for each product
    for i in range(len(prices)):
        ma100=  lib.moving_average(prices[i], 100)

        if not multi_product:
            plt.plot(range(len(ma100)), ma100, alpha = 0.75, label=f'Product {i+1}', color=colors[i])
        else:
            plt.plot(range(len(ma100)), ma100, alpha = 0.75, label=f'Product {i+1} (Firm {market.products[i].firm.index + 1})', color=colors[i])
            plt.axhline(y=true_nash_prices[i], linestyle='--', alpha = 0.75, label=f'Nash Product {i+1}', color=colors[i])

    plt.axhline(y=np.mean(monopoly_prices), linestyle='--', alpha = 0.75, label='Monopoly Price', color='black')

    plt.ylabel('Prices')
    plt.xlabel('Period')
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.subplots_adjust(left=0.2, right=0.8, top=0.95)
    plt.savefig(os.path.join(save_dir, foldername + "_prices_products.png"))
    plt.clf()

    if not merger:
        plt.figure(figsize=(10,5))
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
        plt.figure(figsize=(10,5))
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

    return states