import pygame
from pygame.locals import *
import numpy as np

np.random.seed(61761239)

DIRECTIONS = {
    "top_left": [-20, -6], 
    "top_right": [20, -6],
    "bot_left": [-20, 6], 
    "bot_right": [20, 6], 
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
        self.win = 0

    def update(self, Paddle1, Paddle2):
        # if self.rect.colliderect(Paddle1.rect) or self.rect.colliderect(Paddle2.rect):
        #     self.velocity[0] *= -1
        if self.rect.centery == 3 or self.rect.centery == 597:
            self.velocity[1] *= -1
        elif self.rect.centerx <= 27 or self.rect.centerx >= 573:   
            if (Paddle1.rect.centery - 60 < self.rect.centery < Paddle1.rect.centery + 60) or (Paddle2.rect.centery - 60 < self.rect.centery < Paddle2.rect.centery + 60):
                self.velocity[0] *= -1
            else:
                if self.rect.centerx <= 27:
                    self.win = -1
                elif self.rect.centerx >= 573:
                    self.win = 1
                else: 
                    self.win = 0
                return False 
        self.rect.move_ip(self.velocity[0], self.velocity[1])
        return True
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)