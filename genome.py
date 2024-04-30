import random
from gen import Gen

class Genome:
    def __init__(self):
        self.length = 16
        self.genes = [Gen() for _ in range(self.length)]
        self.hidden_layer_bias = self.random_vector(7)
        self.output_layer_bias = self.random_vector(2)

    # genera vectores aleatorios entre 1 y -1
    def random_vector(self, size):
        return [random.uniform(-1, 1) for _ in range(size)]
    
    # copia una lista de genes
    def copy(self):
        copy = Genome()
        copy.genes = self.genes[:]
        copy.hidden_layer_bias = self.hidden_layer_bias[:]
        copy.output_layer_bias = self.output_layer_bias[:]
        return copy

    # mediante una lista copiada de genes realizar mutaciones aleatorias entre 1 y 4. Lo que haces es cambiar 
    #de posicion los genes ya existentes entre 1 y 4 veces.
    def mutate(self):
        mutated_genome = self.copy()
        amount_of_mutations = random.randint(1, 4)
        for _ in range(amount_of_mutations):
            index = random.randint(0, self.length - 1)
            mutated_genome.genes[index] = Gen()
        return mutated_genome

    # intercambia elementos de una lista(genes) con los de otra lista(genes) que se la pasa por parametro y 
    #devuelve la lista intercambiaba o modificada.
    def crossover(self, another_genome):
        crossed_genome = self.copy()
        amount_of_crossovers = random.randint(1, 4)
        for _ in range(amount_of_crossovers):
            index = random.randint(0, self.length - 1)
            crossed_genome.genes[index] = another_genome.genes[index]
        return crossed_genome
