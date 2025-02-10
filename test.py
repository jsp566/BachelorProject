import numpy as np
import PRODUCT
import FIRM
import DEMAND
import Qlearning
import MARKET


# Demand function
mu = 0.1
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
qualities = 1

# Marginal cost
marginal_costs = 1

# Learning rate
alpha = 0.1

# Exloration rate
beta = 0.5
def Exloration_Rate(t):
    return np.exp(-beta*t)

# Discount factor
gamma = 0.9

# Number of iterations
maxit = 100000

# Number of firms
numb_firms = 2

# Number of products per firm
numb_products = 1

# Price range
numb_prices = 20
include_NE_and_Mono=True
extra=0.1

# Given memory of prices = 1


# Start

market = MARKET.Market(DEMAND.DemandFunction(Share))

for i in range(numb_firms):
    firm = FIRM.Firm(Qlearning.Qlearning(gamma, alpha, Exloration_Rate))
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

print([state.prices for state in states])