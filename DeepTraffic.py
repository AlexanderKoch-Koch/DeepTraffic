from Agent import Agent
import random
import numpy as np
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Queue

pool = ThreadPool(processes=1)

# evolution parameters
generations = 20
num_agents = 80
sigma_divisor = 5

# start parameters for first gen agents
params = [1,        # lanesSide
          7,        # patchesAhead
          0,        # patchesBehind
          10000,     # trainIterations
          10,       # l1_num_neurons
          0,        # l2_num_neurons
          0,        # l3_num_neurons
          0.001,    # learning_rate
          0.0,      # momentum
          64,       # batch_size
          0.01,     # l2_decay
          0.88,     # gamma
          1]        # temporal window

for i in range(generations):
    # for each generation
    print("generation: " + str(i))
    parameters = []
    scores = []
    queues = []
    processes = []
    agents = np.zeros((num_agents, len(params) + 1), dtype=np.float32)  # gamma, epsilon, learning_rate, neurons, score
    for a in range(num_agents):
        # for each agent a in generation i
        agents[a][0] = max(1, round(random.gauss(mu=params[0], sigma=params[0]/sigma_divisor))) # lanesSide
        agents[a][1] = max(1, round(random.gauss(mu=params[1], sigma=params[1]/sigma_divisor)))   # patchesAhead
        agents[a][2] = max(0, round(random.gauss(mu=params[2], sigma=params[2]/sigma_divisor)))   # patchesBehind
        agents[a][3] = max(1, round(random.gauss(mu=params[3], sigma=0)))   # trainIterations
        agents[a][4] = max(1, round(random.gauss(mu=params[4], sigma=params[4]/sigma_divisor)))     # l1_num_neurons
        agents[a][5] = max(0, round(random.gauss(mu=params[5], sigma=params[5]/sigma_divisor)))   # l2_num_neurons
        agents[a][6] = max(0, round(random.gauss(mu=params[6], sigma=params[6]/sigma_divisor)))   # l3_num_neurons
        agents[a][7] = random.gauss(mu=params[7], sigma=params[7]/sigma_divisor)             # learning_rate
        agents[a][8] = random.gauss(mu=params[8], sigma=params[8]/sigma_divisor)                  # momentum
        agents[a][9] = round(random.gauss(mu=params[9], sigma=params[9]/sigma_divisor))             # batch_size
        agents[a][10] = random.gauss(mu=params[10], sigma=params[10]/sigma_divisor)            # l2_decay
        agents[a][11] = random.gauss(mu=params[11], sigma=params[11]/sigma_divisor)             # gamma
        agents[a][12] = max(1, round(random.gauss(mu=params[12], sigma=params[12]/sigma_divisor))) # temporal window

        agent = Agent(agents[a][0:len(agents[a] - 1)])
        queues.append(Queue())
        processes.append(Process(target=agent.run, args=(queues[a],)))
        processes[a].start()

    #print("launched all threads")
    score_index = len(params)
    for a in range(num_agents):
        agents[a][score_index] = queues[a].get()

    # sort agents by score
    agents = agents[np.argsort(agents[:, score_index])]
    print(agents[:, score_index])
    # take mean of the 2 best agents parameters
    for parameter in range(0, len(params) - 1):
        params[parameter] = np.mean(agents[-2, parameter])

    # print values of ten best agents
    print(agents[-1:, :])
    print(agent.generate_code(agents[a][0:len(agents[a] - 1)]))

