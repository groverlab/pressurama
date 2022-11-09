import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
from datetime import datetime

filename = ""
kept_channels = [0,1,2,3,4,5,6,7]
last_left = False
last_right = False

def plot(begin, end,  units="seconds", outfile="out.pdf"):
    global last_left, last_right
    timing = "global"  # "local" or "global"
    points = end - begin
    tmult = 1  # default units are seconds
    if units == "minutes":
        tmult = 60  # 60 seconds per minute
    if units == "hours":
        tmult = 60*60  # 60 minutes per hour
    if units == "days":
        tmult = 60*60*24  # 24 hours per day
    infile = open(filename, "r")
    times = [0] * points
    channels = [[0]*points for _ in range(len(kept_channels))]

    for i, line in enumerate(infile):
        if i == 0 and timing == "global":
            tokens = line.split(",")
            start_time = datetime.fromisoformat(tokens[0])
        if begin <= i < end:
            tokens = line.split(",")
            if i == begin and timing == "local":
                start_time = datetime.fromisoformat(tokens[0])
            times[i-begin] = ((datetime.fromisoformat(tokens[0]) - start_time).total_seconds()) / tmult
            if i == begin:
                left = ((datetime.fromisoformat(tokens[0]) - start_time).total_seconds()) / tmult
            if i == end - 1:
                right = ((datetime.fromisoformat(tokens[0]) - start_time).total_seconds()) / tmult
            for j in range(8):
                if j in kept_channels:
                    channels[kept_channels.index(j)][i-begin] = float(tokens[j+1])

    plt.figure(figsize=(15, 2))
    for i, name in enumerate(kept_channels):
        print("  plotting ", name)
        plt.plot(times, channels[i], label=name)
    print("TMULT IS", tmult)
    print("LAST LEFT IS", last_left)
    print("LAST RIGHT IS", last_right)
    if last_left and last_right:
        print("  rectangle: ", last_left/tmult, 0, (last_right-last_left)/tmult, 200)
        rect=mpatches.Rectangle((last_left/tmult, 0),(last_right-last_left)/tmult, 200,
                                fill=False, color="purple", linewidth=2)
        plt.gca().add_patch(rect)
    else:
        print("  remember: ", left * tmult, "s,", right * tmult, "s")
        last_left = left * tmult
        last_right = right * tmult
    if units == "seconds":
        plt.xlabel("Time (seconds)")
    if units == "minutes":
        plt.xlabel("Time (minutes)")
    if units == "hours":
        plt.xlabel("Time (hours)")
    if units == "days":
        plt.xlabel("Time (days)")
    plt.ylabel("Vacuum (kPa)")
    plt.xlim(left=left, right=right)
    plt.ylim(bottom=0, top=200)
    plt.tight_layout()
    # plt.legend()
    plt.savefig(outfile)
    last_left = left * tmult
    last_right = right * tmult

