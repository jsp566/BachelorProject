import numpy as np

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
maxit = 10000

# Number of products
n = 10

# Number of prices
num_p = 10

# Given memory of prices = 1