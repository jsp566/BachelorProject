import numpy as np
import utils.lib as lib
import Classes.SIMULATOR as SIMULATOR
import utils.config as config
import matplotlib.pyplot as plt
from os.path import basename
import pickle
import os


filename =  basename(__file__).replace('.py', '')


def new_session(i, market, iterations, start_period = 1, convergence = None, foldername = None, variation = None):
    before = market.simulate(iterations, start_period=start_period, convergence=convergence)
    market.merge(0,1)
    after = market.simulate(iterations, start_period=start_period, convergence=convergence)
    if foldername:
        filename = str(i) + ".pkl"
        if variation:

            filename = str(variation) + "_" + filename
            
        with open(os.path.join(os.getcwd(), 'Output', 'Data', foldername, filename), 'wb') as f:
            pickle.dump(before + after, f)
    return


def main():
    # Start
    sessions = 100
    iterations = 10**7
    numb_firms = 3
    parallel=True
    savedData = True
    


    new_config = config.create_config(sessions=sessions, iterations=iterations, numb_firms=numb_firms)
    market= SIMULATOR.setup(new_config)
    SIMULATOR.simulate_sessions(new_config, filename=filename, parallel=parallel, savedData=savedData, session=new_session)
    # Collusion Quotient:

    print("Reading data")
    lengths = []
    collusion_quotients = []
    mergerperiods = []
    for i in range(sessions):
        print(i)
        with open(os.path.join(os.getcwd(), 'Output', 'Data', filename, str(i) + ".pkl"), 'rb') as f:
            result = pickle.load(f)
        lengths.append(len(result))
        mergerperiod = next(i for i, state in enumerate(result) if len(state.firm_profits) < numb_firms)
        mergerperiods.append(mergerperiod)
        collusion_quotients.append(np.mean([state.collussion_quotient  for state in result], axis=1))
    

    plt.hist(lengths, bins=100)
    plt.xlabel('Length of session')
    plt.ylabel('Frequency')
    plt.title('Length of session')
    plt.savefig(config.create_filepath(filename + "_totallengths"))

    plt.clf()
    
    
    
    min_length = min(lengths)
    max_length = max(lengths)



    print("Extending data")
    for i in range(sessions):
        cq = np.array(collusion_quotients[i])
        if len(cq) < max_length:
            collusion_quotients[i] = np.append(cq, [np.mean(cq[-100:])]*(max_length - len(cq)))

    

    collusion_quotients = np.array(collusion_quotients)

    average_collusion_quotient = np.mean(collusion_quotients, axis=0)

    plt.plot(range(min_length), average_collusion_quotient[:min_length])
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient"))

    plt.clf()


    period = range(len(average_collusion_quotient))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient_full"))

    plt.clf()

    # Moving average
    ma100=  lib.moving_average(average_collusion_quotient, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100"))
    plt.clf()

    print("Getting mergers periods data")

    plt.hist(mergerperiods, bins=100)
    plt.xlabel('Periods until merger')
    plt.ylabel('Frequency')
    plt.title('Periods until merger')
    plt.savefig(config.create_filepath(filename + "_periods_before_merger"))

    plt.clf()

    plt.hist([lengths[i] - mergerperiods[i] for i in range(len(mergerperiods))], bins=100)
    plt.xlabel('Periods after merger')
    plt.ylabel('Frequency')
    plt.title('Periods after merger')
    plt.savefig(config.create_filepath(filename + "_periods_after_merger"))

    plt.clf()

    print("Calculating lengths of collusion quotients")
    

    new_collusion_quotients = [None] * sessions
    for i in range(sessions):
        new_collusion_quotients[i] = collusion_quotients[i][mergerperiods[i]-10**5:]
        

        
    lengths = [len(c) for c in new_collusion_quotients]
    min_length = min(lengths)
    max_length = max(lengths)
    
    print("Extending data")
    for i in range(sessions):
        cq = np.array(new_collusion_quotients[i])
        if len(cq) < max_length:
            new_collusion_quotients[i] = np.append(cq, [np.mean(cq[-100:])]*(max_length - len(cq)))


    new_collusion_quotients = np.array(new_collusion_quotients)
    
    average_collusion_quotient = np.mean(new_collusion_quotients, axis=0)
    
    plt.plot(range(min_length), average_collusion_quotient[:min_length])
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient_merged"))

    plt.clf()

    period = range(len(average_collusion_quotient))
    plt.plot(period, average_collusion_quotient)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    plt.savefig(config.create_filepath(filename + "_collusion_quotient_merged_full"))

    plt.clf()

    # Moving average
    ma100=  lib.moving_average(average_collusion_quotient, 100)
    repetitions = np.linspace(0, len(ma100), len(ma100))

    plt.plot(repetitions, ma100)
    plt.ylabel('Collusion Quotient')
    plt.xlabel('Period')
    

    plt.savefig(config.create_filepath(filename + "_ma100_merged"))
    plt.clf()
        
        


if __name__ == "__main__":
    config.profile_main(main,filename)
