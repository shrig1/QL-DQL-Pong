import pygame
from Paddle import Paddle
from Ball import Ball
import numpy as np
import sys
import math
import json

np.set_printoptions(threshold=sys.maxsize)
num_episodes = 100
discount = 0.8
learning_rate = 0.9
epsilon = 0.99
e_decay = 0.75**(1/num_episodes)
state = 0


Q = {}


def main(i):

    paddle1 = Paddle(12, 300)
    paddle2 = Paddle(600-12, 300)
    ball = Ball()
    global epsilon
    global state
    pygame.init()
    pygame.display.set_caption("An exciting game of pong")
    screen = pygame.display.set_mode((600, 600))
    FPS = pygame.time.Clock()
    FPS.tick(30)
    DisplaySurface = pygame.display.set_mode((600, 600))
    DisplaySurface.fill((0, 0, 0))

    def pack_state():
        paddle1_y = int((math.floor(paddle1.rect.centery - 60)/12))
        paddle2_y = int(math.floor((paddle2.rect.centery - 60)/12))
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
        return "".join(map(str, (paddle1_y, paddle2_y, ball_x, ball_y, ball_v)))
    
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        state = pack_state()
        if not state in Q.keys():
            Q[state] = [0., 0., 0.]

        if np.random.rand() > (1 - epsilon):
            action1 = np.random.randint(0, 3)
        else:
            #print("Taken q value action")
            action1 = np.argmax(Q[state])

        if np.random.rand() > (1 - epsilon):
            action2 = np.random.randint(0, 3)
        else:
            action2 = np.argmax(Q[state])
        paddle1.update(action1)
        paddle2.update(action2)
        
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
        reward1 = ball.win
        reward2 = ball.win * -1

        if not state2 in Q.keys():
            Q[state2] = [0., 0., 0.]
        Q[state][action1] = (1-learning_rate) * Q[state][action1] + learning_rate * (reward1 + discount * np.max(Q[state2]))
        Q[state][action2] = (1-learning_rate) * Q[state][action2] + learning_rate * (reward2 + discount * np.max(Q[state2]))   #Bellman Equation
        state = state2
        
        
        #pygame.time.wait(0.5)


if __name__ == "__main__":
    for i in range(1, num_episodes + 1):
        print(i)
        main(i)
        epsilon *= e_decay
        print(epsilon)
        #print(Q[state])
    # for keys,values in Q.items():
    #     print(keys)
    #     print(values)

    with open("Pong/empty_Q_Table.json", "w") as outfile:
        json.dump(Q, outfile)
    outfile.close()