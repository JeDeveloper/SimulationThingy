import time
from os import sep
import importlib
import numpy as np
from entity import Entity

from util import *

SETUPROOT = "sim_setups"

class Simulation:
    def __init__(self, rep_number, params):
        self.__rep_number = rep_number

        self.__name = params['name']
        self.__genome_shape = params['genome_shape']
        self.__entity_name_length = params['entity_name_length']
        self.__num_generations = params['generations']
        self.__carrying_cap = params['carrying_capactiy']
        self.__consent_required = params['consent'] # not implemented yet

        self.__entity_num_mates = params['entity_num_mates']
        self.__entity_offspring_count = params['entity_offspring_count']
        self.__entity_lifespan = params['entity_lifespan']

        mating_recombination_function_file = params['mating_recombination_func']
        self.recombination = importlib.import_module(SETUPROOT + "." + mating_recombination_function_file).recombine
        selection_pressure_function_file = params['selection_pressure']
        self.selection_pressure = importlib.import_module(SETUPROOT + "." + selection_pressure_function_file).apply

        self.rand = None
        self.generations = []
        self.entity_name_log = []
    # accessors
    def rep_number(self):
        return self.__rep_number

    def name(self):
        return self.__name + f"_R{self.rep_number()}"

    def genome_shape(self):
        return self.__genome_shape

    def genome_size(self):
        return np.product(self.__genome_shape)

    def num_generations(self):
        return self.__num_generations

    def entity_name_length(self):
        return self.__entity_name_length

    def carrying_cap(self):
        return self.__carrying_cap

    def is_consent_required(self):
        return self.__consent_required

    def entity_num_mates(self):
        return self.__entity_num_mates

    def entity_offspring_count(self):
        return self.__entity_offspring_count

    def entity_lifespan(self):
        return self.__entity_lifespan

    # run functions
    def new_entity_name(self):
        n = None
        while True:
            n = "".join([chr(ord("a") + self.rand.integers(0, 26)) for _ in range(self.entity_name_length())])
            if n not in self.entity_name_log:
                break
        self.entity_name_log.append(n)
        return n

    def populate(self):
        self.rand = np.random.default_rng(time.gmtime())
        starting_population = []
        for i in range(self.sim.carring_cap()):
            e = self.gen_entity()
            starting_population.append(e)
        self.generations.append(starting_population)

    def gen_entity(self):
        genome = self.rand.random(size=self.genome_shape()) * self.genome_size()
        e = Entity(genome, self.new_entity_name(),
                   num_mates=self.entity_num_mates(), offspring_count=self.entity_offspring_count(),
                   lifespan=self.entity_lifespan())
        return e

    def generation(self):
        curr_gen = [e for e in self.generations[len(self.generations)]]
        # sort by result of selection pressure function
        curr_gen.sort(key=lambda e: self.selection_pressure(e, self))
        # trim those that didn't make the cut
        curr_gen = curr_gen[:self.carrying_cap()]
        # make next gen list
        next_gen = [e.copy_to_next_gen() for e in curr_gen if e.age() < e.lifespan()]
        for e in curr_gen:
            e_mates = e.choose_mates(sans(curr_gen, e))
            for _ in range(len(e.offspring_count())):
                next_gen.append(Entity(
                    genome=self.recombination(e, *e_mates,
                                              offspring_count=int(e.offspring_count() / self.entity_num_mates())),
                    num_mates=self.entity_num_mates(),
                    offspring_count=self.entity_offspring_count(),
                    lifespan=self.entity_lifespan()
                ))

        self.generations.append(next_gen)

    def __dict__(self):
        d = {}
        d['replication'] = self.rep_number()
        d['rand'] = self.rand
        d['generations'] = [[e.__dict__() for e in g] for g in self.generations]
        return d