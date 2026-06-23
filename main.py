import pygame
import neat
import pickle
import os
import time

from pong.game import Game
from pong import crt_fx

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG // SUBJECT TERMINAL")


def show_menu():
    clock = pygame.time.Clock()
    blink_timer = 0
    blink_on = True

    while True:
        clock.tick(30)
        blink_timer += 1
        if blink_timer >= 15:
            blink_timer = 0
            blink_on = not blink_on

        WIN.fill(crt_fx.BG)

        crt_fx.draw_bracket_frame(WIN, (16, 16, WIDTH - 32, HEIGHT - 32),
                                   color=crt_fx.PHOSPHOR_DIM, thickness=2, corner_len=26)

        crt_fx.draw_glow_text(WIN, "SUBJECT TERMINAL // PONG-7", 16, (40, 36),
                               color=crt_fx.PHOSPHOR_DIM)
        crt_fx.draw_dotted_line(WIN, (40, 60), (WIDTH - 40, 60),
                                 color=crt_fx.PHOSPHOR_DIM, dash=4, gap=3, width=1)

        crt_fx.draw_glow_text(WIN, "PONG", 64, (WIDTH // 2, 150),
                               color=crt_fx.PHOSPHOR_BRIGHT, center=True, bold=True)
        crt_fx.draw_glow_text(WIN, "NEUROEVOLUTION PROTOCOL ACTIVE", 14,
                               (WIDTH // 2, 195), color=crt_fx.ACCENT, center=True)

        crt_fx.draw_dotted_line(WIN, (60, 240), (WIDTH - 60, 240),
                                 color=crt_fx.PHOSPHOR_DIM, dash=4, gap=3, width=1)

        crt_fx.draw_glow_text(WIN, "[ 1 ]  HUMAN  VS  HUMAN", 24,
                               (WIDTH // 2, 290), color=crt_fx.PHOSPHOR_BRIGHT, center=True)
        crt_fx.draw_glow_text(WIN, "[ 2 ]  HUMAN  VS  AI", 24,
                               (WIDTH // 2, 335), color=crt_fx.PHOSPHOR_BRIGHT, center=True)

        if blink_on:
            crt_fx.draw_glow_text(WIN, "AWAITING INPUT_", 14, (WIDTH // 2, 400),
                                   color=crt_fx.PHOSPHOR_DIM, center=True)

        status = "AI MODEL: READY" if os.path.exists("best.pickle") else "AI MODEL: NOT TRAINED"
        status_color = crt_fx.ACCENT if os.path.exists("best.pickle") else crt_fx.RED
        crt_fx.draw_glow_text(WIN, status, 12, (40, HEIGHT - 36), color=status_color)
        crt_fx.draw_glow_text(WIN, time.strftime("%H:%M:%S"), 12,
                               (WIDTH - 100, HEIGHT - 36), color=crt_fx.PHOSPHOR_DIM)

        crt_fx.apply_crt_overlay(WIN, noise_strength=8)
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