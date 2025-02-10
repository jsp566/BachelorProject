import numpy as np
import PRODUCT
import FIRM
import DEMAND
import Qlearning
import ZeroMemQlearning
import MARKET


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

market = MARKET.Market(DEMAND.DemandFunction(Share))

for i in range(numb_firms):
    firm = FIRM.Firm(ZeroMemQlearning.ZeroMemQlearning(gamma, alpha, Calvani_Exploration_Rate))
    market.add_firm(firm)
    for j in range(numb_products):
        product = PRODUCT.Product(qualities, marginal_costs)
        firm.add_product(product)


market.set_priceranges(numb_prices, include_NE_and_Mono, extra)

state_space = market.set_state_space()

for firm in market.firms:
    action_space = firm.set_action_space()
    firm.strategy.initialize(market.state_space, firm.action_space)


for firm in market.firms:
    for product in firm.products:
        print(product.pricerange)



print(market.get_nash_prices())
print(market.get_monopoly_prices())

states = market.simulate(maxit)


# plot
import matplotlib.pyplot as plt

states = states[-100:]
mono = market.get_monopoly_prices()
nash = market.get_nash_prices()

period = [state.t for state in states]

price1 = [state.prices[0] for state in states]
mono1 = [mono[0] for state in states]
nash1 = [nash[0] for state in states]

price2 = [state.prices[1] for state in states]
mono2 = [mono[1] for state in states]
nash2 = [nash[1] for state in states]


plt.plot(period, price1, label='Price 1')
#plt.plot(period, mono1, label='Mono 1')
plt.plot(period, nash1, label='Nash 1')


plt.plot(period, price2, label='Price 2')
#plt.plot(period, mono2, label='Mono 2')
plt.plot(period, nash2, label='Nash 2')

plt.legend()
plt.show()

