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
    numb_firms = 4
    numb_products = (2, 1, 1, 1)
    parallel=True
    savedData = True

    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms, numb_products=numb_products)

    market= SIMULATOR.setup(new_config)
    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData)
    
    true_nash_cq = lib.get_collusion_quotient(market.get_true_nash_profits(), market.get_nash_profits(), market.get_monopoly_profits())
    true_nash_prices = market.get_true_nash_prices()
    monopoly_prices = market.get_monopoly_prices()


    # Collusion Quotient:
    states = []
    for i in range(sessions):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
    
        states.append(result)

    lengths = [len(state) for state in states]
    plt.hist(lengths, bins=100)
    plt.xlabel('Length of session')
    plt.ylabel('Frequency')
    plt.title('Length of session')
    plt.savefig(config.create_filepath(filename + "_lengths"))

    plt.clf()

    min_length = min(lengths)
    max_length = max(lengths)

    collusion_quotients = np.zeros((max_length, sum(numb_products)))
    true_collusion_quotients = np.zeros((max_length, sum(numb_products)))
    prices = np.zeros((max_length, sum(numb_products)))
    for result in states:
        cq = np.array([state.collussion_quotient for state in result])
        cq = np.append(cq, np.tile(np.mean(cq[-100:], axis=0), (max_length - len(cq), 1)), axis=0)
        collusion_quotients += cq / sessions

        p = np.array([state.prices for state in result])
        p = np.append(p, np.tile(np.mean(p[-100:], axis=0), (max_length - len(p), 1)), axis=0)
        prices += p / sessions

        true_cq = np.array([state.true_collussion_quotient for state in result])
        true_cq = np.append(true_cq, np.tile(np.mean(true_cq[-100:], axis=0), (max_length - len(true_cq), 1)), axis=0)
        true_collusion_quotients += true_cq / sessions

        # transpose collusion quotient shape
    collusion_quotients = np.transpose(collusion_quotients)
    prices = np.transpose(prices)
    true_collusion_quotients = np.transpose(true_collusion_quotients)

    average_collusion_quotient = np.mean(collusion_quotients, axis=0)
    average_prices = np.mean(prices, axis=0)
    average_true_collusion_quotient = np.mean(true_collusion_quotients, axis=0)

    # Moving average
    ma100=  lib.moving_average(average_collusion_quotient, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')

    plt.savefig(config.create_filepath(filename + "_ma100"))

    plt.clf()

    # Moving average

    for i in range(len(collusion_quotients)):
        ma100=  lib.moving_average(collusion_quotients[i], 100)
        repetitions = np.linspace(0, len(ma100), len(ma100))
        plt.plot(repetitions, ma100, label=f'Product {i+1}')
        plt.axhline(y=true_nash_cq[i], linestyle='--', label=f'True Nash CQ Product {i+1}')

    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.legend()
    
    plt.savefig(config.create_filepath(filename + "_ma100_products"))
    plt.clf()


    # Moving average
    ma100=  lib.moving_average(average_true_collusion_quotient, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('True Collusion Quotient')
    plt.xlabel('Period')

    plt.savefig(config.create_filepath(filename + "_ma100_true"))

    plt.clf()

    # Moving average

    for i in range(len(true_collusion_quotients)):
        ma100=  lib.moving_average(true_collusion_quotients[i], 100)
        repetitions = np.linspace(0, len(ma100), len(ma100))
        plt.plot(repetitions, ma100, label=f'Product {i+1}')
        
    plt.ylabel('True Collusion Quotient')
    plt.xlabel('Period')
    plt.legend()
    
    plt.savefig(config.create_filepath(filename + "_ma100_true_products"))
    plt.clf()



    # Moving average
    ma100=  lib.moving_average(average_prices, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('Prices')
    plt.xlabel('Period')

    plt.savefig(config.create_filepath(filename + "_ma100_prices"))

    plt.clf()

    # Moving average
    for i in range(len(prices)):
        ma100=  lib.moving_average(prices[i], 100)
        repetitions = np.linspace(0, len(ma100), len(ma100))
        plt.plot(repetitions, ma100, label=f'Product {i+1}')
        plt.axhline(y=true_nash_prices[i], linestyle='--', label=f'True Nash Prices Product {i+1}')

    plt.axhline(y=np.mean(monopoly_prices), linestyle='--', label='Monopoly Price')

    plt.ylabel('Prices')
    plt.xlabel('Period')
    plt.legend()

    plt.savefig(config.create_filepath(filename + "_ma100_prices_products"))
    plt.clf()








if __name__ == "__main__":
    config.profile_main(main,filename)
