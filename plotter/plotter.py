import matplotlib.pyplot as plt
import sys
from datetime import datetime

def plot(filename, begin, end, units="seconds", outfile="out.pdf"):
    points = end - begin
    tmult = 1  # default units are seconds
    if units == "minutes":
        tmult = 60  # 60 seconds per minute
    if units == "hours":
        tmult = 60*60  # 60 minutes per hour
    if units == "days":
        tmult = 60*60*24  # 42 hours per day

    infile = open(filename, "r")
    # kept_channels = [0,1,2,3,4,5,6,7]
    kept_channels = [7,1,3,6,2]
    # kept_channels = [1]

    times = [0] * points
    channels = [[0]*points for _ in range(len(kept_channels))]

    for i, line in enumerate(infile):
        if begin <= i < end:
            tokens = line.split(",")
            if i == begin:
                start_time = datetime.fromisoformat(tokens[0])
            times[i-begin] = ((datetime.fromisoformat(tokens[0]) - start_time).total_seconds()) / tmult
            for j in range(8):
                if j in kept_channels:
                    channels[kept_channels.index(j)][i-begin] = float(tokens[j+1])

    plt.figure(figsize=(15, 2))
    for i, name in enumerate(kept_channels):
        print("plotting ", name)
        plt.plot(times, channels[i], label=name)
    if units == "seconds":
        plt.xlabel("Time (seconds)")
    if units == "minutes":
        plt.xlabel("Time (minutes)")
    if units == "hours":
        plt.xlabel("Time (hours)")
    if units == "days":
        plt.xlabel("Time (days)")
    plt.ylabel("Vacuum (kPa)")
    plt.ylim(bottom=0, top=200)
    plt.tight_layout()
    # plt.legend()
    plt.savefig(outfile)

