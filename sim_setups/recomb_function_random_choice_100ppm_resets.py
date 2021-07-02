import recomb_func_random_choice

def recombine(context, *args):
    rand_choice_rec_results = recomb_func_random_choice.recombine(context, *args)
    mutations = context.rand.random(size=context.genome_shape()) < 0.0001
    newvals = context.rand.random(size=context.genome_shape()) * context.genome_size()
    rand_choice_rec_results[mutations] = newvals[mutations]