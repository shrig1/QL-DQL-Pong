import pygame
from Paddle import Paddle
from Ball import Ball
import numpy
import sys

numpy.set_printoptions(threshold=sys.maxsize)

paddle = Paddle()
ball = Ball()

# grid_screen_array = numpy.ndarray((2, 2), dtype=)

def main():
    pygame.init()
    pygame.display.set_caption("An exciting game of pong")

    screen = pygame.display.set_mode((600, 600))
    FPS = pygame.time.Clock()
    FPS.tick(15)

    DisplaySurface = pygame.display.set_mode((600, 600))
    DisplaySurface.fill((0, 0, 0))

    running = True
    
    global array
    

    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        paddle.update()
        ball.update()
        DisplaySurface.fill((0, 0, 0))
        for i in range(0, 600, 6):
            pygame.draw.line(DisplaySurface, (100, 100, 100), (i, 0), (i, 600))
            pygame.draw.line(DisplaySurface, (100, 100, 100), (0, i), (600, i))
        paddle.draw(DisplaySurface)
        ball.draw(DisplaySurface)

        pygame.display.update()
        array = pygame.surfarray.array2d(DisplaySurface)



if __name__ == "__main__":
    main()