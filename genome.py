import random
from gen import Gen

class Genome:
    def __init__(self):
        self.length = 16
        self.genes = [Gen() for _ in range(self.length)]
        self.hidden_layer_bias = self._random_vector(7)
        self.output_layer_bias = self._random_vector(2)

    def _random_vector(self, size):
        return [random.uniform(-1, 1) for _ in range(size)]
    
    def copy(self):
        copy = Genome()
        copy.genes = self.genes[:]  # Copy the list
        copy.hidden_layer_bias = self.hidden_layer_bias[:]
        copy.output_layer_bias = self.output_layer_bias[:]
        return copy

    def mutate(self):
        mutated_genome = self.copy()
        amount_of_mutations = random.randint(1, 4)
        for _ in range(amount_of_mutations):
            index = random.randint(0, self.length - 1)
            mutated_genome.genes[index] = Gen()
        return mutated_genome

    def crossover(self, another_genome):
        crossed_genome = self.copy()
        amount_of_crossovers = random.randint(1, 4)
        for _ in range(amount_of_crossovers):
            index = random.randint(0, self.length - 1)
            crossed_genome.genes[index] = another_genome.genes[index]
        return crossed_genome
