import pygame
import os
import random
import time
import matplotlib.pyplot as plt  # Para tomar las mediciones
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# ------------------------ Juego -------------------------------------------


# Global Constants
millis = lambda: int(round(time.time() * 1000))

DINOS_PER_GENERATION = 10
MIN_SPAWN_MILLIS = 1500
MAX_SPAWN_MILLIS = 2500

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# RUNNING = pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png"))
DUCKING = pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png"))
# JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

DINO = pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png"))

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = pygame.image.load(os.path.join("Assets/Bird", "Bird1.png"))

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

# -------------------------------- Fin Juego --------------------------------------------------------

# -------------------------------- Algoritmo Genetico -----------------------------------------------

class Gen:
    def __init__(self):
        self.source_hidden_layer = random.choice([True, False])
        self.id_source_neuron = random.randint(0, 6)
        if self.source_hidden_layer:
            self.id_target_neuron = random.randint(0, 6)
        else:
            self.id_target_neuron = random.randint(0, 1)
        self.weight = random.uniform(-1, 1)


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

# ------------------ Fin Algoritmo genetico --------------------------------------------------------

# ------------------ Red Neuronal ------------------------------------------------------------------
    
# La red neuronal tiene dos capas: una capa oculta y una capa de salida.
# La capa oculta está representada por la matriz hidden_layer_weights y su respectivo sesgo hidden_layer_bias.
# La capa de salida está representada por la matriz output_layer_weights y su respectivo sesgo output_layer_bias.

class Brain:
    def __init__(self, genome):
        self.inputs = []
        self.outputs = [1, 0]
        # self.hidden_layer_weights = self.zeroes_matrix(7, 7)
        # self.output_layer_weights = self.zeroes_matrix(2, 7)
        self.hidden_layer_weights = self.uniform_init(7, 7, -0.5, 0.5)  # Inicialización uniforme para los pesos de la capa oculta
        self.output_layer_weights = self.uniform_init(2, 7, -0.5, 0.5)  # Inicialización uniforme para los pesos de la capa de salida
        for gen in genome.genes:
            if gen.source_hidden_layer:
                self.hidden_layer_weights[gen.id_target_neuron][gen.id_source_neuron] = gen.weight
            else:
                self.output_layer_weights[gen.id_target_neuron][gen.id_source_neuron] = gen.weight
        self.hidden_layer_bias = genome.hidden_layer_bias
        self.output_layer_bias = genome.output_layer_bias
        self.hidden_outputs = []
# --------------------- Funcionamiento de FeedForward -----------------------------------------------
# El método feed_forward toma una capa de entrada como entrada, realiza las operaciones de 
# multiplicación de matriz y vector para propagar la entrada a través de la red y produce una salida.
        
    def feed_forward(self, input_layer_values): 
        self.inputs = input_layer_values
        self.hidden_outputs = self.matrix_vector_multiplication(self.hidden_layer_weights, input_layer_values)
        self.hidden_outputs = [self.ReLU(x + bias) for x, bias in zip(self.hidden_outputs, self.hidden_layer_bias)]
        self.outputs = self.matrix_vector_multiplication(self.output_layer_weights, self.hidden_outputs)
        self.outputs = [self.ReLU(x + bias) for x, bias in zip(self.outputs, self.output_layer_bias)]
# ------------------- Funcionamiento de ReLU -----------------------------------------------------------
# La función ReLU (Rectified Linear Activation) se utiliza como función de activación en 
# las capas ocultas y de salida. ReLU devuelve cero para valores negativos y el mismo valor para valores positivos.
        
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

# --------------------------- Fin Red Neuronal -----------------------------------------------------

# ---------------------- Clase para todos los objetos del Juego - Metodo para verificar colisiones ---------

class GameObject:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.obj_width = 0
        self.obj_height = 0
        self.image = ""

    def is_collisioning_with(self, anObject):
        return (self.x_pos + self.obj_width > anObject.x_pos and self.x_pos < anObject.x_pos + anObject.obj_width) and (self.y_pos + self.obj_height  > anObject.y_pos and self.y_pos < anObject.y_pos + anObject.obj_height)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x_pos, self.y_pos))

# ------------------------- Fin -------------------------------------------------------------
        
# Representa el suelo en el juego. Se mueve en sentido contrario al movimiento de 
# los obstáculos y se reinicia cuando alcanza cierta posición.
# Hereda de GameObject.

