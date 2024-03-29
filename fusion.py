import pygame
import os
import random
import time

pygame.init()

# Global Constants
millis = lambda: int(round(time.time() * 1000))

DINOS_PER_GENERATION = 500
MIN_SPAWN_MILLIS = 2500
MAX_SPAWN_MILLIS = 5000

DINOS_POR_GENERACION = 100
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

class Gen:
    def __init__(self):
        self.source_hidden_layer = random.random() < 0.5
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
        self.hidden_layer_bias = self.random_vector(7)
        self.output_layer_bias = self.random_vector(2)

    def random_vector(self, size):
        return [random.uniform(-1, 1) for _ in range(size)]
    
    def copy(self):
        copy = Genome()
        copy.genes = [gen for gen in self.genes]
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


class Ground(GameObject):
    def __init__(self):
        super().__init__()
        self.x_pos = 2400
        self.y_pos = 515
        self.image = BG

    def update(self, speed):
        self.x_pos -= speed
        if self.x_pos <= 0:
            self.x_pos = 2400


class Dino(GameObject):
    def __init__(self):
        super().__init__()
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        # self.dino_duck = False
        # self.dino_run = True
        # self.dino_jump = False
        self.image = self.run_img[0]
        self.step_index = 0
        self.dino_rect = self.image.get_rect()
        self.x_pos = random.randint(100, 300)
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
        #self.image = self.run_img[self.step_index // 5]
        # self.dino_rect = self.image.get_rect()
        # self.step_index += 1

    def crouch(self):
        if not self.crouching():
            self.y_pos = 484
            self.obj_width = 110
            self.obj_height = 52
            #self.image = self.duck_img[self.step_index // 5]
            # self.dino_rect = self.image.get_rect()
            # self.step_index += 1

    def stop_crouch(self):
        self.y_pos = 450
        self.obj_width = 80
        self.obj_height = 86
        #self.image = self.run_img[self.step_index // 5]
        # self.dino_rect = self.image.get_rect()
        # self.step_index += 1

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


class Cactus(Enemy):
    def __init__(self):
        super().__init__()
        self.type = random.randint(0, 5)
        if self.type == 0:
            self.image = SMALL_CACTUS[0]
            self.obj_width = 30
            self.obj_height = 66
            if random.randint(0,1) == 0:
                self.y_pos = 444
            else:
                self.y_pos = 470            
        if self.type == 1:
            self.image = SMALL_CACTUS[1]
            self.obj_width = 64
            self.obj_height = 66
            if random.randint(0,1) == 0:
                self.y_pos = 444
            else:
                self.y_pos = 470
        if self.type == 2:
            self.image = SMALL_CACTUS[2]
            self.obj_width = 98
            self.obj_height = 66
            if random.randint(0,1) == 0:
                self.y_pos = 444
            else:
                self.y_pos = 470
        if self.type == 3:
            self.image = LARGE_CACTUS[0]
            self.obj_width = 46
            self.obj_height = 96
            if random.randint(0,1) == 0:
                self.y_pos = 444
            else:
                self.y_pos = 470
        if self.type == 4:
            self.image = LARGE_CACTUS[1]
            self.obj_width = 96
            self.obj_height = 96
            if random.randint(0,1) == 0:
                self.y_pos = 444
            else:
                self.y_pos = 470
        if self.type == 5:
            self.image = LARGE_CACTUS[2]
            self.obj_width = 146
            self.obj_height = 96
            if random.randint(0,1) == 0:
                self.y_pos = 444
            else:
                self.y_pos = 470


class Bird(Enemy):
    def __init__(self):
        super().__init__()
        self.type = random.randint(0, 1)
        if self.type == 0:
            self.image = BIRD[0]
            self.y_pos = 100
        else:
            self.image = BIRD[1]
            self.y_pos = 200
        self.obj_width = 84
        self.obj_height = 40


