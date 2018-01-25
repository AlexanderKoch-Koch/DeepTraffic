from Agent import Agent
import random
import numpy as np
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Queue

pool = ThreadPool(processes=1)

# evolution parameters
generations = 1
num_agents = 1

# start parameters for first gen agents
params = [1,        # lanesSide
          7,        # patchesAhead
          0,        # patchesBehind
          5000,     # trainIterations
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
        agents[a][0] = int(max(1, random.gauss(mu=params[0], sigma=0.1))) # lanesSide
        agents[a][1] = int(max(1, random.gauss(mu=params[1], sigma=0.5)))  # patchesAhead
        agents[a][2] = int(max(0, random.gauss(mu=params[2], sigma=0.4)))  # patchesBehind
        agents[a][3] = int(max(1, random.gauss(mu=params[3], sigma=100)))    # trainIterations
        agents[a][4] = int(max(1, random.gauss(mu=params[4], sigma=1.5)))  # l1_num_neurons
        agents[a][5] = int(max(0, random.gauss(mu=params[5], sigma=1)))  # l2_num_neurons
        agents[a][6] = int(max(0, random.gauss(mu=params[6], sigma=0.5)))  # l3_num_neurons
        agents[a][7] = random.gauss(mu=params[7], sigma=0.0001)  # learning_rate
        agents[a][8] = random.gauss(mu=params[8], sigma=0)  # momentum
        agents[a][9] = int(random.gauss(mu=params[9], sigma=2))  # batch_size
        agents[a][10] = random.gauss(mu=params[10], sigma=0.001)  # l2_decay
        agents[a][11] = random.gauss(mu=params[11], sigma=0.01)  # gamma
        agents[a][12] = int(max(1, random.gauss(mu=params[12], sigma=0.5)))  # temporal window

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
    #print(agents[-10:, :])
    print(params)

