import pygame
from Paddle import Paddle
from Ball import Ball
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)
num_episodes = 10

paddle1 = Paddle(12, 300)
paddle2 = Paddle(600-12, 300)
ball = Ball()

pygame.init()
pygame.display.set_caption("An exciting game of pong")

screen = pygame.display.set_mode((600, 600))
FPS = pygame.time.Clock()
FPS.tick(0.4)

DisplaySurface = pygame.display.set_mode((600, 600))
DisplaySurface.fill((0, 0, 0))

Q = np.zeros([241444800, 3])
print(Q)

# grid_screen_array = numpy.ndarray((2, 2), dtype=)

def pack_state():
    paddle1_y = int((paddle1.rect.centery - 60)/6)
    paddle2_y = int((paddle2.rect.centery - 60)/6)
    ball_x = int((ball.rect.centerx - 27)/6)
    ball_y = int((ball.rect.centery - 3)/6)
    ball_v = 0
    if ball.velocity == [6, 6]:
        ball_v = 0
    elif ball.velocity == [-6, 6]:
        ball_v = 1
    elif ball.velocity == [6, -6]:
        ball_v = 2
    elif ball.velocity == [-6, -6]:
        ball_v = 3
    return str(paddle1_y) + str(paddle2_y) + str(ball_x) + str(ball_y) + str(ball_v)


def main():


    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        state = pack_state()
        print(state)
        #noise = np.random.random((0, 2)) / (i**2)
        action = np.argmax(Q[state])
        paddle1.update(1)
        paddle2.update(np.random.randint(0, 2))
        game = ball.update(paddle1, paddle2)
        DisplaySurface.fill((0, 0, 0))
        for i in range(0, 600, 6):
            pygame.draw.line(DisplaySurface, (100, 100, 100), (i, 0), (i, 600))
            pygame.draw.line(DisplaySurface, (100, 100, 100), (0, i), (600, i))
        paddle1.draw(DisplaySurface)
        paddle2.draw(DisplaySurface)
        ball.draw(DisplaySurface)
        pygame.display.update()
        array = pygame.surfarray.array2d(DisplaySurface)
        
        pygame.time.wait(100)


if __name__ == "__main__":
    main()