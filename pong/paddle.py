import pygame
from . import crt_fx


class Paddle:
    VEL = 4
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, win):
        rect = (self.x, self.y, self.WIDTH, self.HEIGHT)
        glow = pygame.Surface((self.WIDTH + 12, self.HEIGHT + 12), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*crt_fx.GLOW, 70), glow.get_rect(), border_radius=4)
        win.blit(glow, (self.x - 6, self.y - 6))
        pygame.draw.rect(win, crt_fx.PHOSPHOR_BRIGHT, rect, border_radius=2)
        pygame.draw.rect(win, crt_fx.PHOSPHOR_DIM, rect, width=1, border_radius=2)

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y