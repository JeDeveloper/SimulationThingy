import numpy as np


def choose_mates(e, options):
    """

    :param e:
    :param options:
    :return:
    """
    options.sort(key=lambda x: np.sum(np.abs(np.array([ord(c) for c in x.name()]) -
                                             np.array([ord(c) for c in e.name()]))))
    return options[:min(e.num_mates(), len(options))]
