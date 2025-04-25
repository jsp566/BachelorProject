import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import time
import matplotlib.pyplot as plt
from os.path import basename
import cProfile
import pstats

filename = basename(__file__).replace('.py', '')

def main():
    # Start
    alphas = np.linspace(0.0, 0.25, 1, endpoint=False) #SET Alpha values
    betas = np.linspace(0.0, 2*10**-5, 2, endpoint=False) #SET Beta values
    sessions = 1
    iterations = 1000000
    numb_firms = 2

    average_collusion_quotient = [] #List to store average collusion quotients
    for alpha in alphas:
        for beta in betas: 
            fun = lambda t: np.exp(-beta*t) #lambda function for exploration rate
            print(f"alpha = {alpha}, beta = {beta}")
            new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms, alpha=alpha, beta=beta)
            market, results = SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=False, savedData=False)
            min_length = min(len(result) for result in results)
            collusion_quotients = [[state.collussion_quotient for state in result[:10000]] for result in results]
            collusion_quotients = np.array(collusion_quotients)
            average_collusion_quotient.append(np.mean(collusion_quotients))


    #Plotting heatmap of collusion quotients for different beta and alpha values
    average_collusion_quotient = np.array(average_collusion_quotient).reshape(len(alphas), len(betas))
    plt.imshow(average_collusion_quotient, cmap='hot_r', origin='lower', interpolation='nearest')
    plt.colorbar()
    plt.ylabel(r'$\alpha$')
    plt.xlabel(r'$\beta$x$10^5$')
    plt.savefig(config.create_filepath(filename))


if __name__ == "__main__":
    config.profile_main(main,filename)
