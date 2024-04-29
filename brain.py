import random
import pygame

class Brain:
    def __init__(self, genome):
        self.inputs = []
        self.outputs = [1, 0]
        self.hidden_layer_weights = self.zeroes_matrix(7, 7)
        self.output_layer_weights = self.zeroes_matrix(2, 7)
        for gen in genome.genes:
            if gen.source_hidden_layer:
                self.hidden_layer_weights[gen.id_target_neuron][gen.id_source_neuron] = gen.weight
            else:
                self.output_layer_weights[gen.id_target_neuron][gen.id_source_neuron] = gen.weight
        self.hidden_layer_bias = genome.hidden_layer_bias
        self.output_layer_bias = genome.output_layer_bias
        self.hidden_outputs = []

    def feed_forward(self, input_layer_values): 
        self.inputs = input_layer_values
        self.hidden_outputs = self.matrix_vector_multiplication(self.hidden_layer_weights, input_layer_values)
        self.hidden_outputs = [self.ReLU(x + bias) for x, bias in zip(self.hidden_outputs, self.hidden_layer_bias)]
        self.outputs = self.matrix_vector_multiplication(self.output_layer_weights, self.hidden_outputs)
        self.outputs = [self.ReLU(x + bias) for x, bias in zip(self.outputs, self.output_layer_bias)]
        
    def ReLU(self, x):
        return max(0, x)

    def zeroes_matrix(self, rows, cols):
        return [[0 for _ in range(cols)] for _ in range(rows)]

    def matrix_vector_multiplication(self, matrix, vector):
        return [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]
    
    def uniform_init(self, rows, cols, lower_bound, upper_bound):
        return [[random.uniform(lower_bound, upper_bound) for _ in range(cols)] for _ in range(rows)]
    
    def set_neural_connection_stroke(self, weight):
        if weight > 0:
            return (0, 255, 0)
        elif weight < 0:
            return (255, 255, 0)
        else:
            return (255, 0, 0)

    def print_network(self, screen):
        input_positions = [(600, 50), (600, 90), (600, 130), (600, 170), (600, 210), (600, 250), (600, 290)]
        hidden_positions = [(800, 50), (800, 90), (800, 130), (800, 170), (800, 210), (800, 250), (800, 290)]
        output_positions = [(1000, 150), (1000, 190)]

        for i in range(7):
            # Input layer to hidden layer lines
            for j in range(7):
                weight = self.hidden_layer_weights[i][j]
                color = self.set_neural_connection_stroke(weight)
                pygame.draw.line(screen, color, input_positions[i], hidden_positions[j], 2)
            # Hidden layer to output layer lines
            for k in range(2):
                weight = self.output_layer_weights[k][i]
                color = self.set_neural_connection_stroke(weight)
                pygame.draw.line(screen, color, hidden_positions[i], output_positions[k], 2)
            # Input layer circles
            pygame.draw.circle(screen, (255, 255, 255), input_positions[i], 20)
            # Hidden layer circles
            color = (255, 255, 255) if self.hidden_outputs[i] == 0 else (170, 170, 170)
            pygame.draw.circle(screen, color, hidden_positions[i], 20)
            # Input texts
            font = pygame.font.Font(None, 20)
            text1 = font.render(str(round(self.inputs[i], 2)), True, (0, 0, 0))
            screen.blit(text1, (input_positions[i][0] - 10, input_positions[i][1] - 10))
            text2 = font.render(str(round(self.hidden_outputs[i], 2)), True, (0, 0, 0))
            screen.blit(text2, (hidden_positions[i][0] - 10, hidden_positions[i][1] - 10))

        # Output circles
        for i in range(2):
            color = (255, 255, 255) if self.outputs[i] == 0 else (170, 170, 170)
            pygame.draw.circle(screen, color, output_positions[i], 20)
            font = pygame.font.Font(None, 20)
            text = font.render(str(round(self.outputs[i], 2)), True, (0, 0, 0))
            screen.blit(text, (output_positions[i][0] - 10, output_positions[i][1] - 10))
