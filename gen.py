import random

class Gen:
    def __init__(self):
        self.source_hidden_layer = random.choice([True, False])
        self.id_source_neuron = random.randint(0, 6)
        if self.source_hidden_layer:
            self.id_target_neuron = random.randint(0, 6)
        else:
            self.id_target_neuron = random.randint(0, 1)
        self.weight = random.uniform(-1, 1)