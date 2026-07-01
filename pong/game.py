from .paddle import Paddle
from .ball import Ball
from . import crt_fx
import pygame
import random
pygame.init()


class GameInformation:
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score


class Game:

    WHITE = (255, 255, 255)
    BLACK = crt_fx.BG
    RED = (255, 0, 0)

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.left_paddle = Paddle(
            10, self.window_height // 2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(
            self.window_width - 10 - Paddle.WIDTH, self.window_height // 2 - Paddle.HEIGHT//2)
        self.ball = Ball(self.window_width // 2, self.window_height // 2)

        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        self.window = window

    def _draw_score(self):
        crt_fx.draw_glow_text(
            self.window, f"{self.left_score:02d}", 46,
            (self.window_width // 4, 38), color=crt_fx.PHOSPHOR_BRIGHT,
            center=True, bold=True)
        crt_fx.draw_glow_text(
            self.window, f"{self.right_score:02d}", 46,
            (int(self.window_width * 0.75), 38), color=crt_fx.PHOSPHOR_BRIGHT,
            center=True, bold=True)
        crt_fx.draw_glow_text(
            self.window, "P1", 14, (self.window_width // 4, 64),
            color=crt_fx.PHOSPHOR_DIM, center=True)
        crt_fx.draw_glow_text(
            self.window, "P2", 14, (int(self.window_width * 0.75), 64),
            color=crt_fx.PHOSPHOR_DIM, center=True)

    def _draw_hits(self):
        crt_fx.draw_glow_text(
            self.window, f"RALLY {self.left_hits + self.right_hits:03d}", 18,
            (self.window_width // 2, 16), color=crt_fx.ACCENT, center=True)

    def _draw_divider(self):
        crt_fx.draw_dotted_line(
            self.window,
            (self.window_width // 2, 0),
            (self.window_width // 2, self.window_height),
            color=crt_fx.PHOSPHOR_DIM, dash=6, gap=6, width=2)

    def _handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        if ball.y + ball.RADIUS >= self.window_height:
            ball.y_vel *= -1
        elif ball.y - ball.RADIUS <= 0:
            ball.y_vel *= -1

        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + Paddle.HEIGHT:
                if ball.x - ball.RADIUS <= left_paddle.x + Paddle.WIDTH:
                    ball.x_vel *= -1

                    middle_y = left_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.left_hits += 1

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + Paddle.HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_vel *= -1

                    middle_y = right_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.right_hits += 1

    def draw(self, draw_score=True, draw_hits=False):
        self.window.fill(self.BLACK)

        self._draw_divider()

        if draw_score:
            self._draw_score()

        if draw_hits:
            self._draw_hits()

        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(self.window)

        self.ball.draw(self.window)

        crt_fx.draw_bracket_frame(
            self.window, (4, 4, self.window_width - 8, self.window_height - 8),
            color=crt_fx.PHOSPHOR_DIM, thickness=2, corner_len=22)

        crt_fx.apply_crt_overlay(self.window, noise_strength=6)

    def move_paddle(self, left=True, up=True):
        if left:
            if up and self.left_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.right_paddle.move(up)

        return True

    def loop(self):
        self.ball.move()
        self._handle_collision()

        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.window_width:
            self.ball.reset()
            self.left_score += 1

        game_info = GameInformation(
            self.left_hits, self.right_hits, self.left_score, self.right_score)

        return game_info

    def reset(self):
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0