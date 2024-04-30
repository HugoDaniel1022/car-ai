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
    
    # Partiendo de los datos de entrada (matriz 1x7), los multiplica por los pesos ocultos (matriz 7x7). Luego suma los bias ocultos correspondientes a los pesos anteriormente mencionados y aplica una funcion ReLU quedando una matrix de 1x7. Vuelve a repetir el ciclo, esta vez multiplicando por los pesos de salida (matriz de 2x7), suma los bias de salida correspondinetes a los pesos de salida y vuelve a aplicar ReLU, obteniendo asi una matriz de 1x2 que serian los valores de salida entre 0 y 1.
    def feed_forward(self, input_layer_values): 
        self.inputs = input_layer_values
        self.hidden_outputs = self.matrix_vector_multiplication(self.hidden_layer_weights, input_layer_values)
        self.hidden_outputs = [self.ReLU(x + bias) for x, bias in zip(self.hidden_outputs, self.hidden_layer_bias)]
        self.outputs = self.matrix_vector_multiplication(self.output_layer_weights, self.hidden_outputs)
        self.outputs = [self.ReLU(x + bias) for x, bias in zip(self.outputs, self.output_layer_bias)]
        
    # pasado un parametro, si este es menor que 0 devuelve 0, y si es mayor devuelve ese mismo parametro
    def ReLU(self, x):
        return max(0, x)
    
    # crea una matriz llena de 0's, con la cantidad de filas y columnas que le pasemos por parametro
    def zeroes_matrix(self, rows, cols):
        return [[0 for _ in range(cols)] for _ in range(rows)]
    
    # multiplicador de matrices
    def matrix_vector_multiplication(self, matrix, vector):
        return [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]
    
    # cambia de colores las conexiones de la red neuronal
    def set_neural_connection_stroke(self, weight):
        if weight > 0:
            return (0, 255, 0)
        elif weight < 0:
            return (255, 255, 0)
        else:
            return (0, 0, 0)
        
    #imprime el grafico de las conexciones de la red neuronal
    def print_network(self, screen):
        input_positions = [(600, 50), (600, 90), (600, 130), (600, 170), (600, 210), (600, 250), (600, 290)]
        hidden_positions = [(800, 50), (800, 90), (800, 130), (800, 170), (800, 210), (800, 250), (800, 290)]
        output_positions = [(1000, 150), (1000, 190)]

        for i in range(7):
            for j in range(7):
                weight = self.hidden_layer_weights[i][j]
                color = self.set_neural_connection_stroke(weight)
                pygame.draw.line(screen, color, input_positions[i], hidden_positions[j], 2)
            for k in range(2):
                weight = self.output_layer_weights[k][i]
                color = self.set_neural_connection_stroke(weight)
                pygame.draw.line(screen, color, hidden_positions[i], output_positions[k], 2)
            pygame.draw.circle(screen, (255, 255, 255), input_positions[i], 20)
            color = (255, 255, 255) if self.hidden_outputs[i] == 0 else (170, 170, 170)
            pygame.draw.circle(screen, color, hidden_positions[i], 20)
            font = pygame.font.Font(None, 20)
            text1 = font.render(str(round(self.inputs[i], 2)), True, (0, 0, 0))
            screen.blit(text1, (input_positions[i][0] - 10, input_positions[i][1] - 10))
            text2 = font.render(str(round(self.hidden_outputs[i], 2)), True, (0, 0, 0))
            screen.blit(text2, (hidden_positions[i][0] - 10, hidden_positions[i][1] - 10))

        for i in range(2):
            color = (255, 255, 255) if self.outputs[i] == 0 else (170, 170, 170)
            pygame.draw.circle(screen, color, output_positions[i], 20)
            font = pygame.font.Font(None, 20)
            text = font.render(str(round(self.outputs[i], 2)), True, (0, 0, 0))
            screen.blit(text, (output_positions[i][0] - 10, output_positions[i][1] - 10))