class Ground(GameObject):
    def __init__(self):
        super().__init__()
        self.x_pos = 10
        self.y_pos = 515
        self.image = BG

 # Actualiza la posición del suelo según la velocidad del juego
        
    def update(self, speed):
        self.x_pos -= speed
        if self.x_pos <= 0:
            self.x_pos = 75

class Cloud(GameObject):
    def __init__(self):
        super().__init__()
        self.x_pos = 100
        self.y_pos = 340
        self.image = CLOUD

 # Actualiza la posición del suelo según la velocidad del juego
        
    def update(self, speed):
        self.x_pos -= speed
        if self.x_pos <= 0:
            self.x_pos = 1050

# ---------------------------- Fin -------------------------------------------------------

# Representa al dinosaurio controlado por la red neuronal en el juego. Contiene lógica 
# para saltar, agacharse, actualizar la entrada de la red neuronal y procesar las salidas 
# de la misma.
# Hereda de GameObject y Genome.

class Dino(GameObject):
    ultimo_id = 0
    def __init__(self):
        super().__init__()
        Dino.ultimo_id += 1
        self.id = Dino.ultimo_id
        self.image = DINO
        #se ata la variable del dino
        self.x_pos = 100
        #self.x_pos = random.randint(100, 300)
        self.y_pos = 450
        self.obj_width = 80
        self.obj_height = 86
        self.jump_stage = 0
        self.alive = True
        self.score = 0
        self.genome = Genome()
        self.brain = Brain(self.genome)
        self.brain_inputs = [0] * 7


    def update(self, next_obstacle_info, speed):
        self.update_brain_inputs(next_obstacle_info, speed)
        self.brain.feed_forward(self.brain_inputs)
        self.process_brain_output()
        if self.jumping():
            self.update_jump()

    def update_brain_inputs(self, next_obstacle_info, speed):
        self.brain_inputs[0] = next_obstacle_info[0] / 900  # normalized distance
        self.brain_inputs[1] = (next_obstacle_info[1] - 450) / (1350 - 450)  # normalized obstacle x pos
        self.brain_inputs[2] = (next_obstacle_info[2] - 370) / (480 - 370)  # normalized obstacle y pos
        self.brain_inputs[3] = (next_obstacle_info[3] - 30) / (146 - 30)  # normalized obstacle width
        self.brain_inputs[4] = (next_obstacle_info[4] - 40) / (96 - 40)  # normalized obstacle height
        self.brain_inputs[5] = (self.y_pos - 278) / (484 - 278)  # normalized dino y pos
        self.brain_inputs[6] = (speed - 15) / (30 - 15)  # normalized speed

    def update_jump(self):
        self.y_pos = 450 - ((-4 * self.jump_stage * (self.jump_stage - 1)) * 172)
        self.jump_stage += 0.03
        if self.jump_stage > 1:
            self.stop_jump()

    def process_brain_output(self):

        # nueva logica parecida a la anterior

        # if self.brain.outputs[0] == 0 and self.brain.outputs[1] == 0:
        #     if self.crouching():
        #         self.stop_crouch()
        #     if self.jumping():
        #         self.stop_jump()
        # elif self.brain.outputs[0] > self.brain.outputs[1]:
        #     if self.crouching():
        #         self.stop_crouch()
        #     if not self.jumping():
        #         self.jump()
        # else:
        #     if self.jumping():
        #         self.stop_jump()
        #     if not self.crouching():
        #         self.crouch()

        if self.brain.outputs[0] != 0:
            if not self.crouching() and not self.jumping():
                self.jump()
        if self.brain.outputs[1] == 0:
            if self.crouching():
                self.stop_crouch()
        else:
            if self.jumping():
                self.stop_jump()
            self.crouch()

    def jump(self):
        self.jump_stage = 0.0001

    def stop_jump(self):
        self.jump_stage = 0
        self.y_pos = 450

    def crouch(self):
        if not self.crouching():
            self.y_pos = 484
            self.obj_width = 110
            self.obj_height = 52
            self.image = DUCKING

    def stop_crouch(self):
        self.y_pos = 450
        self.obj_width = 80
        self.obj_height = 86

    def jumping(self):
        return self.jump_stage > 0

    def crouching(self):
        return self.obj_width == 110

    def die(self, sim_score):
        self.alive = False
        self.score = sim_score

    def reset(self):
        self.alive = True
        self.score = 0


class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self.x_pos = 1350

    def update(self, speed):
        self.x_pos -= speed

    def is_offscreen(self):
        return self.x_pos + self.obj_width < 0

