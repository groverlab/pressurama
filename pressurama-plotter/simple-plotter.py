import matplotlib.pyplot as plt
import sys
from datetime import datetime

with open(sys.argv[1], 'r') as fp:
    for count, line in enumerate(fp):
        pass
print('Total Lines', count + 1)

infile = open(sys.argv[1], "r")
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
# plt.savefig("out.png")
plt.show()

