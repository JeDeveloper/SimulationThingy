class Generation:
    def __init__(self, **kwargs):
        if 'previous' in kwargs:
            previous_generation = kwargs['previous']
            context = kwargs['context']
            self.gen_number = previous_generation.gen_number + 1
            gen_members = [e.copy_to_next_gen() for e in previous_generation.ending_population if e.age() < e.lifespan()]
            # sort by result of selection pressure function
            gen_members.sort(key=lambda e: kwargs['selection_pressure'](e, context))
            # trim those that didn't make the cut
            self.starting_population = gen_members[:min(context.carrying_cap(), len(gen_members) - 1)]
            self.ending_population = [e for e in self.starting_population]

        else:
            if 'gen_number' in kwargs:
                self.gen_number = kwargs['gen_number']
            else:
                self.gen_number = 0
            self.starting_population = kwargs['entities']
            if 'ending_population' in kwargs:
                self.ending_population = kwargs['ending_population']
            else:
                self.ending_population = [e for e in self.starting_population]

    def __dict__(self):
        return {
            'gen_number': self.gen_number,
            'starting_population': [e.__dict__() for e in self.starting_population],
            'ending_population': [e.__dict__() for e in self.ending_population]
        }
