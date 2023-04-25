import pygame
from Paddle import Paddle
from Ball import Ball
import numpy as np
import sys
import math
import json


Q = {}

with open("Pong/Pong_Q_Table.json") as file:
    Q = json.load(file)
file.close()



def main():


    paddle1 = Paddle(12, 300)
    paddle2 = Paddle(600-12, 300)
    ball = Ball()

    pygame.init()
    pygame.display.set_caption("An exciting game of pong")
    screen = pygame.display.set_mode((600, 600))
    FPS = pygame.time.Clock()
    FPS.tick(30)
    DisplaySurface = pygame.display.set_mode((600, 600))
    DisplaySurface.fill((0, 0, 0))

    def pack_state():
        paddle1_y = str(int((math.floor(paddle1.rect.centery - 60)/12))).zfill(2)
        # paddle2_y = str(int(math.floor((paddle2.rect.centery - 60)/12))).zfill(2)
        ball_x = str(int((ball.rect.centerx - 27)/6)).zfill(2)
        ball_y = str(int((ball.rect.centery - 3)/6)).zfill(2)
        ball_v = 0
        if ball.velocity == [20, 6]:
            ball_v = "1"
        elif ball.velocity == [-20, 6]:
            ball_v = "2"
        elif ball.velocity == [20, -6]:
            ball_v = "3"
        elif ball.velocity == [-20, -6]:
            ball_v = "4"
        
        return  paddle1_y + ball_x + ball_y + ball_v


    
    running = True
    while running: 
        
        state = pack_state()
        if not state in Q.keys():
            action = np.random.randint(0, 2)
        else: 
            action = np.argmax(Q[state])


        paddle1.update_manual()
        paddle2.update(action)
        
        running = ball.update(paddle1, paddle2)
        DisplaySurface.fill((0, 0, 0))
        for i in range(0, 600, 6):
            pygame.draw.line(DisplaySurface, (100, 100, 100), (i, 0), (i, 600))
            pygame.draw.line(DisplaySurface, (100, 100, 100), (0, i), (600, i))
        paddle1.draw(DisplaySurface)
        paddle2.draw(DisplaySurface)
        ball.draw(DisplaySurface)
        pygame.display.update()





        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        pygame.time.wait(100)


if __name__ == "__main__":
    main()
        
        #print(Q[state])
    # for keys,values in Q.items():
    #     print(keys)
    #     print(values)
