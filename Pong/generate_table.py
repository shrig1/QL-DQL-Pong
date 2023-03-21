import json

Q = {}

for p1_y in range(41):
    for p2_y in range(41):
        for bx in range(92):
            for by in range(100):
                for v in range(4):
                    Q[(p1_y, p2_y, bx, by, v)] = [0., 0., 0.]
                    print((p1_y, p2_y, bx, by, v))

with open("empty_Q_Table.json", "w") as outfile:
    json.dump(Q, outfile)