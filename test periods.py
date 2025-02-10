import numpy as np
import lib
import PRODUCT
import FIRM
import DEMAND
import Qlearning
import ZeroMemQlearning
import MARKET
import time


# Demand function
mu = 0.25
def Share(P, A):
    '''
    P: Price matrix
    A: Observable attributes matrix
    '''
    numer = np.exp((A-P)/mu)
    denom = 1 + np.sum(numer)
    result = numer/denom
    return result


# Observable attributes
qualities = 2

# Marginal cost
marginal_costs = 1

# Learning rate
alpha = 0.125

# Exloration rate
beta = 0.00001
def Calvani_Exploration_Rate(t):
    return np.exp(-beta*t)

def Mathias_Exploration_Rate(t):
    return (0.015**(2/maxit))**t

# Discount factor
gamma = 0.95

# Number of iterations
maxit = 1000000

# Number of firms
numb_firms = 2

# Number of products per firm
numb_products = 1

# Price range
numb_prices = 15
include_NE_and_Mono=True
extra=0.1

# Given memory of prices = 1


# Start

times = 50

sum_collusion_quotients = 0
for i in range(times):
    print(i)
    start = time.time()
    market = MARKET.Market(DEMAND.DemandFunction(Share))

    for i in range(numb_firms):
        firm = FIRM.Firm(Qlearning.Qlearning(gamma, alpha, Calvani_Exploration_Rate))
        market.add_firm(firm)
        for j in range(numb_products):
            product = PRODUCT.Product(qualities, marginal_costs)
            firm.add_product(product)


    market.set_priceranges(numb_prices, include_NE_and_Mono, extra)

    state_space = market.set_state_space()

    for firm in market.firms:
        action_space = firm.set_action_space()
        firm.strategy.initialize(market.state_space, firm.action_space)

    states = market.simulate(maxit)

    
    profits = np.array([state.profits for state in states])
    mean = np.mean(profits, axis=1)
    nash = np.mean(market.get_nash_profits())

    mono = np.mean(market.get_monopoly_profits())

    collusion_quotient = lib.get_collusion_quotient(mean, nash, mono)

    sum_collusion_quotients += collusion_quotient
    end = time.time()
    print(end-start)
    
average_collusion_quotient = sum_collusion_quotients/times

print(average_collusion_quotient)

import matplotlib.pyplot as plt

period = [state.t for state in states]

plt.plot(period, average_collusion_quotient)
plt.ylabel('Collusion Quotient')
plt.xlabel('Period')

plt.show()