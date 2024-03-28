import random
import time

DINOS_PER_GENERATION = 10
MIN_SPAWN_MILLIS = 500
MAX_SPAWN_MILLIS = 1500

millis = lambda: int(round(time.time() * 1000))

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


class Brain:
    def __init__(self, genomeObject):
        self.inputs = []
        self.outputs = [1, 0]
        self.hidden_layer_weights = self.zeroes_matrix(7, 7)
        self.output_layer_weights = self.zeroes_matrix(2, 7)
        for gen in genomeObject.genes:
            if gen.source_hidden_layer:
                self.hidden_layer_weights[gen.id_target_neuron][gen.id_source_neuron] = gen.weight
            else:
                self.output_layer_weights[gen.id_target_neuron][gen.id_source_neuron] = gen.weight
        self.hidden_layer_bias = genomeObject.hidden_layer_bias
        self.output_layer_bias = genomeObject.output_layer_bias
        self.hidden_outputs = []
    
    def zeroes_matrix(self, rows, cols):
        return [[0 for _ in range(cols)] for _ in range(rows)]

    def matrix_vector_multiplication(self, matrix, vector):
        return [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]

    def feed_forward(self, input_layer_values):
        self.inputs = input_layer_values
        self.hidden_outputs = self.matrix_vector_multiplication(self.hidden_layer_weights, input_layer_values)
        self.hidden_outputs = [self.ReLU(x + bias) for x, bias in zip(self.hidden_outputs, self.hidden_layer_bias)]
        self.outputs = self.matrix_vector_multiplication(self.output_layer_weights, self.hidden_outputs)
        self.outputs = [self.ReLU(x + bias) for x, bias in zip(self.outputs, self.output_layer_bias)]

    def ReLU(self, x):
        return max(0, x)
    

class GameObject:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.obj_width = 0
        self.obj_height = 0
        self.sprite = ""
        self.sprite_offset = [0, 0]

    def is_collisioning_with(self, anObject):
        return (self.x_pos + self.obj_width > anObject.x_pos and self.x_pos < anObject.x_pos + anObject.obj_width) and (self.y_pos + self.obj_height  > anObject.y_pos and self.y_pos < anObject.y_pos + anObject.obj_height)


class Ground(GameObject):
    def __init__(self):
        super().__init__()
        self.x_pos = 2400
        self.y_pos = 515
        self.sprite = "ground"

    def update(self, speed):
        self.x_pos -= speed
        if self.x_pos <= 0:
            self.x_pos = 2400


class Dino(GameObject):
    def __init__(self):
        super().__init__()
        self.x_pos = random.randint(100, 300)
        self.y_pos = 450
        self.obj_width = 80
        self.obj_height = 86
        self.jump_stage = 0
        self.alive = True
        self.score = 0
        self.genome = Genome()
        self.brain = None
        self.brain_inputs = [0] * 7
        self.init_brain()

    def init_brain(self):
        self.brain = Brain(self.genome)

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
        self.sprite = "standing_dino"

    def stop_jump(self):
        self.jump_stage = 0
        self.y_pos = 450
        self.sprite = "walking_dino_1"

    def crouch(self):
        if not self.crouching():
            self.y_pos = 484
            self.obj_width = 110
            self.obj_height = 52
            self.sprite = "crouching_dino_1"

    def stop_crouch(self):
        self.y_pos = 450
        self.obj_width = 80
        self.obj_height = 86
        self.sprite = "walking_dino_1"

    def jumping(self):
        return self.jump_stage > 0

    def crouching(self):
        return self.obj_width == 110

    def die(self, sim_score):
        self.alive = False
        self.score = sim_score
        print("ESTOY RE DEAAAAAAAD")

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
        self.cactus_widths = [30, 64, 98, 46, 96, 146]
        self.cactus_heights = [66, 66, 66, 96, 96, 96]
        self.cactus_y_pos = [470, 470, 470, 444, 444, 444]
        self.obj_width = self.cactus_widths[self.type]
        self.obj_height = self.cactus_heights[self.type]
        self.y_pos = self.cactus_y_pos[self.type]
        self.sprite = "cactus_type_" + str(self.type + 1)
        self.sprite_offset = [-2, -2]


class Bird(Enemy):
    def __init__(self):
        super().__init__()
        self.birds_y_pos = [435, 480, 370]
        self.obj_width = 84
        self.obj_height = 40
        self.type = random.randint(0, 2)
        self.y_pos = self.birds_y_pos[self.type]
        self.sprite = "bird_flying_1"
        self.sprite_offset = [-4, -16]


class Simulation:
    def __init__(self):
        self.dinos = [Dino() for _ in range(DINOS_PER_GENERATION)]
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
                    self.dinos.remove(dino)
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

    def next_generation(self):
        print("Nueva generacion")



# dino = Dino()
# cactus = Cactus()
# for i in range(10):
#     print(dino.x_pos, dino.y_pos, cactus.x_pos, cactus.y_pos)
#     cactus.x_pos -= 200
#     print(dino.is_collisioning_with(cactus))
#     time.sleep(1)

# simu1 = Simulation()
# for i in range(100):
#     simu1.update()
#     for dino in simu1.dinos:
#         print(f"\ndino {simu1.dinos.index(dino)}")
#         print("score: ", simu1.score)
#         # print("inputs: ", dino.brain.inputs)
#         print("OUTPUTS: ", dino.brain.outputs)
#         print(f"jumping: {dino.jumping()} - crouching: {dino.crouching()}")
#     time.sleep(2)


        
    # print("\nhidden_layer_weights: ", simu1.dinos[0].brain.hidden_layer_weights)
    # print("\noutput_layer_weights: ", simu1.dinos[0].brain.output_layer_weights)
    # print("\nhidden_layer_bias: ", simu1.dinos[0].brain.hidden_layer_bias)
    # print("\noutput_layer_bias: ", simu1.dinos[0].brain.output_layer_bias)
    # print("\nhidden_outputs: ", simu1.dinos[0].brain.hidden_outputs)

    # print("simu1.speed: ", simu1.speed)
    # print("simu1.gound: ", simu1.ground)
    # print("simu1.score: ", simu1.score)
    # print("simu1.generation: ", simu1.generation)
    # print("simu1.last_gen_avg_score: ", simu1.last_gen_avg_score)
    # print("simu1.last_gen_max_score: ", simu1.last_gen_max_score)
    # print("simu1.dinos_alive: ", simu1.dinos_alive)
    # print("simu1.last_spawn_time: ", simu1.last_spawn_time)
    # print("simu1.time_to_spawn: ", simu1.time_to_spawn)
    #time.sleep(5)



# dino1  = Dino()
# print(dino1.brain.inputs)
# print(dino1.brain.outputs)
# print(dino1.brain.hidden_outputs)
# dino1.update([0,0,0,0,0], 15)
# print(dino1.brain.inputs)
# print(dino1.brain.outputs)
# print(dino1.brain.hidden_outputs)

    
# genoma1 = Genome()
# brian1 = Brain(genoma1)
# print(brian1.hidden_layer_weights)
# print(brian1.output_layer_weights)
# print(brian1.inputs)
# print(brian1.outputs)
# print("hidden_layer_weights")
# print(brian1.hidden_layer_weights)
# print("output_layer_weights")
# print(brian1.output_layer_weights)
# print("hidden_layer_bias")
# print(brian1.hidden_layer_bias)
# print("output_layer_bias")
# print(brian1.output_layer_bias)
# print("hidden_outputs")
# print(brian1.hidden_outputs)