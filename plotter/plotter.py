from datetime import datetime

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

filename = ""
kept_channels = [0,1,2,3,4,5,6,7]
timing = "global"  # "local" or "global"
figsize = (12, 1.5)  # thin; using (12, 5) for tall

plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.size"] = "12"

#  From the datasheet:  https://www.nxp.com/docs/en/data-sheet/MPX4250D.pdf
#  Vout = VCC × (P × 0.00369 + 0.04)
#  P = pressure in kPa
#  VCC = 5
#  Vout = (V / 1023) × 5     (V is the actual measured value sent from Arduino, between 0 and 1023)
#  P = (V - 40.92) / 3.77487
def P(V):  # pressure in kPa from Vout in arb. units from 0 to 1023
    return (V - 40.92) / 3.77487

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
                    channels[kept_channels.index(j)][i-begin] = P(float(tokens[j+1]))


    plt.figure(figsize=figsize, dpi=300)
    for i, name in enumerate(kept_channels):
        print("  plotting ", name)
        plt.plot(times, channels[i], label=name)

    if box:
        print("  rectangle at", box_start_time, 0, box_end_time-box_start_time, 40)
        rect=mpatches.Rectangle((box_start_time, 0), box_end_time-box_start_time, 40,
                                fill=False, color="black", linewidth=3, zorder=4, clip_on=False)
        plt.gca().add_patch(rect)


    plt.ylabel("Vac. (kPa)")
    if units == "seconds1":
        plt.xticks([0,5,10,15])
        # plt.xlabel("Time (seconds)")
    if units == "seconds2":
        plt.xticks([0,0.5,1.0,1.5])
        plt.ylabel("Vacuum (kPa)")
    if units == "minutes":
        plt.locator_params(axis="x", nbins=4)
        # plt.xlabel("Time (minutes)")
    if units == "hours":
        pass
        # plt.xlabel("Time (hours)")
    if units == "days":
        plt.xticks([0,1,2])
        # plt.xlabel("Time (days)")
    
    plt.xlim(left=left, right=right)
    plt.ylim(bottom=0, top=40)
    plt.tight_layout()
    # plt.legend()
    plt.savefig(outfile)

