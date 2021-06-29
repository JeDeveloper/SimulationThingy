from experiment import Experiment
exp = Experiment(params_file_path="sim_setups/example_sim_params_file.json")
exp.execute()
exp.save_results()