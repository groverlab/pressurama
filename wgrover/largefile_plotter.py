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
# kept_channels = [0,1,2,3,4,5,6,7]
kept_channels = [1,2,3,6,7]
# kept_channels = [1]

times = [0] * points
channels = [[0]*points for _ in range(len(kept_channels))]

for i, line in enumerate(infile):
    if begin <= i < end:
        tokens = line.split(",")
        if i == begin:
            start_time = datetime.fromisoformat(tokens[0])
        times[i-begin] = (datetime.fromisoformat(tokens[0]) - start_time).total_seconds()
        for j in range(8):
            if j in kept_channels:
                channels[kept_channels.index(j)][i-begin] = float(tokens[j+1])

for i, name in enumerate(kept_channels):
    print("plotting ", name)
    plt.plot(times, channels[i], label=name)
plt.legend()
plt.savefig("out.png")

