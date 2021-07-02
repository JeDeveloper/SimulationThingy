import sys
import json
from simulation import Simulation
import logging
from datetime import datetime
from os import sep

class Experiment:
    def __init__(self, **kwargs):
        root = logging.getLogger()
        logging.basicConfig(filename=f"program_logs{sep}{self.param_set_name}_{str(datetime.now())}.log",
                            level=logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

        if 'params_file_path' in kwargs:
            with open(kwargs['params_file_path']) as f:
                self.params = json.load(f)
                self.param_set_name = self.params['name']
                self.reps = self.params['replications']
                self.sims = [Simulation(rep, self.params) for rep in range(self.reps)]
                self.exp_start_time = None
                self.exp_end_time = None
        else:
            assert 'experiment_file_path' in kwargs
            with open(kwargs['experiment_file_path']) as expfile:
                params = json.load(expfile)
                self.param_set_name = params['name']
                param_keys = [
                    'genome_shape', 'generations', 'carrying_capactiy', 'entity_name_length',
                    'mating_recombination_func', 'selection_pressure', 'mate_choice_func',
                    'consent', 'semirandom_survival', 'entity_num_mates', 'entity_offspring_count',
                    'entity_lifespan']
                self.params = {key: params[key] for key in param_keys}
                self.sims = [Simulation(sim['replication'], params, **sim) for sim in params['replications']]
                self.reps = len(self.sims)

                self.exp_start_time = datetime(**params['start_time'])
                self.exp_end_time = datetime(**params['end_time'])


    def execute(self):
        self.exp_start_time = datetime.now()
        logging.info(f"Started experiment from param set {self.param_set_name} at {str(self.exp_start_time)}.")
        for sim in self.sims:
            logging.info(f"Running simulation {sim.rep_number()}.")
            sim.run()
            logging.info(f"Simulation {sim.rep_number()} run complete.")
        self.exp_end_time = datetime.now()
        logging.info(f"Experiment concluded.")

    def save_results(self):
        export_dict = {}
        export_dict['start_time'] = {'year': self.exp_start_time.year, 'month': self.exp_start_time.month,
                                     'day': self.exp_start_time.day, 'hour': self.exp_start_time.hour,
                                     'minute': self.exp_start_time.minute, 'second': self.exp_start_time.second}
        export_dict['end_time'] = {'year': self.exp_end_time.year, 'month': self.exp_end_time.month,
                                     'day': self.exp_end_time.day, 'hour': self.exp_end_time.hour,
                                     'minute': self.exp_end_time.minute, 'second': self.exp_end_time.second}
        export_dict.update(self.params)
        replications_dict = []
        for sim in self.sims:
            replications_dict.append(sim.__dict__())
        export_dict['replications'] = replications_dict

        filename = f"sim_logs{sep}{self.param_set_name}_{str(self.exp_start_time)}.json"
        with open(filename, 'w') as f:
            json.dump(export_dict, f, indent="\t")
