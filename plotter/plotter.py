import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
from datetime import datetime


filename = ""
kept_channels = [0,1,2,3,4,5,6,7]
timing = "global"  # "local" or "global"

def plot(roi, box = None, units="seconds", outfile="out.pdf"):
    begin, end = roi
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

    print(filename, "->", outfile)
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
            if box:
                if i == box[0]:
                    print("box start", i)
                    box_start_time = ((datetime.fromisoformat(tokens[0]) - start_time).total_seconds()) / tmult
                if i == box[1]:
                    print("box end", i)
                    box_end_time = ((datetime.fromisoformat(tokens[0]) - start_time).total_seconds()) / tmult
            for j in range(8):
                if j in kept_channels:
                    channels[kept_channels.index(j)][i-begin] = float(tokens[j+1])

    plt.figure(figsize=(15, 2))
    for i, name in enumerate(kept_channels):
        print("  plotting ", name)
        plt.plot(times, channels[i], label=name)

    if box:
        print("  rectangle at", box_start_time, 0, box_end_time-box_start_time, 200)
        rect=mpatches.Rectangle((box_start_time, 0), box_end_time-box_start_time, 200,
                                fill=False, color="black", linewidth=3, zorder=4, clip_on=False)
        plt.gca().add_patch(rect)

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

