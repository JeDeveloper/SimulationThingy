from random import uniform


def choose_mates(e, options):
    """

    :param e:
    :param options:
    :return:
    """
    options.sort(key=lambda x: uniform(0, 1))
    return options[:min(e.num_mates(), len(options))]