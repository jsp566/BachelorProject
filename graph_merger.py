import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import pickle
import os
from copy import deepcopy


filename =  basename(__file__).replace('.py', '')


def new_session(i, market, iterations, start_period = 1, convergence = None, foldername = None, variation = None):
    new_market = deepcopy(market)
    
    before = new_market.simulate(iterations, start_period=start_period, convergence=convergence)
    new_market.merge(0,1)
    after = new_market.simulate(iterations, start_period=start_period, convergence=convergence)
    if foldername:
        filename = str(i) + ".pkl"
        if variation:

            filename = str(variation) + "_" + filename
            
        with open(os.path.join(os.getcwd(), 'Output', 'Data', foldername, filename), 'wb') as f:
            pickle.dump(before + after, f)
    return


def main():
    # Start
    sessions = 100
    iterations = 10**7
    numb_firms = 3
    parallel=True
    savedData = True
    


    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)
    market= SIMULATOR.setup(new_config)
    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData, session=new_session)
    # Collusion Quotient:

    true_nash_cq = lib.get_collusion_quotient(market.get_true_nash_profits(), market.get_nash_profits(), market.get_monopoly_profits())
    true_nash_prices = market.get_true_nash_prices()
    monopoly_prices = market.get_monopoly_prices()

    print("Reading data")
    states = []
    for i in range(sessions):
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
    
        states.append(result)

    lengths = [len(state) for state in states]
    min_length = min(lengths)
    max_length = max(lengths)

    collusion_quotients = []
    mergerperiods = [next(i for i, state in enumerate(result) if len(state.firm_profits) < numb_firms) for result in states]

    collusion_quotients = np.zeros((max_length, 3))
    prices = np.zeros((max_length, 3))
    for result in states:
        cq = np.array([state.collussion_quotient for state in result])
        end = np.tile(np.mean(cq[-100:], axis=0), (max_length - len(cq), 1))

        cq = np.append(cq, end, axis=0)
        p = np.array([state.prices for state in result])
        p = np.append(p, np.tile(np.mean(p[-100:], axis=0), (max_length - len(p), 1)), axis=0)
        collusion_quotients += cq / sessions
        prices += p / sessions

    collusion_quotients = np.transpose(collusion_quotients)
    prices = np.transpose(prices)

    plt.hist(lengths, bins=100)
    plt.xlabel('Length of session')
    plt.ylabel('Frequency')
    plt.title('Length of session')
    plt.savefig(config.create_filepath(filename + "_totallengths"))

    plt.clf()

    

    average_collusion_quotient = np.mean(collusion_quotients, axis=0)
    average_prices = np.mean(prices, axis=0)

    plt.plot(range(min_length), average_collusion_quotient[:min_length])
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient"))

    plt.clf()


    period = range(len(average_collusion_quotient))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient_full"))

    plt.clf()

    # Moving average
    ma100=  lib.moving_average(average_collusion_quotient, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100"))
    plt.clf()

    ma100=  lib.moving_average(average_prices, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('Prices')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100_prices"))
    plt.clf()

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





    print("Getting mergers periods data")

    plt.hist(mergerperiods, bins=100)
    plt.xlabel('Periods until merger')
    plt.ylabel('Frequency')
    plt.title('Periods until merger')
    plt.savefig(config.create_filepath(filename + "_periods_before_merger"))

    plt.clf()

    plt.hist([lengths[i] - mergerperiods[i] for i in range(len(mergerperiods))], bins=100)
    plt.xlabel('Periods after merger')
    plt.ylabel('Frequency')
    plt.title('Periods after merger')
    plt.savefig(config.create_filepath(filename + "_periods_after_merger"))

    plt.clf()

    print("Calculating lengths of collusion quotients")
    

    new_states = [None] * sessions
    for i in range(sessions):
        new_states[i] = states[i][mergerperiods[i]-10**5:]

    lengths = [len(c) for c in new_states]
    min_length = min(lengths)
    max_length = max(lengths)

    print("Extending data")
    collusion_quotients = np.zeros((max_length, 3))
    prices = np.zeros((max_length, 3))
    for result in new_states:
        cq = np.array([state.collussion_quotient for state in result])
        end = np.tile(np.mean(cq[-100:], axis=0), (max_length - len(cq), 1))

        cq = np.append(cq, end, axis=0)
        p = np.array([state.prices for state in result])
        p = np.append(p, np.tile(np.mean(p[-100:], axis=0), (max_length - len(p), 1)), axis=0)
        collusion_quotients += cq / sessions
        prices += p / sessions

    collusion_quotients = np.transpose(collusion_quotients)
    prices = np.transpose(prices)

    average_collusion_quotient = np.mean(collusion_quotients, axis=0)
    average_prices = np.mean(prices, axis=0)

    plt.plot(range(min_length), average_collusion_quotient[:min_length])
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient_merged"))

    plt.clf()

    period = range(len(average_collusion_quotient))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient_merged_full"))

    plt.clf()

    # Moving average
    ma100=  lib.moving_average(average_collusion_quotient, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100_merged"))
    plt.clf()
        
    ma100=  lib.moving_average(average_prices, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('Prices')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100_prices_merged"))
    plt.clf()
        
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
    

    plt.savefig(config.create_filepath(filename + "_ma100_products_merged"))
    plt.clf()

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
    

    plt.savefig(config.create_filepath(filename + "_ma100_prices_products_merged"))
    plt.clf()


if __name__ == "__main__":
    config.profile_main(main,filename)
