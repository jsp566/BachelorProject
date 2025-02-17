import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import time
import matplotlib.pyplot as plt
from os.path import basename


def main():
    # Start
    alphas = np.linspace(0.0, 0.25, 10, endpoint=False) #SET Alpha values
    betas = np.linspace(0.0, 2*10**-5, 10, endpoint=False) #SET Beta values
    times = 25 #Repetitions

    average_collusion_quotient = [] #List to store average collusion quotients
    sim_start = time.time()

    for alpha in alphas:
        for beta in betas: 
            fun = lambda t: np.exp(-beta*t) #lambda function for exploration rate
            print(f"alpha = {alpha}, beta = {beta}")
            start = time.time()
            new_config = config.create_config(exploration_rate=fun, alpha=alpha, beta=beta)
            sum_collusion_quotients = 0
            for i in range(times):
            
                start = time.time()

                market, states = SIMULATOR.simulate(new_config)


                profits = np.array([state.profits for state in states[-1000:]])

                mean = np.mean(profits)
                nash = np.mean(market.get_nash_profits())
                mono = np.mean(market.get_monopoly_profits())

                collusion_quotient = lib.get_collusion_quotient(mean, nash, mono)
                sum_collusion_quotients += collusion_quotient

            end = time.time()
            print(f"Average collusion quotient: {sum_collusion_quotients/times}")
            print(f"Time: {end-start}s")
            average_collusion_quotient.append(sum_collusion_quotients/times)


    #Plotting heatmap of collusion quotients for different beta and alpha values
    average_collusion_quotient = np.array(average_collusion_quotient).reshape(len(alphas), len(betas))
    plt.imshow(average_collusion_quotient, cmap='hot_r', interpolation='nearest')
    #plt.xticks(ticks = [5*10**(-6),1*10**(-5),1.5*10**(-5)], labels=[0.5,1,1.5])
    #plt.yticks(ticks = [0.05,0.1,0.15,0.2], labels=[0.05,0.1,0.15,0.2])
    plt.colorbar()
    plt.ylabel(r'$\alpha$')
    plt.xlabel(r'$\beta$x$10^5$')
    filename = basename(__file__)
    plt.savefig(config.create_filepath(filename))
    plt.show()


if __name__ == "__main__":
    main()