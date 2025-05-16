import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pickle
import itertools


filename =  basename(__file__).replace('.py', '')



def main():
    # Start
    sessions = 100
    iterations = 10**7
    numb_products = (2, 1)
    convergence = None
    parallel=True
    savedData = True

    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_products=numb_products, convergence=convergence)

    market= SIMULATOR.setup(new_config)

    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData)
    
    true_nash_cq = lib.get_collusion_quotient(market.get_true_nash_profits(), market.get_nash_profits(), market.get_monopoly_profits())
    true_nash_prices = market.get_true_nash_prices()
    monopoly_prices = market.get_monopoly_prices()

    # Collusion Quotient:
    
    collusion_quotients = np.zeros((iterations+1, 3))
    prices = np.zeros((iterations+1, 3))
    for i in range(sessions):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)

        collusion_quotients += np.array([state.collussion_quotient for state in result]) / sessions
        prices += np.array([state.prices for state in result]) / sessions

    # transpose collusion quotient shape
    collusion_quotients = np.transpose(collusion_quotients)
    prices = np.transpose(prices)

    period = range(iterations+1)
    plt.plot(period, np.mean(collusion_quotients, axis=0))
    plt.axhline(y=np.mean(true_nash_cq), color='r', linestyle='--', label='True Nash CQ')
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient_full"))

    plt.clf()

    # Moving average
    ma100=  lib.moving_average(np.mean(collusion_quotients, axis=0), 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.axhline(y=np.mean(true_nash_cq), color='r', linestyle='--', label='True Nash CQ')
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100_full"))
    plt.clf()


    plt.plot(period, collusion_quotients[0], label='Product 1')
    plt.plot(period, collusion_quotients[1], label='Product 2')
    plt.plot(period, collusion_quotients[2], label='Product 3')
    plt.axhline(y=true_nash_cq[0], color='r', linestyle='--', label='True Nash CQ Product 1')
    plt.axhline(y=true_nash_cq[1], color='g', linestyle='--', label='True Nash CQ Product 2')
    plt.axhline(y=true_nash_cq[2], color='b', linestyle='--', label='True Nash CQ Product 3')
    plt.legend()
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient_products"))

    plt.clf()

    # Moving average
    ma100=  lib.moving_average(collusion_quotients[0], 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))
    plt.plot(repetitions, ma100, label='Product 1')
    ma100=  lib.moving_average(collusion_quotients[1], 100)
    plt.plot(repetitions, ma100, label='Product 2')
    ma100=  lib.moving_average(collusion_quotients[2], 100)
    plt.plot(repetitions, ma100, label='Product 3')

    plt.axhline(y=true_nash_cq[0], color='r', linestyle='--', label='True Nash CQ Product 1')
    plt.axhline(y=true_nash_cq[1], color='g', linestyle='--', label='True Nash CQ Product 2')
    plt.axhline(y=true_nash_cq[2], color='b', linestyle='--', label='True Nash CQ Product 3')
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100_products"))
    plt.clf()


    # Plotting prices
    period = range(iterations+1)
    plt.plot(period, np.mean(prices, axis=0))
    plt.axhline(y=np.mean(true_nash_prices), color='r', linestyle='--', label='True Nash Prices')
    plt.axhline(y=np.mean(monopoly_prices), color='g', linestyle='--', label='Monopoly Prices')

    plt.ylabel('Prices')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_prices_full"))

    plt.clf()

    # Moving average
    ma100=  lib.moving_average(np.mean(prices, axis=0), 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.axhline(y=np.mean(true_nash_prices), color='r', linestyle='--', label='True Nash Prices')
    plt.axhline(y=np.mean(monopoly_prices), color='g', linestyle='--', label='Monopoly Prices')
    plt.ylabel('Prices')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100_prices_full"))
    plt.clf()


    plt.plot(period, prices[0], label='Product 1')
    plt.plot(period, prices[1], label='Product 2')
    plt.plot(period, prices[2], label='Product 3')
    plt.axhline(y=true_nash_prices[0], color='r', linestyle='--', label='True Nash Prices Product 1')
    plt.axhline(y=true_nash_prices[1], color='g', linestyle='--', label='True Nash Prices Product 2')
    plt.axhline(y=true_nash_prices[2], color='b', linestyle='--', label='True Nash Prices Product 3')
    plt.axhline(y=monopoly_prices[0], color='g', linestyle='--', label='Monopoly Prices Product 1')
    plt.axhline(y=monopoly_prices[1], color='g', linestyle='--', label='Monopoly Prices Product 2')
    plt.axhline(y=monopoly_prices[2], color='g', linestyle='--', label='Monopoly Prices Product 3')

    plt.legend()
    plt.ylabel('Prices')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_prices_products"))

    plt.clf()

    # Moving average
    ma100=  lib.moving_average(prices[0], 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))
    plt.plot(repetitions, ma100, label='Product 1')
    ma100=  lib.moving_average(prices[1], 100)
    plt.plot(repetitions, ma100, label='Product 2')
    ma100=  lib.moving_average(prices[2], 100)
    plt.plot(repetitions, ma100, label='Product 3')

    plt.axhline(y=true_nash_prices[0], color='r', linestyle='--', label='True Nash Prices Product 1')
    plt.axhline(y=true_nash_prices[1], color='g', linestyle='--', label='True Nash Prices Product 2')
    plt.axhline(y=true_nash_prices[2], color='b', linestyle='--', label='True Nash Prices Product 3')
    plt.axhline(y=monopoly_prices[0], color='g', linestyle='--', label='Monopoly Prices Product 1')
    plt.axhline(y=monopoly_prices[1], color='g', linestyle='--', label='Monopoly Prices Product 2')
    plt.axhline(y=monopoly_prices[2], color='g', linestyle='--', label='Monopoly Prices Product 3')

    plt.ylabel('Prices')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100_prices_products"))
    plt.clf()



if __name__ == "__main__":
    config.profile_main(main,filename)
