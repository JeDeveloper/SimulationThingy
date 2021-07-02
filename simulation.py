import logging
import time
from os import sep
import importlib
import numpy as np
from entity import Entity
from generation import Generation

from util import *

SETUPROOT = "sim_setups"

class Simulation:
    def __init__(self, rep_number, params, **kwargs):
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
        mate_choice = params['mate_choice_func']
        self.choose_mates = importlib.import_module(SETUPROOT + "." + mate_choice).choose_mates

        if 'rand_seed' in kwargs:
            pass
        else:
            self.randseed = time.time()
            self.rand = np.random.default_rng(int(self.randseed))
        if 'generations' in kwargs:
            self.generations = [Generation(gen_number=g['gen_number'],
                                           entities=[Entity(name=e['name'],
                                                            genome=np.fromarray(e['genome']),
                                                            age=e['age'],
                                                            num_mates=self.entity_num_mates(),
                                                            offspring_count=self.entity_offspring_count(),
                                                            lifespan=self.entity_lifespan())
                                                     for e in g['starting_population']],
                                           ending_population=[Entity(name=e['name'],
                                                                     genome=np.fromarray(e['genome']),
                                                                     age=e['age'],
                                                                     num_mates=self.entity_num_mates(),
                                                                     offspring_count=self.entity_offspring_count(),
                                                                     lifespan=self.entity_lifespan())
                                                              for e in g['ending_population']])
                                for g in kwargs['generations']]
        else:
            self.generations = []
        self.entity_name_log = []
        for g in self.generations:
            self.entity_name_log += [e.name() for e in g.starting_population if e not in self.entity_name_log]

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

    def current_generation(self):
        return self.generations[len(self.generations) - 1]

    # run functions
    def run(self):
        if len(self.generations) > 0:
            logging.info("Simulation already run! Aborting...")
            return
        logging.info("Running simulation")
        self.populate()
        logging.info(f"Executing simulation for {self.num_generations()} generations.")
        for g in range(self.num_generations()):
            self.generation()
        logging.info(f"Simulation complete.")

    def new_entity_name(self):
        while True:
            n = "".join([chr(ord("a") + self.rand.integers(0, 26)) for _ in range(self.entity_name_length())])
            if n not in self.entity_name_log:
                break
        self.entity_name_log.append(n)
        return n

    def populate(self):
        logging.info(f"Populating environment with {self.carrying_cap()} randomly generated entities.")
        starting_population = []
        for i in range(self.carrying_cap()):
            e = self.gen_entity()
            starting_population.append(e)
        self.generations.append(Generation(entities=starting_population))

    def gen_entity(self):
        genome = self.rand.random(size=self.genome_shape()) * self.genome_size()
        e = Entity(self.new_entity_name(), genome,
                   num_mates=self.entity_num_mates(), offspring_count=self.entity_offspring_count(),
                   lifespan=self.entity_lifespan())
        return e

    def generation(self):
        logging.info(f"Running generation {len(self.generations)}.")
        starttime = time.time()
        curr_gen = Generation(previous=self.current_generation(),
                              selection_pressure=self.selection_pressure,
                              context=self)
        self.generations.append(curr_gen)
        for e in curr_gen.starting_population:
            logging.info(f"Choosing mates for {e.name()}.")
            e_mates = self.choose_mates(e, sans(curr_gen.starting_population, e))
            logging.info(f"Mates chosen: {', '.join([x.name() for x in e_mates])}.")
            if len(e_mates) > 0:
                offspring = [Entity(
                    name=self.new_entity_name(),
                    genome=self.recombination(self, e, *e_mates),
                    num_mates=self.entity_num_mates(),
                    offspring_count=self.entity_offspring_count(),
                    lifespan=self.entity_lifespan()
                ) for _ in range(e.offspring_count())]
                logging.info(f"{e.name()} produced offspring {', '.join([ofs.name() for ofs in offspring])}")
                curr_gen.ending_population.extend(offspring)
        logging.info(f"Generation {len(self.generations)} completed in {time.time() - starttime} seconds.")


    def __dict__(self):
        d = {}
        d['replication'] = self.rep_number()
        d['rand_seed'] = self.randseed
        d['generations'] = [g.__dict__() for g in self.generations]
        return d

    def poplatiome(self):
        return {e.name(): e.genome for e in self.current_generation().starting_population}