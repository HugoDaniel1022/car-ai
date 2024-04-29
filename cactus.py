import pygame
import os
from enemy import Enemy

class Cactus(Enemy):
    def __init__(self, num):
        super().__init__()
        self.num = num
        if self.num == 0:
            self.image = pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png"))
            self.obj_width = 30
            self.obj_height = 66
            self.y_pos = 470
        else:
            self.image = pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png"))
            self.obj_width = 46
            self.obj_height = 96
            self.y_pos = 444 
