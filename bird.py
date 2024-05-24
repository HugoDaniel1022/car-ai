import pygame
import os
from enemy import Enemy

class Bird(Enemy):
    def __init__(self, num):
        super().__init__()
        self.num = num
        if self.num == 0:
            self.image = pygame.image.load(os.path.join("images/taxi.png"))
            self.x_pos = 470
            self.obj_width = 40
            self.obj_height = 80
        elif self.num == 1:
            self.image = pygame.image.load(os.path.join("images/van.png"))
            self.x_pos = 300
            self.obj_width = 50
            self.obj_height = 90
        else:
            self.image = pygame.image.load(os.path.join("images/semi_trailer.png"))
            self.x_pos = 130
            self.obj_width = 60
            self.obj_height = 100