import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import time
import matplotlib.pyplot as plt
from os.path import basename
import cProfile
import pstats
import pickle
import os

filename = basename(__file__).replace('.py', '')

def main():
    # Start
    alphas = np.linspace(0.0, 0.25, 10, endpoint=False) #SET Alpha values
    betas = np.linspace(0.0, 2*10**-5, 10, endpoint=False) #SET Beta values
    sessions = 100
    iterations = 10**7
    numb_firms = 2
    parallel=True
    savedData = True

    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)
    
    variations = {
        "learning_rate": alphas,
        "exploration_rate_params": [(beta,) for beta in betas]
    }

    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData, variations=variations)

    average_collusion_quotient = [] #List to store average collusion quotients
    for alpha in alphas:
        for beta in betas:
            this_collusion_quotient = []
            for i in range(sessions):
                with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, f"(('exploration_rate_params', ({beta},)), ('learning_rate', {alpha}))_" + str(i) + ".pkl"), 'rb') as f:
                    result = pickle.load(f)
                
                collusion_quotients = [state.collussion_quotient for state in result[-100000:]]
                collusion_quotients = np.array(collusion_quotients)
                this_collusion_quotient.append(np.mean(collusion_quotients))
            
            average_collusion_quotient.append(np.mean(this_collusion_quotient))


    #Plotting heatmap of collusion quotients for different beta and alpha values
    average_collusion_quotient = np.array(average_collusion_quotient).reshape(len(alphas), len(betas))
    plt.imshow(average_collusion_quotient, cmap='hot_r', origin='lower', interpolation='nearest')
    plt.colorbar()
    plt.xticks(ticks=np.arange(len(betas)), labels=[f"{beta:.1e}" for beta in betas], rotation=45)
    plt.yticks(ticks=np.arange(len(alphas)), labels=[f"{alpha:.2f}" for alpha in alphas])
    plt.ylabel(r'$\alpha$')
    plt.xlabel(r'$\beta$x$10^5$')
    plt.savefig(config.create_filepath(filename))


if __name__ == "__main__":
    config.profile_main(main,filename)
