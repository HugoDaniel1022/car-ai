import pygame
import os
from gameObject import GameObject
from genome import Genome
from brain import Brain

class Dino(GameObject):
    ultimo_id = 0
    def __init__(self):
        super().__init__()
        Dino.ultimo_id += 1
        self.id = Dino.ultimo_id
        self.image = pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png"))
        # se fija la posicion en el eje x del dino
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

    # actualiza toda la red neuronal, desde los datos recogidos en el ambiente hasta los datos de salida, y 
    #luego lleva a cabo los procesos de agacharse, quedarse quieto o saltar
    def update(self, next_obstacle_info, speed):
        self.update_brain_inputs(next_obstacle_info, speed)
        self.brain.feed_forward(self.brain_inputs)
        self.process_brain_output()
        if self.jumping():
            self.update_jump()

    # setea los inputs del cerebro del dino con datos tomados del ambiente y normalizados
    def update_brain_inputs(self, next_obstacle_info, speed):
        self.brain_inputs[0] = next_obstacle_info[0] / 900  # normalizacion de la distancia entre el dino y el objeto
        self.brain_inputs[1] = (next_obstacle_info[1] - 450) / (1350 - 450)  # normalizacion del eje x del enemigo
        self.brain_inputs[2] = (next_obstacle_info[2] - 370) / (480 - 370)  # normalizacion del eje y del enemigo
        self.brain_inputs[3] = (next_obstacle_info[3] - 30) / (146 - 30)  # normalizacion del ancho del enemigo
        self.brain_inputs[4] = (next_obstacle_info[4] - 40) / (96 - 40)  # normalizacion del alto del enemigo
        self.brain_inputs[5] = (self.y_pos - 278) / (484 - 278)  # normalizacion del eje y del dino
        self.brain_inputs[6] = (speed - 15) / (30 - 15)  # normalizacion de la velocidad del juego

    # actualiza el estado del dino cuando esta saltando
    def update_jump(self):
        self.y_pos = 450 - ((-4 * self.jump_stage * (self.jump_stage - 1)) * 172)
        self.jump_stage += 0.03
        if self.jump_stage > 1:
            self.stop_jump()

    # dados los resultados de salida de la red neuronal el dino se agacha, salta o no hace nada.
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

    # modifica el atributo jump_stage del dino para que el mismo pueda realizar el salto
    def jump(self):
        self.jump_stage = 0.0001

    # hace que el dino deje de saltar
    def stop_jump(self):
        self.jump_stage = 0
        self.y_pos = 450

    # hace que el dino se agache
    def crouch(self):
        if not self.crouching():
            self.y_pos = 484
            self.obj_width = 110
            self.obj_height = 52
            self.image = pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png"))

    # hace que el dino deje de agacharse
    def stop_crouch(self):
        self.y_pos = 450
        self.obj_width = 80
        self.obj_height = 86

    # retorna si el dino esta saltando o no
    def jumping(self):
        return self.jump_stage > 0
    
    # retorna si el dino esta agachado o no
    def crouching(self):
        return self.obj_width == 110

    # cuando se invoca, cambia el estado del dino de vivo a muerto y le asigna un puntaje
    def die(self, sim_score):
        self.alive = False
        self.score = sim_score

    # revive a los dinos muertos
    def reset(self):
        self.alive = True
        self.score = 0