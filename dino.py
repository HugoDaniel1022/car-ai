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
        self.image = pygame.image.load(os.path.join("images/car.png"))
        # se fija la posicion en el eje x del dino
        self.x_pos = 300
        #self.x_pos = random.randint(100, 300)
        self.y_pos = 400
        self.obj_width = 40
        self.obj_height = 80
        self.move_stage_left = 0
        self.move_stage_right = 0
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
        if self.moving_right():
            self.update_move_right()
        if self.moving_left():
            self.update_move_left()
            

    # setea los inputs del cerebro del dino con datos tomados del ambiente y normalizados
    def update_brain_inputs(self, next_obstacle_info, speed):
        self.brain_inputs[0] = next_obstacle_info[0] / 400  # normalizacion de la distancia entre el dino y el objeto
        self.brain_inputs[1] = (next_obstacle_info[1] / 400)  # normalizacion del eje y del enemigo
        self.brain_inputs[2] = (next_obstacle_info[2] - 130) / (470 - 130)  # normalizacion del eje x del enemigo
        self.brain_inputs[3] = (next_obstacle_info[3] - 40) / (60 - 40)  # normalizacion del ancho del enemigo
        self.brain_inputs[4] = (next_obstacle_info[4] - 80) / (100 - 80)  # normalizacion del alto del enemigo
        self.brain_inputs[5] = (self.x_pos - 130) / (470 - 130)  # normalizacion del eje x del dino
        self.brain_inputs[6] = (speed - 15) / (30 - 15)  # normalizacion de la velocidad del juego
        print(self.brain_inputs)

    # actualiza el estado del dino cuando esta saltando
    def update_move_left(self):
        self.x_pos = 300 - ((-4 * self.move_stage_left * (self.move_stage_left - 1)) * 172)
        self.move_stage_left += 0.03
        if self.move_stage_left > 1:
            self.stop_move_left()

    def update_move_right(self):
        self.x_pos = 300 + ((-4 * self.move_stage_right * (self.move_stage_right - 1)) * 172)
        self.move_stage_right += 0.03
        if self.move_stage_right > 1:
            self.stop_move_right()

    # dados los resultados de salida de la red neuronal el dino se agacha, salta o no hace nada.
    def process_brain_output(self):
        if self.brain.outputs[0] < self.brain.outputs[1]:
            if self.x_pos == 300:
                self.move_left()
        elif self.brain.outputs[0] > self.brain.outputs[1]:
            if self.x_pos == 300:
                self.move_right()
        # if self.brain.outputs[0] != 0:
        #     if not self.moving_right() and not self.moving_left():
        #         self.move_right()
        # if self.brain.outputs[1] == 0:
        #     if self.moving_right():
        #         self.stop_move_right()
        # else:
        #     if self.moving_left():
        #         self.stop_move_left()
        #     self.move_right()

    def move_left(self):
        self.move_stage_left = 0.0001
    
    def move_right(self):
        self.move_stage_right = 0.0001

    # hace que el dino deje de saltar
    def stop_move_left(self):
        self.move_stage_left = 0
        self.x_pos = 300

    def stop_move_right(self):
        self.move_stage_right = 0
        self.x_pos = 300

    # retorna si el dino esta saltando o no
    def moving_left(self):
        return self.move_stage_left > 0
    
    def moving_right(self):
        return self.move_stage_right > 0


    # cuando se invoca, cambia el estado del dino de vivo a muerto y le asigna un puntaje
    def die(self, sim_score):
        self.alive = False
        self.score = sim_score

    # revive a los dinos muertos
    def reset(self):
        self.alive = True
        self.score = 0