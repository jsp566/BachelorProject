import numpy as np
import lib

import SIMULATOR
import config

import time

def main():
    # Start
    discount_factors = np.linspace(0.0, 1.0, 20, endpoint=False)
    times = 25

    average_collusion_quotient = []
    for gamma in discount_factors:
        print(f"gamma = {gamma}")
        new_config = config.create_config(discount_factor=gamma)
        sum_collusion_quotients = 0
        for i in range(times):
            print(f"i = {i}")
            start = time.time()

            market, states = SIMULATOR.simulate(new_config)


            profits = np.array([state.profits for state in states])

            mean = np.mean(profits)
            nash = np.mean(market.get_nash_profits())
            mono = np.mean(market.get_monopoly_profits())

            collusion_quotient = lib.get_collusion_quotient(mean, nash, mono)
            print(f"collusion_quotient = {collusion_quotient}")

            sum_collusion_quotients += collusion_quotient
            end = time.time()
            print(f"Time: {end-start}s")
        average_collusion_quotient.append(sum_collusion_quotients/times)


    import matplotlib.pyplot as plt


    plt.plot(discount_factors, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Discount factor')

    plt.savefig('discount_factor.png')
