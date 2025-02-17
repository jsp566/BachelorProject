import numpy as np
import utils.config as config
import Classes.SIMULATOR as SIMULATOR
import time
import os

# simulate
start = time.time()
market, states = SIMULATOR.simulate(config.defaultconfig)
end = time.time()
print(f"Time: {end-start}s")

# plot
import matplotlib.pyplot as plt

states = states[-100:]
mono = market.get_monopoly_prices()
nash = market.get_nash_prices()

period = range(len(states))

price1 = [state.prices[0] for state in states]
mono1 = [mono[0] for state in states]
nash1 = [nash[0] for state in states]

price2 = [state.prices[1] for state in states]
mono2 = [mono[1] for state in states]
nash2 = [nash[1] for state in states]


plt.plot(period, price1, label='Price 1')
#plt.plot(period, mono1, label='Mono 1', linestyle='dashed')
#plt.plot(period, nash1, label='Nash 1', linestyle='dashed')


plt.plot(period, price2, label='Price 2')
#plt.plot(period, mono2, label='Mono 2', linestyle='dashed')
#plt.plot(period, nash2, label='Nash 2', linestyle='dashed')

plt.legend()

filename = os.path.basename(__file__)
plt.savefig(config.create_filepath(filename))

plt.show()


