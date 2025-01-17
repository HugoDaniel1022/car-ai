import pygame
from simulation import Simulation

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# llama a los metodos update() y print() de Simulacion
def draw():
    simulation.update()
    simulation.print(SCREEN)

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