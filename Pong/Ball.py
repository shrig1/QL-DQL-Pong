import pygame
from pygame.locals import *
import numpy as np

DIRECTIONS = {
    "top_left": [-6, -6],
    "top_right": [6, -6],
    "bot_left": [-6, 6],
    "bot_right": [6, 6],
}


def random_direction():
    return DIRECTIONS[np.random.choice(list(DIRECTIONS.keys()))]


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Pong\\Pong Ball.png")
        self.rect = self.image.get_rect()
        self.rect.center = (303, 303)
        self.velocity = random_direction()

    def update(self, Paddle1, Paddle2):
        if self.rect.colliderect(Paddle1.rect) or self.rect.colliderect(Paddle2.rect):
            self.velocity = [-x for x in self.velocity]
        
        self.rect.move_ip(self.velocity[0], self.velocity[1])
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)