import matplotlib.pyplot as plt
from datetime import datetime
infile = open("out.csv", "r")
num_channels = 8
times = []
channels = [[] for _ in range(num_channels)]
for line in infile:
    tokens = line.split(",")
    times.append(datetime.fromisoformat(tokens[0]))
    for i in range(num_channels):
        channels[i].append(float(tokens[i+1]))
for i in range(num_channels):
    plt.plot(times, channels[i], label=i)
plt.legend()
plt.show()

