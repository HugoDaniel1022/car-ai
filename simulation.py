import time
import pygame
import random 
from dino import Dino
from bird import Bird

# funcion que devuelve el tiempo actual, se usa para respawnear a los enemigos
millis = lambda: int(round(time.time() * 1000))
# de aca se setea la cantidad de dinos por generacion (colocar siempre multiplos de 10)
DINOS_PER_GENERATION = 50
# tiempo minimo de respawneo
MIN_SPAWN_MILLIS = 1500
# tiempo maximo de respawneo
MAX_SPAWN_MILLIS = 2500

# medidas de la pantalla
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Simulation:
    def __init__(self):
        self.dinos = [Dino() for i in range(DINOS_PER_GENERATION)]
        self.enemies = []
        self.speed = 15
        self.score = 0
        self.generation = 1
        self.last_gen_avg_score = 0
        self.last_gen_max_score = 0
        self.dinos_alive = DINOS_PER_GENERATION
        self.last_spawn_time = millis()
        # fije el tiempo en el que respawnean los enemies
        self.time_to_spawn = MAX_SPAWN_MILLIS
        # self.time_to_spawn = random.uniform(MIN_SPAWN_MILLIS, MAX_SPAWN_MILLIS)
        self.ultimo_dino_values = []
        self.ultimo_dino_prom = 0
        self.cont = 0
        self.gen_progress = 0
        self.ultimo_dino_score = 0

    # Actualiza la situacion del juego, hace correr el puntaje, actualiza a los dinos que estan vivos. 
    #Si hay enemigos les va actualizando la posicion en el eje x con respecto a la velocidad que tiene el juego,
    #si el enemigo esta fuera de la pantalla lo remueve, tambien crea nuevos enemigos dependiendo de el tiempo 
    #de respawneo, verifica si hay colisiones y va acelerando la velocidad del juego.
    def update(self):
        self.score += 1
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
        self.speed += 0.001

    # imprime a los dinos y enemigos que estan vivos dentro del juego, y asi como tambien la info
    def print(self, SCREEN):
        for dino in self.dinos:
            if dino.alive:
                dino.draw(SCREEN)
        for enemy in self.enemies:
            enemy.draw(SCREEN)
        self.print_info()

    # imprime la informacion util por pantalla
    def print_info(self):
        #Tipo de letra
        font = pygame.font.Font('freesansbold.ttf', 30)
 
        generacion = font.render("Generation: " + str(self.generation), True, (0, 0, 0))
        geneRect = generacion.get_rect()
        geneRect.center = (SCREEN_WIDTH // 2 - 0, SCREEN_HEIGHT // 2 - 250)
        SCREEN.blit(generacion, geneRect)

        dinos_vivos = font.render("Autos Vivos: " + str(len([dino for dino in self.dinos if dino.alive])), True, (0, 0, 0))
        dinos_vivosRect = dinos_vivos.get_rect()
        dinos_vivosRect.center = (SCREEN_WIDTH // 2 - 0, SCREEN_HEIGHT // 2 - 200)
        SCREEN.blit(dinos_vivos, dinos_vivosRect)

        score = font.render("Score: " + str(self.score), True, (0, 0, 0))
        scoreRect = score.get_rect()
        scoreRect.center = (SCREEN_WIDTH // 2 - 0, SCREEN_HEIGHT // 2 - 150)
        SCREEN.blit(score, scoreRect)

        maxscore = font.render("Max Score: " + str(self.last_gen_max_score), True, (0, 0, 0))
        maxscoreRect = maxscore.get_rect()
        maxscoreRect.center = (SCREEN_WIDTH // 2 - 0, SCREEN_HEIGHT // 2 - 100)
        SCREEN.blit(maxscore, maxscoreRect)

        # avgscore = font.render("Max AVG: " + str(self.last_gen_avg_score), True, (0, 0, 0))
        # avgscoreRect = avgscore.get_rect()
        # avgscoreRect.center = (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 200)
        # SCREEN.blit(avgscore, avgscoreRect)

        # ultimodino = font.render("Ult Auto Score: " + str(self.ultimo_dino_score), True, (0, 0, 0))
        # ultimodinoRect = ultimodino.get_rect()
        # ultimodinoRect.center = (SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 2 - 100)
        # SCREEN.blit(ultimodino, ultimodinoRect)

        # ultimodinoProm = font.render("Ult Auto Prom: " + str(self.ultimo_dino_prom), True, (0, 0, 0))
        # ultimodinoPromRect = ultimodinoProm.get_rect()
        # ultimodinoPromRect.center = (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 250)
        # SCREEN.blit(ultimodinoProm, ultimodinoPromRect)


        ult_gen_max = font.render("Ult Gen Max: " + str(self.gen_progress), True, (0, 0, 0))
        ult_gen_maxRect = ult_gen_max.get_rect()
        ult_gen_maxRect.center = (SCREEN_WIDTH // 2 - 0, SCREEN_HEIGHT // 2 - 50)
        SCREEN.blit(ult_gen_max, ult_gen_maxRect)

        #self.print_network()


    # imprime la red neuronal de los dinos vivos
    def print_network(self):
        for dino in self.dinos:
            if dino.alive:
                dino.brain.print_network(SCREEN)
                break

    # obtiene las variables del ambiente para enviar los datos de entrada al cerebro del dino
    def next_obstacle_info(self, dino):
        result = [0, 0, 0, 0, 0]
        for enemy in self.enemies:
            if enemy.y_pos < dino.y_pos:
                result = [dino.y_pos - enemy.y_pos, enemy.y_pos, enemy.x_pos, enemy.obj_width, enemy.obj_height]
                break
        print(result)
        return result
    
    # hace que aparezcan los enemigos en la pantalla, de momento para la prueba se fijan un total de 7 enemigos,
    #y se vuelve a repetir el ciclo para saber si vedaderamente nuestro dino esta aprendiendo
    def spawn_enemy(self, cont):
        #lista para cambiar los patrones
        lista = [Bird(0), Bird(2), Bird(1)]
        self.enemies.append(lista[cont])
        self.cont += 1
        if self.cont == len(lista):
            self.cont = 0

    # chequea si hay colisiones entre el dino y alguno de los enemigos, si es asi elimina a los dinos que 
    #hayan chocado con algun objeto, cuando los dinos vivos sea = a 0, ejecuta la funcion next_generation()
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

    # crea una nueva generacion, al mismo tiempo resetea a valores originales el score y la velocidad, elimina 
    #a todos los enemigos, ordena a los dinos por puntaje y los deja preparados para el algoritmo genetico. 
    #Tambien va seteando algunos valores maximos que se van consiguiendo a medida que los dinos van evolucionando. 
    #La parte importante crea una lista nueva que sera la proxima generacion y luego rellena la misma con los 
    #primeros 5 ganadores, luego usa al dino que salio primero para mutarlo en cierta proporcion de muestras y 
    #en otro tanto los entrecruza con los genes del dino que salio 2, de esta manera se mantienen los genes 
    #ganadores y al mismo tiempo se consiguen mutaciones de los mismos y entrecruzamientos dejando una 
    #generacion en teoria mejor que la anterior. Este ciclo se repite la infinitamente.
    def next_generation(self):
        self.score = 0
        self.speed = 15
        self.enemies.clear()
        self.dinos.sort(key=lambda x: x.score, reverse=True)
        self.ultimo_dino_score = self.dinos[0].score
        self.ultimo_dino_values.append(self.dinos[0].score)
        self.ultimo_dino_prom = self.avg(self.ultimo_dino_values, self.generation)
        if self.dinos[0].score > self.last_gen_max_score:
            self.gen_progress = self.generation
        self.generation += 1
        dinos_score_sum = sum(dino.score for dino in self.dinos)
        if dinos_score_sum // DINOS_PER_GENERATION > self.last_gen_avg_score:
            self.last_gen_avg_score = dinos_score_sum // DINOS_PER_GENERATION
        if self.dinos[0].score > self.last_gen_max_score:
            self.last_gen_max_score = self.dinos[0].score
        # for dino in self.dinos:
        #     dino.reset()
        new_dinos = []
        new_dinos.extend(self.dinos[:5])
        for dino in new_dinos:
            dino.reset()
        father = self.dinos[0]
        mather = self.dinos[1]
        for _ in range(int(DINOS_PER_GENERATION * 0.4)):
            son = Dino()
            son.genome = father.genome.crossover(mather.genome)
            new_dinos.append(son)
        for _ in range(int(DINOS_PER_GENERATION * 0.3)):
            son = Dino()
            son.genome = father.genome.mutate()
            new_dinos.append(son)
        for _ in range(int(DINOS_PER_GENERATION * 0.2)):
            son = Dino()
            son.genome = random.choice(self.dinos[:5]).genome.crossover(random.choice(self.dinos[:5]).genome)
            new_dinos.append(son)
        for _ in range(DINOS_PER_GENERATION - len(new_dinos)):
            new_dinos.append(Dino())
        self.dinos = new_dinos

    # saca el promedio entre valores y cantidad de valores que se le pasen por parametro
    def avg(self, values, n):
        if n == 0:
            return 0
        return sum(values) // n
    
    # funcion fuera de uso por el momento, busca valores repetidos(se creo para futuro hacer investigacion)
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