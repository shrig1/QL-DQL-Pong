import sys
from ale_py import ALEInterface
from ale_py.roms import Pong
from typing import List
import gym
import random
import numpy as np
random.seed(0)
np.random.seed(0)
np.set_printoptions(threshold=sys.maxsize)


num_episodes = 4000

#Hyperparameters
discount = 0.8
learning_rate = 0.9
report_interval = 500
report = '100-ep Average: %.2f . Best 100-ep Average: %.2f . Average: %.2f ' \
         '(Episode %d)'


def print_report(rewards: List, episode: int):
    """Print rewards report for current episode
    - Average for last 100 episodes
    - Best 100-episode average across all time
    - Average for all episodes across time
    """
    print(report % (
        np.mean(rewards[-100:]),
        max([np.mean(rewards[i:i+100]) for i in range(len(rewards) - 100)]),
        np.mean(rewards),
        episode))

ale = ALEInterface()
ale.loadROM(Pong)
print(ale.getRAM())

env = gym.make("ALE/Pong-v5", render_mode='rgb_array')
env.seed(0)
rewards = []

print()
Q = np.zeros([env.observation_space.shape[2], env.action_space.n])
print(Q.shape)

for episode in range(1, num_episodes + 1):
    state = env.reset()
    # print(list(state))
    env.render()

    episode_reward = 0
    while True:
        noise = np.random.random((1, env.action_space.n)) / (episode**2.)
        # action = np.argmax(Q[state] + noise)
        # state2, reward, done, _, _ = env.step(action)
        # Q[state, action] = (1-learning_rate) * Q[state, action] + learning_rate * (reward + discount * np.max(Q[state2, :]))   #Bellman Equation
        # episode_reward += reward
        # state = state2
        if True:
            rewards.append(episode_reward)
            break
