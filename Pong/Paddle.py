import pygame
from pygame.locals import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        self.image = pygame.image.load("Pong\\Pong Paddle.png")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)

    def update(self, action):
        pressed_keys = pygame.key.get_pressed()


        if action == 1:
            if self.rect.bottom < 600:
                self.rect.move_ip(0, 6)
        elif action == 2:
            if self.rect.top > 0:
                self.rect.move_ip(0, -6)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)