# se creo solo 2 tipos de cactus y un pajaro, para poder atar aun mas las variables

class CactusS(Enemy):
    def __init__(self):
        super().__init__()
        self.image = SMALL_CACTUS[0]
        self.obj_width = 30
        self.obj_height = 66
        self.y_pos = 470  


class CactusL(Enemy):
    def __init__(self):
        super().__init__()
        self.image = LARGE_CACTUS[0]
        self.obj_width = 46
        self.obj_height = 96
        self.y_pos = 444 


class BirdL(Enemy):
    def __init__(self):
        super().__init__()
        self.image = BIRD
        self.y_pos = 430
        self.obj_width = 84
        self.obj_height = 40

class BirdH(Enemy):
    def __init__(self):
        super().__init__()
        self.image = BIRD
        self.y_pos = 400
        self.obj_width = 84
        self.obj_height = 40

class BirdHH(Enemy):
    def __init__(self):
        super().__init__()
        self.image = BIRD
        self.y_pos = 370
        self.obj_width = 84
        self.obj_height = 40

# -------------------- Simulación del Juego ---------------------------------------------------

# Controla la simulación del juego. Administra los dinosaurios, enemigos, puntajes, generaciones, etc. 
# Tiene métodos para actualizar el estado del juego, manejar colisiones, generar nuevos enemigos y 
# avanzar a la siguiente generación de dinosaurios.

