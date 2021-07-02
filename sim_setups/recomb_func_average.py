import numpy as np


def recombine(context, *args):
    """
    produces a set of offspring where all entities are identical twins
    :param offspring_count:
    :param args:
    :return:
    """
    all_genomes = np.stack([e.genome for e in args])
    return np.average(all_genomes, axis=0)
