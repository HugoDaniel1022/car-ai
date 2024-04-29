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
            self.image = pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png"))

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