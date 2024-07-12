import os
import neat
import math
import pygame
import random

from dinosaur import Dinosaur, SmallCactus, LargeCactus


pygame.init()
pygame.display.set_caption('Intelli-REX')
pygame.display.set_icon(pygame.image.load('./assets/icon/favicon.png'))

# constants
WIDTH = 1100
HEIGHT = 600
FPS = 30
FONT = pygame.font.SysFont(name='comicsansms', size=20, bold=True)
BG = pygame.image.load('./assets/Other/Track.png')
SMALL_CACTUS = [pygame.image.load('./assets/Cactus/SmallCactus1.png'),
                pygame.image.load('./assets/Cactus/SmallCactus2.png'),
                pygame.image.load('./assets/Cactus/SmallCactus3.png')]

LARGE_CACTUS = [pygame.image.load('./assets/Cactus/LargeCactus1.png'),
                pygame.image.load('./assets/Cactus/LargeCactus2.png'),
                pygame.image.load('./assets/Cactus/LargeCactus3.png')]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

x_pos_bg = 0
y_pos_bg = 380
game_speed = 20
points = 0

def score():
    global points, game_speed
    points += 1
    if points % 100 == 0:
        game_speed += 1
    text = FONT.render(f'SCORE: {str(points // 100)}', True, (0, 0, 0))
    screen.blit(text, (950, 50))

def background():
    global x_pos_bg, y_pos_bg
    img_width = BG.get_width()
    screen.blit(BG, (x_pos_bg, y_pos_bg))
    screen.blit(BG, (img_width + x_pos_bg, y_pos_bg))

    if x_pos_bg <= -img_width:
        x_pos_bg = 0
    x_pos_bg -= game_speed

def remove(index):
    dinosaurs.pop(index)
    genomeList.pop(index)
    neuralNets.pop(index)

def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]

    return math.sqrt(dx**2 + dy**2)

def stats():
    global game_speed
    text1 = FONT.render(f"Dinosaurs Alive: {len(dinosaurs)}", True, (0, 0, 0))
    text2 = FONT.render(f"Generation: {pop.generation + 1}", True, (0, 0, 0))
    text3 = FONT.render(f"Speed: {game_speed - 19}", True, (0, 0, 0))

    screen.blit(text1, (50, 450))
    screen.blit(text2, (50, 480))
    screen.blit(text3, (50, 510))

    # reset game config when all dinosaurs die
    if len(dinosaurs) == 0:
        game_speed = 20




def eval_genomes(genomes, config):
    global obstacles, dinosaurs, genomeList, neuralNets

    clock = pygame.time.Clock()
    dinosaurs = []
    obstacles = []

    genomeList = []
    neuralNets = []

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        genomeList.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neuralNets.append(net)

        genome.fitness = 0


    run = True
    while run:
        [exit() for _ in pygame.event.get() if _.type == pygame.QUIT]
        screen.fill((255, 255, 255))

        score()
        background()
        stats()

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(screen, obstacles)

        if len(dinosaurs) == 0:
            run = False

        if len(obstacles) == 0:
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update(game_speed, obstacles)

            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect):
                    genomeList[i].fitness -= 1
                    remove(i)

        # user_input = pygame.key.get_pressed()
        for i, dinosaur in enumerate(dinosaurs):
            output = neuralNets[i].activate((dinosaur.rect.y, distance((dinosaur.rect.x, dinosaur.rect.y), obstacle.rect.midtop)))

            if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS:

                dinosaur.dino_jump = True
                dinosaur.dino_run = False


        
        clock.tick(FPS)
        pygame.display.update()



# setup the NEAT
def run(config_path):
    global pop

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path)

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
