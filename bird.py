import pygame
import os
from enemy import Enemy

class Bird(Enemy):
    def __init__(self, num):
        super().__init__()
        self.num = num
        self.image = pygame.image.load(os.path.join("Assets/Bird", "Bird1.png"))
        if self.num == 0:
            self.y_pos = 380
        else:
            self.y_pos = 430
        self.obj_width = 84
        self.obj_height = 40