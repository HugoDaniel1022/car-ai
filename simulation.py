import time
import pygame
from dino import Dino
from cactus import Cactus
from bird import Bird

millis = lambda: int(round(time.time() * 1000))
DINOS_PER_GENERATION = 100
MIN_SPAWN_MILLIS = 1500
MAX_SPAWN_MILLIS = 2500
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Simulation:
    def __init__(self):
        self.dinos = [Dino() for i in range(DINOS_PER_GENERATION)]
        self.enemies = []
        self.speed = 15
        # self.ground = Ground()
        # self.cloud = Cloud()
        self.score = 0
        self.generation = 1
        self.last_gen_avg_score = 0
        self.last_gen_max_score = 0
        self.dinos_alive = DINOS_PER_GENERATION
        self.last_spawn_time = millis()
        #fije el tiempo en el que respawnean los enemies
        self.time_to_spawn = MAX_SPAWN_MILLIS
        # self.time_to_spawn = random.uniform(MIN_SPAWN_MILLIS, MAX_SPAWN_MILLIS)
        self.ultimo_dino_values = []
        self.ultimo_dino_prom = 0
        self.ultimos_total_ids = []
        self.ultimos_general_ids = []
        self.ultimo_max_ids = []
        self.cont = 0
        self.gen_progress = 0
        self.ultimo_dino_score = 0
        self.ultimo_dino_obj = 0
        self.ultimo_dino_id = 0
        self.ultimo_dino_pos = 0
        self.dino_mas_ganador = 0
        self.ultimo_dino_q_gano = 0

        self.generaciones = []       # Para tomar las mediciones
        self.promedios_evolucion = []   # Para tomar las mediciones
        self.update_counter = 0  # Contador de actualización
        self.update_frequency = 100  # Frecuencia de actualización (ajustar según sea necesario)  

    def update(self):
        self.score += 1
        self.update_counter += 1
        if self.update_counter > 100:
            self.update_counter = 0
        for dino in self.dinos:
            if dino.alive:
                dino.update(self.next_obstacle_info(dino), int(self.speed))
        for enemy in self.enemies[:]:
            enemy.update(int(self.speed))
            if enemy.is_offscreen():
                self.enemies.remove(enemy)
        if millis() - self.last_spawn_time > self.time_to_spawn:
            self.spawn_enemy(self.cont)
            self.last_spawn_time = millis()
            # self.time_to_spawn = random.uniform(MIN_SPAWN_MILLIS, MAX_SPAWN_MILLIS)
        self.check_collisions()
        # self.ground.update(int(self.speed))
        # self.cloud.update(int(self.speed))
        self.speed += 0.001

    def print(self, SCREEN):
        # self.ground.draw(SCREEN)
        # self.cloud.draw(SCREEN)
        for dino in self.dinos:
            if dino.alive:
                dino.draw(SCREEN)
        for enemy in self.enemies:
            enemy.draw(SCREEN)
        self.print_info()

    def print_info(self):
        #Tipo de letra
        font = pygame.font.Font('freesansbold.ttf', 15)
        #Columna izquierda de datos
        generacion = font.render("Generation: " + str(self.generation), True, (0, 0, 0))
        geneRect = generacion.get_rect()
        geneRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 280)
        SCREEN.blit(generacion, geneRect)

        dinos_vivos = font.render("Dinos Vivos: " + str(len([dino for dino in self.dinos if dino.alive])), True, (0, 0, 0))
        dinos_vivosRect = dinos_vivos.get_rect()
        dinos_vivosRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 260)
        SCREEN.blit(dinos_vivos, dinos_vivosRect)

        score = font.render("Score: " + str(self.score), True, (0, 0, 0))
        scoreRect = score.get_rect()
        scoreRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 240)
        SCREEN.blit(score, scoreRect)

        maxscore = font.render("Max Score: " + str(self.last_gen_max_score), True, (0, 0, 0))
        maxscoreRect = maxscore.get_rect()
        maxscoreRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 220)
        SCREEN.blit(maxscore, maxscoreRect)

        avgscore = font.render("Max AVG: " + str(self.last_gen_avg_score), True, (0, 0, 0))
        avgscoreRect = avgscore.get_rect()
        avgscoreRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 200)
        SCREEN.blit(avgscore, avgscoreRect)

        ultimodino = font.render("Ult Dino Score: " + str(self.ultimo_dino_score), True, (0, 0, 0))
        ultimodinoRect = ultimodino.get_rect()
        ultimodinoRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 180)
        SCREEN.blit(ultimodino, ultimodinoRect)

        ultimodinoProm = font.render("Ult Dino Prom: " + str(self.ultimo_dino_prom), True, (0, 0, 0))
        ultimodinoPromRect = ultimodinoProm.get_rect()
        ultimodinoPromRect.center = (SCREEN_WIDTH // 2 - 480, SCREEN_HEIGHT // 2 - 160)
        SCREEN.blit(ultimodinoProm, ultimodinoPromRect)

        #Columna media de datos

        ult_gen_max = font.render("Ult Gen Max: " + str(self.gen_progress), True, (0, 0, 0))
        ult_gen_maxRect = ult_gen_max.get_rect()
        ult_gen_maxRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 280)
        SCREEN.blit(ult_gen_max, ult_gen_maxRect)

        ult_ids_max = font.render("Ult Ids Max: " + str(self.ultimo_max_ids), True, (0, 0, 0))
        ult_ids_maxRect = ult_ids_max.get_rect()
        ult_ids_maxRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 260)
        SCREEN.blit(ult_ids_max, ult_ids_maxRect)

        ult_ids_gral = font.render("Ult Ids Gral: " + str(self.ultimos_general_ids), True, (0, 0, 0))
        ult_ids_gralRect = ult_ids_gral.get_rect()
        ult_ids_gralRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 240)
        SCREEN.blit(ult_ids_gral, ult_ids_gralRect)

        ult_dino_q_gano = font.render("Ult Dino Q Gano: " + str(self.ultimo_dino_q_gano), True, (0, 0, 0))
        ult_dino_q_ganoRect = ult_dino_q_gano.get_rect()
        ult_dino_q_ganoRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 220)
        SCREEN.blit(ult_dino_q_gano, ult_dino_q_ganoRect)

        ult_dino_pos = font.render("Ult Dino Q Gano Pos: " + str(self.ultimo_dino_pos), True, (0, 0, 0))
        ult_dino_posRect = ult_dino_pos.get_rect()
        ult_dino_posRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 200)
        SCREEN.blit(ult_dino_pos, ult_dino_posRect)

        siguiendo_dino = font.render("Siguiendo Dino: " + str(self.ultimo_dino_id), True, (0, 0, 0))
        siguiendo_dinoRect = siguiendo_dino.get_rect()
        siguiendo_dinoRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 180)
        SCREEN.blit(siguiendo_dino, siguiendo_dinoRect)

        dino_mas_ganador = font.render("Dino + Ganador: " + str(self.dino_mas_ganador), True, (0, 0, 0))
        dino_mas_ganadorRect = dino_mas_ganador.get_rect()
        dino_mas_ganadorRect.center = (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 160)
        SCREEN.blit(dino_mas_ganador, dino_mas_ganadorRect)

        self.print_network()
        #self.print_grafico()

    def print_network(self):
        for dino in self.dinos:
            if dino.alive:
                dino.brain.print_network(SCREEN)
                break

    # def print_grafico(self):
    #     pygame.draw.line(SCREEN, (255,0,0), (50,90), (50,60))


    def next_obstacle_info(self, dino):
        result = [1350, 0, 0, 0, 0]
        for enemy in self.enemies:
            if enemy.x_pos > dino.x_pos:
                result = [enemy.x_pos - dino.x_pos, enemy.x_pos, enemy.y_pos, enemy.obj_width, enemy.obj_height]
                break
        return result
    
    def spawn_enemy(self, cont):
        #lista para cambiar los patrones
        lista = [Cactus(0), Cactus(1), Bird(0), Cactus(1), Cactus(1), Bird(0), Bird(1)]
        self.enemies.append(lista[cont])
        self.cont += 1
        if self.cont == len(lista):
            self.cont = 0
        
    def check_collisions(self):
        self.dinos_alive = 0
        for dino in self.dinos:
            for enemy in self.enemies:
                if dino.alive and dino.is_collisioning_with(enemy):
                    dino.die(self.score)
            if dino.alive:
                self.dinos_alive += 1
        if self.dinos_alive == 0:
            self.cont = 0
            self.next_generation()

    def next_generation(self):
        self.score = 0
        self.speed = 15
        self.enemies.clear()
        self.generaciones.append(self.generation)
        if len(self.ultimos_total_ids) >= 1:
            self.ultimo_dino_q_gano = self.ultimos_total_ids[-1]
        self.dinos.sort(key=lambda x: x.score, reverse=True)
        self.ultimo_dino_id = self.dinos[0].id
        if self.ultimo_dino_obj != 0:
            self.ultimo_dino_pos = self.dinos.index(self.ultimo_dino_obj) + 1
        self.ultimo_dino_obj = self.dinos[0]
        self.ultimo_dino_score = self.dinos[0].score
        self.ultimo_dino_values.append(self.dinos[0].score)
        self.ultimos_total_ids.append(self.dinos[0].id)
        self.dino_mas_ganador = self.encontrar_repetidos(self.ultimos_total_ids)
        if len(self.ultimos_general_ids) > 3:
            self.ultimos_general_ids = []
        self.ultimos_general_ids.append(self.dinos[0].id)
        self.ultimo_dino_prom = self.avg(self.ultimo_dino_values, self.generation)
        self.promedios_evolucion.append(self.ultimo_dino_prom)
        if self.dinos[0].score > self.last_gen_max_score:
            self.gen_progress = self.generation
            if len(self.ultimo_max_ids) > 3:
                self.ultimo_max_ids = []
            self.ultimo_max_ids.append(self.dinos[0].id)
        self.generation += 1
        dinos_score_sum = sum(dino.score for dino in self.dinos)
        if dinos_score_sum // DINOS_PER_GENERATION > self.last_gen_avg_score:
            self.last_gen_avg_score = dinos_score_sum // DINOS_PER_GENERATION
        if self.dinos[0].score > self.last_gen_max_score:
            self.last_gen_max_score = self.dinos[0].score
        for dino in self.dinos:
            dino.reset()
        # new_dinos = []
        # new_dinos.extend(self.dinos[:5])
        # for dino in new_dinos:
        #     dino.reset()
        # father = self.dinos[0]
        # mather = self.dinos[1]
        # for _ in range(int(DINOS_PER_GENERATION * 0.4)):
        #     son = Dino()
        #     son.genome = father.genome.crossover(mather.genome)
        #     new_dinos.append(son)
        # for _ in range(int(DINOS_PER_GENERATION * 0.3)):
        #     son = Dino()
        #     son.genome = father.genome.mutate()
        #     new_dinos.append(son)
        # for _ in range(int(DINOS_PER_GENERATION * 0.2)):
        #     son = Dino()
        #     son.genome = random.choice(self.dinos[:5]).genome.crossover(random.choice(self.dinos[:5]).genome)
        #     new_dinos.append(son)
        # for _ in range(DINOS_PER_GENERATION - len(new_dinos)):
        #     new_dinos.append(Dino())
        # self.dinos = new_dinos

    def avg(self, values, n):
        if n == 0:
            return 0
        return sum(values) // n
    
    def encontrar_repetidos(self, lista):
        if len(lista) > 0:
            conteo = {}
            for elemento in lista:
                if elemento in conteo:
                    conteo[elemento] += 1
                else:
                    conteo[elemento] = 1
            value = 0
            key = ""
            for elemento, cantidad in conteo.items():
                if cantidad >= value:
                    value = cantidad
                    key = elemento
            return key
        else:
            return 0