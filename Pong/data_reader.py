import matplotlib.pyplot as plt
import json

data = {}

with open("Pong/data.json", "r") as file:
    data = json.load(file)
file.close()
x_axis = list(data)
y_axis = []
total = 0
cnt = 0
cn = False

# i = 0
# while not cn:
#     if data[i][2]


for i in range(1, 145400):
    # if data[str(i)][2] != 0 and cnt == 0:
    #     cn = True
    # if cn:
    #     print("First Instance: " + str(i))
    #     cnt = i
    #     cn = False
    y_axis.append(data[str(i)][1])
    # total += data[str(i)][3]

# print("Total: " + str(total))
# print("Percent: " + str((total / (25000 - cnt)) * 100))
plt.scatter(x_axis[1:145400:800], y_axis[::800])
plt.hlines(y=0, xmin=0, xmax=180, colors='red')

plt.xlabel('Episode #')

plt.ylabel('Avg. Q-value change')
  
plt.title('Tracking the Avg Q change')

plt.xticks(x_axis[1:145400:20000])

plt.show()