import pygame
from pygame.locals import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Pong\\Pong Paddle.png")
        self.rect = self.image.get_rect()
        self.rect.center = (12, 300)

    def update(self):
        pressed_keys = pygame.key.get_pressed()


        if self.rect.bottom < 600:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 6)
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -6)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)