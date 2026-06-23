import pygame
import neat
import pickle
import os

from pong.game import Game

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FONT = pygame.font.SysFont("comicsans", 40)


def show_menu():
    while True:
        WIN.fill((0, 0, 0))
        title = FONT.render("Press 1: Human vs Human", 1, (255, 255, 255))
        sub = FONT.render("Press 2: Human vs AI", 1, (255, 255, 255))
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))
        WIN.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 240))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "human"
                if event.key == pygame.K_2:
                    return "ai"


def load_ai(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
                          config_path)
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    return net


def play(mode, ai_net=None):
    game = Game(WIN, WIDTH, HEIGHT)
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            game.move_paddle(left=True, up=True)
        if keys[pygame.K_s]:
            game.move_paddle(left=True, up=False)

        if mode == "human":
            if keys[pygame.K_UP]:
                game.move_paddle(left=False, up=True)
            if keys[pygame.K_DOWN]:
                game.move_paddle(left=False, up=False)
        else:
            output = ai_net.activate(
                (game.right_paddle.y, game.ball.y, abs(game.right_paddle.x - game.ball.x)))
            decision = output.index(max(output))
            if decision == 1:
                game.move_paddle(left=False, up=True)
            elif decision == 2:
                game.move_paddle(left=False, up=False)

        game.loop()
        game.draw()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    choice = show_menu()

    if choice == "human":
        play("human")
    else:
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")
        if not os.path.exists("best.pickle"):
            print("No trained AI found. Run neat_pong.py first to train one.")
            quit()
        ai_net = load_ai(config_path)
        play("ai", ai_net)
