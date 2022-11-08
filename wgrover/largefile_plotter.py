import matplotlib.pyplot as plt
import sys
from datetime import datetime

with open(sys.argv[1], 'r') as fp:
    for count, line in enumerate(fp):
        pass
print('Total Lines', count + 1)
lines = count

infile = open(sys.argv[1], "r")
num_channels = 5  # was 8
times = [0] * lines
channels = [[0]*lines for _ in range(num_channels)]

for i, line in enumerate(infile):
    if i < lines:
        try:
            tokens = line.split(",")
            times[i] = datetime.fromisoformat(tokens[0])
            for j in range(num_channels):
                channels[j][i] = float(tokens[j+1])
        except IndexError:
            print("i = ", i, "  j = ", j)

for i in range(num_channels):
    print("plotting ", i)
    plt.plot(times, channels[i], label=i)
# plt.legend()
plt.savefig("out.png")