class Simulation:
    def __init__(self):
        self.dinos = [Dino() for _ in range(DINOS_PER_GENERATION)]
        self.dinos
        self.enemies = []
        self.speed = 15
        self.ground = Ground()
        self.score = 0
        self.generation = 1
        self.last_gen_avg_score = 0
        self.last_gen_max_score = 0
        self.dinos_alive = DINOS_PER_GENERATION
        self.last_spawn_time = millis()
        self.time_to_spawn = random.uniform(MIN_SPAWN_MILLIS, MAX_SPAWN_MILLIS)

    def update(self):
        #coloco a mano contador de puntaje luego sacarlo
        self.score += 1
        for dino in self.dinos:
            if dino.alive:
                dino.update(self.next_obstacle_info(dino), int(self.speed))
        for enemy in self.enemies[:]:
            enemy.update(int(self.speed))
            if enemy.is_offscreen():
                self.enemies.remove(enemy)
        if millis() - self.last_spawn_time > self.time_to_spawn:
            self.spawn_enemy()
            self.last_spawn_time = millis()
            self.time_to_spawn = random.uniform(MIN_SPAWN_MILLIS, MAX_SPAWN_MILLIS)
        self.check_collisions()
        self.ground.update(int(self.speed))
        self.speed += 0.001

    def check_collisions(self):
        self.dinos_alive = 0
        for dino in self.dinos:
            for enemy in self.enemies:
                if dino.alive and dino.is_collisioning_with(enemy):
                    dino.die(self.score)
                    #aca hice remover a los dinos pero hay que sacar esta linea
                    #self.dinos.remove(dino)
            if dino.alive:
                self.dinos_alive += 1
        if self.dinos_alive == 0:
            self.next_generation()

    def next_obstacle_info(self, dino):
        result = [1280, 0, 0, 0, 0]
        for enemy in self.enemies:
            if enemy.x_pos > dino.x_pos:
                result = [enemy.x_pos - dino.x_pos, enemy.x_pos, enemy.y_pos, enemy.obj_width, enemy.obj_height]
                break
        return result
    
    def spawn_enemy(self):
        if random.random() < 0.5:
            self.enemies.append(Cactus())
        else:
            self.enemies.append(Bird())
    
    def print(self, SCREEN):
        self.ground.draw(SCREEN)
        for enemy in self.enemies:
            enemy.draw(SCREEN)
        for dino in self.dinos:
            if dino.alive:
                dino.draw(SCREEN)

    def next_generation(self):
        print("NUEVA GENERACION")
        self.score = 0
        self.generation += 1
        self.speed = 15
        self.enemies.clear()
        dinos_score_sum = sum(dino.score for dino in self.dinos)
        self.last_gen_avg_score = dinos_score_sum // DINOS_PER_GENERATION
        self.dinos.sort(key=lambda x: x.score, reverse=True)
        self.last_gen_max_score = self.dinos[0].score
        # recoleccion de datos para posterior probar una teoria
        datos_genes = []
        for i in self.dinos[0].genome.genes:
            dic = {}
            dic["source_hidden_layer"] = i.source_hidden_layer
            dic["id_source_neuron"] = i.id_source_neuron
            dic["id_target_neuron"] = i.id_target_neuron
            dic["weight"] = i.weight
            datos_genes.append(dic)
        datos_brain = {}
        datos_brain["hidden_layer_weights"] = self.dinos[0].brain.hidden_layer_weights
        datos_brain["output_layer_weights"] = self.dinos[0].brain.output_layer_weights
        datos_brain["hidden_layer_bias"] = self.dinos[0].brain.hidden_layer_bias
        datos_brain["output_layer_bias"] = self.dinos[0].brain.output_layer_bias
        datos_genes.append(datos_brain)

        new_dinos = []
        new_dinos.extend(self.dinos[:int(DINOS_PER_GENERATION * 0.05)])
        for _ in range(int(DINOS_PER_GENERATION * 0.05)):
            new_dinos.append(Dino())
        for _ in range(int(DINOS_PER_GENERATION * 0.3)):
            father = self.dinos[0]
            son = Dino()
            son.genome = father.genome.mutate()
            new_dinos.append(son)
        for _ in range(int(DINOS_PER_GENERATION * 0.4)):
            father = random.choice(self.dinos[:int(DINOS_PER_GENERATION * 0.05)])
            son = Dino()
            son.genome = father.genome.mutate()
            new_dinos.append(son)
        for _ in range(int(DINOS_PER_GENERATION * 0.2)):
            father = random.choice(self.dinos[:int(DINOS_PER_GENERATION * 0.05)])
            mother = random.choice(self.dinos[:int(DINOS_PER_GENERATION * 0.05)])
            son = Dino()
            son.genome = father.genome.crossover(mother.genome)
            new_dinos.append(son)
        self.dinos = new_dinos


def setup():
    global simulation
    pygame.init()
    pygame.display.set_mode((1280, 720))
    simulation = Simulation()

def draw():
    screen.fill((247, 247, 247))
    simulation.update()
    simulation.print(SCREEN)
    font = pygame.font.Font('freesansbold.ttf', 30)
    score = font.render("Score: " + str(simulation.score), True, (0, 0, 0))
    scoreRect = score.get_rect()
    scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 -200)
    SCREEN.blit(score, scoreRect)
    generacion = font.render("Generation: " + str(simulation.generation), True, (0, 0, 0))
    geneRect = generacion.get_rect()
    geneRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 250)
    SCREEN.blit(generacion, geneRect)
    maxscore = font.render("Max Score: " + str(simulation.last_gen_max_score), True, (0, 0, 0))
    maxscoreRect = maxscore.get_rect()
    maxscoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
    SCREEN.blit(maxscore, maxscoreRect)



setup()
screen = pygame.display.get_surface()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw()

    pygame.display.flip()
    pygame.time.Clock().tick(60)