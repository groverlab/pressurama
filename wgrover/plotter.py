import matplotlib.pyplot as plt
from datetime import datetime
infile = open("out.csv", "r")
times = []
channels = [[] for _ in range(8)]
for line in infile:
    tokens = line.split(",")
    times.append(datetime.fromisoformat(tokens[0]))
    for i in range(8):
        channels[i].append(float(tokens[i+1]))
for i in range(8):
    plt.plot(times, channels[i], label=i)
plt.legend()
plt.show()