class Simulation:
    def __init__(self):
        self.dinos = [Dino() for i in range(DINOS_PER_GENERATION)]
        self.enemies = []
        self.speed = 15
        self.ground = Ground()
        self.cloud = Cloud()
        self.score = 0
        self.generation = 1
        self.last_gen_avg_score = 0
        self.last_gen_max_score = 0
        self.dinos_alive = DINOS_PER_GENERATION
        self.last_spawn_time = millis()
        #fije el tiempo en el que respawnean los enemies
        self.time_to_spawn = MAX_SPAWN_MILLIS
        # self.time_to_spawn = random.uniform(MIN_SPAWN_MILLIS, MAX_SPAWN_MILLIS)
        self.ultimo_dino_values = []
        self.ultimo_dino_prom = 0
        self.ultimos_total_ids = []
        self.ultimos_general_ids = []
        self.ultimo_max_ids = []
        self.cont = 0
        self.gen_progress = 0
        self.ultimo_dino_score = 0
        self.ultimo_dino_obj = 0
        self.ultimo_dino_id = 0
        self.ultimo_dino_pos = 0
        self.dino_mas_ganador = 0
        self.ultimo_dino_q_gano = 0

        self.generaciones = []       # Para tomar las mediciones
        self.promedios_evolucion = []   # Para tomar las mediciones
        self.update_counter = 0  # Contador de actualización
        self.update_frequency = 100  # Frecuencia de actualización (ajustar según sea necesario)  

    def update(self):
        self.score += 1
        self.update_counter += 1
        if self.update_counter > 100:
            self.update_counter = 0
        for dino in self.dinos:
            if dino.alive:
                dino.update(self.next_obstacle_info(dino), int(self.speed))
        for enemy in self.enemies[:]:
            enemy.update(int(self.speed))
            if enemy.is_offscreen():
                self.enemies.remove(enemy)
        if millis() - self.last_spawn_time > self.time_to_spawn:
            self.spawn_enemy(self.cont)
            self.last_spawn_time = millis()
            # self.time_to_spawn = random.uniform(MIN_SPAWN_MILLIS, MAX_SPAWN_MILLIS)
        self.check_collisions()
        self.ground.update(int(self.speed))
        self.cloud.update(int(self.speed))
        self.speed += 0.001

    def print(self, SCREEN):
        self.ground.draw(SCREEN)
        self.cloud.draw(SCREEN)
        for dino in self.dinos:
            if dino.alive:
                dino.draw(SCREEN)
        for enemy in self.enemies:
            enemy.draw(SCREEN)
        self.print_info()

    def print_info(self):
        #Tipo de letra
        font = pygame.font.Font('freesansbold.ttf', 15)
        #Columna izquierda de datos
        generacion = font.render("Generation: " + str(simulation.generation), True, (0, 0, 0))
        geneRect = generacion.get_rect()
        geneRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 280)
        SCREEN.blit(generacion, geneRect)

        dinos_vivos = font.render("Dinos Vivos: " + str(len([dino for dino in simulation.dinos if dino.alive])), True, (0, 0, 0))
        dinos_vivosRect = dinos_vivos.get_rect()
        dinos_vivosRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 260)
        SCREEN.blit(dinos_vivos, dinos_vivosRect)

        score = font.render("Score: " + str(simulation.score), True, (0, 0, 0))
        scoreRect = score.get_rect()
        scoreRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 240)
        SCREEN.blit(score, scoreRect)

        maxscore = font.render("Max Score: " + str(simulation.last_gen_max_score), True, (0, 0, 0))
        maxscoreRect = maxscore.get_rect()
        maxscoreRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 220)
        SCREEN.blit(maxscore, maxscoreRect)

        avgscore = font.render("Max AVG: " + str(simulation.last_gen_avg_score), True, (0, 0, 0))
        avgscoreRect = avgscore.get_rect()
        avgscoreRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 200)
        SCREEN.blit(avgscore, avgscoreRect)

        ultimodino = font.render("Ult Dino Score: " + str(simulation.ultimo_dino_score), True, (0, 0, 0))
        ultimodinoRect = ultimodino.get_rect()
        ultimodinoRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 180)
        SCREEN.blit(ultimodino, ultimodinoRect)

        ultimodinoProm = font.render("Ult Dino Prom: " + str(simulation.ultimo_dino_prom), True, (0, 0, 0))
        ultimodinoPromRect = ultimodinoProm.get_rect()
        ultimodinoPromRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 160)
        SCREEN.blit(ultimodinoProm, ultimodinoPromRect)

        #Columna media de datos

        ult_gen_max = font.render("Ult Gen Max: " + str(simulation.gen_progress), True, (0, 0, 0))
        ult_gen_maxRect = ult_gen_max.get_rect()
        ult_gen_maxRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 280)
        SCREEN.blit(ult_gen_max, ult_gen_maxRect)

        ult_ids_max = font.render("Ult Ids Max: " + str(simulation.ultimo_max_ids), True, (0, 0, 0))
        ult_ids_maxRect = ult_ids_max.get_rect()
        ult_ids_maxRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 260)
        SCREEN.blit(ult_ids_max, ult_ids_maxRect)

        ult_ids_gral = font.render("Ult Ids Gral: " + str(simulation.ultimos_general_ids), True, (0, 0, 0))
        ult_ids_gralRect = ult_ids_gral.get_rect()
        ult_ids_gralRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 240)
        SCREEN.blit(ult_ids_gral, ult_ids_gralRect)

        ult_dino_q_gano = font.render("Ult Dino Q Gano: " + str(simulation.ultimo_dino_q_gano), True, (0, 0, 0))
        ult_dino_q_ganoRect = ult_dino_q_gano.get_rect()
        ult_dino_q_ganoRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 220)
        SCREEN.blit(ult_dino_q_gano, ult_dino_q_ganoRect)

        ult_dino_pos = font.render("Ult Dino Q Gano Pos: " + str(simulation.ultimo_dino_pos), True, (0, 0, 0))
        ult_dino_posRect = ult_dino_pos.get_rect()
        ult_dino_posRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 200)
        SCREEN.blit(ult_dino_pos, ult_dino_posRect)

        siguiendo_dino = font.render("Siguiendo Dino: " + str(simulation.ultimo_dino_id), True, (0, 0, 0))
        siguiendo_dinoRect = siguiendo_dino.get_rect()
        siguiendo_dinoRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 180)
        SCREEN.blit(siguiendo_dino, siguiendo_dinoRect)

        dino_mas_ganador = font.render("Dino + Ganador: " + str(simulation.dino_mas_ganador), True, (0, 0, 0))
        dino_mas_ganadorRect = dino_mas_ganador.get_rect()
        dino_mas_ganadorRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 160)
        SCREEN.blit(dino_mas_ganador, dino_mas_ganadorRect)

        self.print_network()
        #self.print_grafico()

    def print_network(self):
        for dino in self.dinos:
            if dino.alive:
                dino.brain.print_network(SCREEN)
                break

    # def print_grafico(self):
    #     pygame.draw.line(SCREEN, (255,0,0), (50,90), (50,60))


    def next_obstacle_info(self, dino):
        result = [1350, 0, 0, 0, 0]
        for enemy in self.enemies:
            if enemy.x_pos > dino.x_pos:
                result = [enemy.x_pos - dino.x_pos, enemy.x_pos, enemy.y_pos, enemy.obj_width, enemy.obj_height]
                break
        return result
    
    def spawn_enemy(self, cont):
        #lista para cambiar los patrones
        lista = [CactusS(), CactusL(), BirdL(), CactusS(), CactusS(), BirdH(), BirdHH()]
        self.enemies.append(lista[cont])
        self.cont += 1
        if self.cont == len(lista):
            self.cont = 0
        
    def check_collisions(self):
        self.dinos_alive = 0
        for dino in self.dinos:
            for enemy in self.enemies:
                if dino.alive and dino.is_collisioning_with(enemy):
                    dino.die(self.score)
            if dino.alive:
                self.dinos_alive += 1
        if self.dinos_alive == 0:
            self.cont = 0
            self.next_generation()

    def next_generation(self):
        self.score = 0
        self.speed = 15
        self.enemies.clear()
        self.generaciones.append(self.generation)
        if len(self.ultimos_total_ids) >= 1:
            self.ultimo_dino_q_gano = self.ultimos_total_ids[-1]
        self.dinos.sort(key=lambda x: x.score, reverse=True)
        self.ultimo_dino_id = self.dinos[0].id
        if self.ultimo_dino_obj != 0:
            self.ultimo_dino_pos = self.dinos.index(self.ultimo_dino_obj) + 1
        self.ultimo_dino_obj = self.dinos[0]
        self.ultimo_dino_score = self.dinos[0].score
        self.ultimo_dino_values.append(self.dinos[0].score)
        self.ultimos_total_ids.append(self.dinos[0].id)
        self.dino_mas_ganador = self.encontrar_repetidos(self.ultimos_total_ids)
        if len(self.ultimos_general_ids) > 3:
            self.ultimos_general_ids = []
        self.ultimos_general_ids.append(self.dinos[0].id)
        self.ultimo_dino_prom = self.avg(self.ultimo_dino_values, self.generation)
        self.promedios_evolucion.append(self.ultimo_dino_prom)
        if self.dinos[0].score > self.last_gen_max_score:
            self.gen_progress = self.generation
            if len(self.ultimo_max_ids) > 3:
                self.ultimo_max_ids = []
            self.ultimo_max_ids.append(self.dinos[0].id)
        self.generation += 1
        dinos_score_sum = sum(dino.score for dino in self.dinos)
        if dinos_score_sum // DINOS_PER_GENERATION > self.last_gen_avg_score:
            self.last_gen_avg_score = dinos_score_sum // DINOS_PER_GENERATION
        if self.dinos[0].score > self.last_gen_max_score:
            self.last_gen_max_score = self.dinos[0].score
        for dino in self.dinos:
            dino.reset()
        # new_dinos = []
        # new_dinos.extend(self.dinos[:5])
        # for dino in new_dinos:
        #     dino.reset()
        # father = self.dinos[0]
        # mather = self.dinos[1]
        # for _ in range(int(DINOS_PER_GENERATION * 0.4)):
        #     son = Dino()
        #     son.genome = father.genome.crossover(mather.genome)
        #     new_dinos.append(son)
        # for _ in range(int(DINOS_PER_GENERATION * 0.3)):
        #     son = Dino()
        #     son.genome = father.genome.mutate()
        #     new_dinos.append(son)
        # for _ in range(int(DINOS_PER_GENERATION * 0.2)):
        #     son = Dino()
        #     son.genome = random.choice(self.dinos[:5]).genome.crossover(random.choice(self.dinos[:5]).genome)
        #     new_dinos.append(son)
        # for _ in range(DINOS_PER_GENERATION - len(new_dinos)):
        #     new_dinos.append(Dino())
        # self.dinos = new_dinos

    def avg(self, values, n):
        if n == 0:
            return 0
        return sum(values) // n
    
    def encontrar_repetidos(self, lista):
        if len(lista) > 0:
            conteo = {}
            for elemento in lista:
                if elemento in conteo:
                    conteo[elemento] += 1
                else:
                    conteo[elemento] = 1
            value = 0
            key = ""
            for elemento, cantidad in conteo.items():
                if cantidad >= value:
                    value = cantidad
                    key = elemento
            return key
        else:
            return 0


def draw():
    simulation.update()
    simulation.print(SCREEN)
    # simulation.draw(SCREEN)

#pygame.display.get_surface()

pygame.init()
simulation = Simulation()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    SCREEN.fill((247, 247, 247))
    draw()

    pygame.display.flip()
    pygame.time.Clock().tick(100)