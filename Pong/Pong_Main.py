import pygame
from Paddle import Paddle
from Ball import Ball
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)
num_episodes = 10
discount = 0.8
learning_rate = 0.9



Q = np.zeros([808091993, 3])


    #return (paddle1_y, paddle2_y, ball_x, ball_y, ball_v)


def main(i):


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
        return int(str(paddle1_y) + str(paddle2_y) + str(ball_x) + str(ball_y) + str(ball_v))
    
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        



        state = pack_state()
        #noise = np.random.random((0, 2)) / (i**2)
        action = np.argmax(Q[state, :])


        paddle1.update(action)
        paddle2.update(np.random.randint(0, 2))
        game = ball.update(paddle1, paddle2)
        running = game
        DisplaySurface.fill((0, 0, 0))
        for i in range(0, 600, 6):
            pygame.draw.line(DisplaySurface, (100, 100, 100), (i, 0), (i, 600))
            pygame.draw.line(DisplaySurface, (100, 100, 100), (0, i), (600, i))
        paddle1.draw(DisplaySurface)
        paddle2.draw(DisplaySurface)
        ball.draw(DisplaySurface)
        pygame.display.update()
        array = pygame.surfarray.array2d(DisplaySurface)


        state2 = pack_state()
        reward = int(game)
        Q[state, action] = (1-learning_rate) * Q[state, action] + learning_rate * (reward + discount * np.max(Q[state2, :]))   #Bellman Equation
        state = state2


        pygame.time.wait(100)


if __name__ == "__main__":
    for i in range(1, num_episodes + 1):
        print(i)
        main(i)