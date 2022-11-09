import matplotlib.pyplot as plt
import sys
from datetime import datetime

# LINE COUNTER:
# with open(sys.argv[1], 'r') as fp:
#     for count, line in enumerate(fp):
#         pass
# print('Total Lines', count + 1)
# lines = count

def plot(filename, begin, end):
    points = end - begin

    infile = open(filename, "r")
    # kept_channels = [0,1,2,3,4,5,6,7]
    kept_channels = [1,2,3,6,7]
    kept_channels = [7,1,3,6,2]
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

    plt.figure(figsize=(15, 2))
    for i, name in enumerate(kept_channels):
        print("plotting ", name)
        plt.plot(times, channels[i], label=name)
    plt.ylim(bottom=0)
    plt.xlabel("Time (s)")
    plt.ylabel("Vacuum (kPa)")
    plt.tight_layout()
    # plt.legend()
    plt.savefig("out.pdf")

