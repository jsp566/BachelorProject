import numpy as np
import PRODUCT
import FIRM
import DEMAND
import Qlearning
import ZeroMemQlearning
import MARKET

#Create a testing environment for the different classes in the program
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
quality = 2

# Marginal cost
marginal_cost = 1

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
maxit = 10000

# Number of firms
numb_firms = 2

# Number of products per firm
numb_products = 1

# Price range
numb_prices = 15
include_NE_and_Mono=False
extra=0.1

# Given memory of prices = 1


# Start

market = MARKET.Market(DEMAND.DemandFunction(Share))

for i in range(numb_firms):
    firm = FIRM.Firm(Qlearning.Qlearning(gamma, alpha, Calvani_Exploration_Rate))
    market.add_firm(firm)
    for j in range(numb_products):
        product = PRODUCT.Product(marginal_cost, quality)
        firm.add_product(product)

market.set_priceranges(numb_prices, include_NE_and_Mono, extra)

for firm in market.firms:
    for product in firm.products:
        print(product.pricerange)

print(market.get_no_of_firms())
print(market.get_firms())
states = market.simulate(maxit)