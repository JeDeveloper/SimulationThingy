import numpy as np


def recombine(context, *args):
    """
    produces a set of offspring where all entities are identical twins
    :param offspring_count:
    :param args:
    :return:
    """
    all_genomes = np.stack([e.genome for e in args])
    context.rand.choice(all_genomes, shape=context.genome_shape(), axis=0) # TODO: is this actually what this function does
    return np.average(all_genomes, axis=0)
