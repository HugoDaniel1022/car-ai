import pygame
from simulation import Simulation

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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