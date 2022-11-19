# total lines in file:  383860

from datetime import datetime

import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

filename = "lab_vacuum.csv"
kept_channels = [3]
timing = "local"  # "local" or "global"
figsize = (8, 1.5)  # thin; using (12, 5) for tall

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

def plot(roi, units="seconds", outfile="out.pdf"):
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
            for j in range(8):
                if j in kept_channels:
                    channels[kept_channels.index(j)][i-begin] = P(float(tokens[j+1]))


    plt.figure(figsize=figsize, dpi=1200)
    for i, name in enumerate(kept_channels):
        print("  plotting ", name)
        plt.plot(times, channels[i], label=name)

    plt.ylim([0,80])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Vac. (kPa)")
    plt.tight_layout()
    plt.savefig(outfile)

plot([300, 383860], units="minutes", outfile="lab_vacuum.png")
