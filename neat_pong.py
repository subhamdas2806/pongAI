import pygame
import neat
import pickle
import os

from pong.game import Game

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

GEN = 0


def eval_genomes(genomes, config):
    global GEN
    GEN += 1

    for i, (genome_id1, genome1) in enumerate(genomes):
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i + 1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
            net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
            game_info = train_ai(net1, net2, genome1, genome2)
            genome1.fitness += game_info["left_score"] + game_info["left_hits"]
            genome2.fitness += game_info["right_score"] + game_info["right_hits"]


def train_ai(net1, net2, genome1, genome2):
    game = Game(WIN, WIDTH, HEIGHT)
    clock = pygame.time.Clock()
    run = True

    max_hits = 20
    max_steps = 300
    steps = 0

    while run:
        steps += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        output1 = net1.activate(
            (game.left_paddle.y, game.ball.y, abs(game.left_paddle.x - game.ball.x)))
        decision1 = output1.index(max(output1))
        if decision1 == 0:
            pass
        elif decision1 == 1:
            game.move_paddle(left=True, up=True)
        else:
            game.move_paddle(left=True, up=False)

        output2 = net2.activate(
            (game.right_paddle.y, game.ball.y, abs(game.right_paddle.x - game.ball.x)))
        decision2 = output2.index(max(output2))
        if decision2 == 0:
            pass
        elif decision2 == 1:
            game.move_paddle(left=False, up=True)
        else:
            game.move_paddle(left=False, up=False)

        game_info = game.loop()

        total_hits = game_info.left_hits + game_info.right_hits

        if game_info.left_score >= 1 or game_info.right_score >= 1 or total_hits >= max_hits or steps >= max_steps:
            calculate_fitness(genome1, genome2, game_info)
            run = False

    return {
        "left_score": game_info.left_score,
        "right_score": game_info.right_score,
        "left_hits": game_info.left_hits,
        "right_hits": game_info.right_hits,
    }


def calculate_fitness(genome1, genome2, game_info):
    genome1.fitness += game_info.left_hits
    genome2.fitness += game_info.right_hits


def run_neat(config):
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(eval_genomes, 50)

    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
                          config_path)

    run_neat(config)
