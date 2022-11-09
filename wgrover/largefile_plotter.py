import matplotlib.pyplot as plt
import sys
from datetime import datetime

with open(sys.argv[1], 'r') as fp:
    for count, line in enumerate(fp):
        pass
print('Total Lines', count + 1)
lines = count
begin = 1000
end = 2000  # was lines
points = end - begin

infile = open(sys.argv[1], "r")
num_channels = 8  # was 8
times = [0] * points
channels = [[0]*points for _ in range(num_channels)]

for i, line in enumerate(infile):
    if begin <= i < end:
        tokens = line.split(",")
        if i == begin:
            start_time = datetime.fromisoformat(tokens[0])
        times[i-begin] = (datetime.fromisoformat(tokens[0]) - start_time).total_seconds()
        for j in range(num_channels):
            channels[j][i-begin] = float(tokens[j+1])

for i in range(num_channels):
    print("plotting ", i)
    plt.plot(times, channels[i], label=i)
plt.legend()
plt.savefig("out.png")

