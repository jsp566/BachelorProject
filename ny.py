import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import os
import pickle
import itertools
import Classes.Strategies.Qlearning_one_price
import utils.graph_maker as graph_maker


sessions = 1
iterations = 10
numb_firms = 2
numb_products = (2, 1)
strategy = Classes.Strategies.Qlearning_one_price.Qlearning
parallel=True
savedData = True



new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms, numb_products=numb_products, strategy=strategy)
market= SIMULATOR.setup(new_config)

priceranges = lib.Make_Price_Ranges(market.Nash, market.Mono, 15, include_NE_and_Mono=False, extra=0.1)

priceranges = priceranges[0] 
print(priceranges)

average_p = priceranges[9]


def calculate_profit(average_p, priceranges):
    profits = []
    for price in priceranges:
        profit = market.calculate_profit(average_p, price)
        profits.append(profit)
    return profits
profits = calculate_profit(average_p, priceranges)
# Plotting the profits
print(profits)