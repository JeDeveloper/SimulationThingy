class Entity:
    def __init__(self, name, genome, age=0, **kwargs):
        self.__name = name
        self.genome = genome
        self.__num_mates = kwargs['num_mates']
        self.__offspring_count = kwargs['offspring_count']
        self.__lifespan = kwargs['lifespan']
        self.__age = age

    # accessors
    def name(self):
        return self.name()

    def num_mates(self):
        return self.__num_mates

    def offspring_count(self):
        return self.__offspring_count

    def lifespan(self):
        return self.__lifespan

    def choose_mates(self, prospectives_list):
        pass

    def age(self):
        return self.__age

    def copy_to_next_gen(self):
        return Entity(self.genome, self.name(), self.age() + 1,
                      num_mates=self.num_mates(),
                      offspring_count=self.offspring_count(),
                      lifespan=self.lifespan())

