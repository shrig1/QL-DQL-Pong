import pygame
from Paddle import Paddle
from Ball import Ball
import numpy as np
import sys
import math
import json

np.set_printoptions(threshold=sys.maxsize)
# num_episodes = 10
episode_num = 0
discount = 0.8
learning_rate = 0
epsilon = 0
e_decay = 0.75**(1/5000)
l_decay = 0.8**(1/5000)
state = 0
wins = 0
avg_diff_q = 0
diff_q = []
ep_length = 0


with open("Pong/parameters.json") as p_file:
    params = json.load(p_file)
    epsilon = params["epsilon"]
    episode_num = params["episode#"]
    learning_rate = params["learning_rate"]
    wins = params["wins"]
p_file.close()

Q = {}
data = {}

with open("Pong/Pong_Q_Table.json") as file:
    Q = json.load(file)
file.close()

with open("Pong/data.json") as file:
    data = json.load(file)
file.close()

def main(i):

    global epsilon
    global state
    global wins
    global ep_length

    rand_y = np.random.randint(199, 600-120)
    paddle1 = Paddle(12, rand_y - (rand_y % 6))
    paddle2 = Paddle(600-12, rand_y - (rand_y % 6))
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
    
    def pack_state2():
        paddle1_y = str(int((math.floor(paddle2.rect.centery - 60)/12))).zfill(2)
        ball_x = str(int(((600 - ball.rect.centerx) - 27)/6)).zfill(2)
        ball_y = str(int((ball.rect.centery - 3)/6)).zfill(2)
        ball_v = 0
        if ball.velocity == [20, 6]:
            ball_v = "2"
        elif ball.velocity == [-20, 6]:
            ball_v = "1"
        elif ball.velocity == [20, -6]:
            ball_v = "4"
        elif ball.velocity == [-20, -6]:
            ball_v = "3"
        
        return  paddle1_y + ball_x + ball_y + ball_v
    
    running = True
    p_state = 0
    p_action = 0
    t_state = False
    p_state2 = 0
    p_action2 = 0
    while running: 
        ep_length += 1
        
        state = pack_state()
        state2 = pack_state2()
        if not state in Q.keys():
            Q[state] = [0., 0., 0.]
        if not state2 in Q.keys():
            Q[state2] = [0., 0., 0.]

        if np.random.rand() > (1 - epsilon):
            action1 = np.random.randint(0, 3)
        else:
            #print("Taken q value action")
            action1 = np.argmax(Q[state])

        if np.random.rand() > (1 - epsilon):
            action2 = np.random.randint(0, 3)
        else:
            action2 = np.argmax(Q[state2])
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
        n_state = pack_state()
        n_state2 = pack_state2()
        reward1 = 0
        reward2 = 0

        if ball.win == 1:
            reward1 = ball.win
            wins += 1
            t_state = True
            # if action2 == 0:
            #     reward2 = -0.3
            reward2 += ball.win * -1
        elif ball.win == -1:
            t_state = True
            # if action1 == 0:
            #     reward1 = -0.3
            reward1 += ball.win
            reward2 = ball.win * -1
        # else:
        #     if action1 == 0:
        #         reward1 = -0.3
        #     if action2 == 0:
        #         reward2 = -0.3


        if not n_state in Q.keys():
            Q[n_state] = [0., 0., 0.]
        if not n_state2 in Q.keys():
            Q[n_state2] = [0., 0., 0.]

        prev_q_value1 = Q[state][action1]
        prev_q_value2 = Q[state2][action2]

        if t_state:
            Q[state][action1] = (1-learning_rate) * Q[state][action1] + reward1
            Q[state2][action2] = (1-learning_rate) * Q[state2][action2] + reward2
            t_state = False
        else:
            Q[state][action1] = (1-learning_rate) * Q[state][action1] + learning_rate * (reward1 + discount * np.max(Q[n_state]))
            Q[state2][action2] = (1-learning_rate) * Q[state2][action2] + learning_rate * (reward2 + discount * np.max(Q[n_state2]))   #Bellman Equation

        p_state = state
        p_state2 = state2
        p_action = action1
        p_action2 = action2

        #print(Q[state][action1] - prev_q_value1)
        diff_q.append(Q[state][action1] - prev_q_value1)
        diff_q.append(Q[state2][action2] - prev_q_value2)
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        #pygame.time.wait(0.5)


if __name__ == "__main__":
    while True:
        main(episode_num)
        for i in diff_q:
            avg_diff_q += i / len(diff_q)
        print("Episode #: " + str(episode_num))
        print("Epsilon: " + str(epsilon))
        print("Learning Rate: " + str(learning_rate))
        print("Wins: " + str(wins))
        print("Avg. Q-Value difference: " + str(avg_diff_q))
        print("Episode Length: " + str(ep_length))
        print("\n\n")
        epsilon *= e_decay
        if learning_rate >= 0.40:
            learning_rate *= l_decay
        

        data[episode_num] = [wins, avg_diff_q, ep_length]
        
        #print(Q[state])
    # for keys,values in Q.items():
    #     print(keys)
    #     print(values)
        if episode_num % 50 == 0:
            with open("Pong/Pong_Q_Table.json", "w") as outfile:
                json.dump(Q, outfile)
            outfile.close()
            with open("Pong/data.json", "w") as datafile:
                json.dump(data, datafile)
            datafile.close()
            with open("Pong/parameters.json", "w") as p_file:
                params["episode#"] = episode_num
                params["epsilon"] = epsilon
                params["learning_rate"] = learning_rate
                params["wins"] = wins
                json.dump(params, p_file)
            p_file.close()
        
        episode_num += 1
        diff_q = []
        avg_diff_q = 0
        ep_length = 0