from Agent import Agent
import numpy as np
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Queue
from GeneticAlgorithm import mutate, create_mating_pool, crossover, round_float_random

pool = ThreadPool(processes=1)

# evolution parameters
generations = 100
num_agents = 96
sigma_divisor = 15
mutate_percent = 5

# start parameters for first gen agents
params_start = [1,        # lanesSide
                7,        # patchesAhead
                0,        # patchesBehind
                3000,     # experience size
                10,       # l1_num_neurons
                0,        # l2_num_neurons
                0,        # l3_num_neurons
                0.001,    # learning_rate
                0.0,      # momentum
                64,       # batch_size
                0.01,     # l2_decay
                0.88,     # gamma
                1]        # temporal window

int_params_indexes = [0, 1, 2, 3, 4, 5, 6, 9, 12]

params = np.zeros(shape=(num_agents, len(params_start)))
# mutate params_start to each agent params
params[:] = mutate(params_start, sigma_divisor, 95)

for generation in range(generations):
    # for each generation
    print("generation: " + str(generation))
    parameters = []
    scores = []
    queues = []
    processes = []
    agents = np.zeros((num_agents, len(params_start) + 1), dtype=np.float32)  # params, score
    for a in range(num_agents):
        # for each agent a in generation i
        params[a] = mutate(params[a], sigma_divisor, mutate_percent)
        for i in range(len(int_params_indexes)):
            params[a][int_params_indexes[i]] = round_float_random(params[a][int_params_indexes[i]])
        agents[a][0:-1] = params[a]
        agent = Agent(agents[a][0:len(agents[a] - 1)])
        queues.append(Queue())
        processes.append(Process(target=agent.run, args=(queues[a],)))
        processes[a].start()

    score_index = len(params_start)
    for a in range(num_agents):
        agents[a][score_index] = queues[a].get()

    # sort agents by score
    agents = agents[np.argsort(agents[:, score_index])]
    # print scores
    print(agents[:, score_index])
    print(agents[-1:, :])
    print(agent.generate_code(agents[a][0:len(agents[a] - 1)]))

    mating_params = create_mating_pool(agents, 16)
    params = crossover(mating_params, num_agents)



