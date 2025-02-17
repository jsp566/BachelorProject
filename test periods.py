import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import time


# Start
times = 50

sum_collusion_quotients = 0
for i in range(times):
    print(f"i = {i}")
    start = time.time()
    market, states = SIMULATOR.simulate(config.defaultconfig)

    
    profits = np.array([state.profits for state in states])
    mean = np.mean(profits, axis=1)
    nash = np.mean(market.get_nash_profits())

    mono = np.mean(market.get_monopoly_profits())

    collusion_quotient = lib.get_collusion_quotient(mean, nash, mono)

    sum_collusion_quotients += collusion_quotient
    end = time.time()
    print(f"Time: {end-start}s")
    
average_collusion_quotient = sum_collusion_quotients/times

print(average_collusion_quotient)

import matplotlib.pyplot as plt

period = range(len(states))

plt.plot(period, average_collusion_quotient)
plt.ylabel('Collusion Quotient')
plt.xlabel('Period')

plt.show()