import numpy as np


def apply(e, sim_env):
    """
    rates the fitness of an entity from 0 to 1, based on how similar it is to the average entity in the population
    :param e: the entity to rate
    :param sim_env: the simulation in which the entity exists
    :return: a rating from 0 to 1
    """

    population_average = np.average(np.stack(sim_env.poplatiome().values()), axis=0)
    diff = np.abs(population_average - e.genome)
    return 1 - (np.sum(diff) / diff.size)
