from datetime import datetime

import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy

filename = ""
kept_channels = [0,1,2,3,4,5,6,7]
timing = "global"  # "local" or "global"
figsize = (12, 1.5)  # thin; using (12, 5) for tall
peak_entry = None
peak_exit = None

plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.size"] = "12"

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

#  From the datasheet:  https://www.nxp.com/docs/en/data-sheet/MPX4250D.pdf
#  Vout = VCC × (P × 0.00369 + 0.04)
#  P = pressure in kPa
#  VCC = 5
#  Vout = (V / 1023) × 5     (V is the actual measured value sent from Arduino, between 0 and 1023)
#  P = (V - 40.92) / 3.77487
def P(V):  # pressure in kPa from Vout in arb. units from 0 to 1023
    return (V - 40.92) / 3.77487

def plot(roi, box = None, units="seconds", outfile="out.pdf", freq=False, color=-1):
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
    # peak_times = []
    # peak_durations = []
    # last_peak_time = 0
    in_peak = False
    peak_count = 0
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
                    pressure = P(float(tokens[j+1]))
                    channels[kept_channels.index(j)][i-begin] = pressure
                    if freq:
                        if in_peak:  # in peak, look for exit
                            if pressure < peak_exit:  # exiting peak
                                peak_count += 1
                                # peak_times.append(times[i-begin])
                                # peak_durations.append(times[i-begin] - last_peak_time)
                                # last_peak_time = times[i-begin]
                                in_peak = False
                        else:  # not in peak, look for entry
                            if pressure > peak_entry:  # entering peak
                                in_peak = True

    if freq:
        print(f"freq analysis for roi {begin} to {end}")
        print(f"peak count = {peak_count}")
        print(f"elapsed seconds = {right-left}")
        print(f"frequency = {peak_count / (right-left)} Hz")
        print(f"period = {(right-left) / peak_count} s")

    plt.figure(figsize=figsize, dpi=1200)
    for i, name in enumerate(kept_channels):
        print("  plotting ", name)
        if color >= 0:  # if a color number is specified, use it:
            plt.plot(times, channels[i], label=name, color=colors[color])
        else:  # otherwise just use the next default color:
            plt.plot(times, channels[i], label=name)
        if freq:
            plt.plot(times, numpy.full(len(times), peak_entry))
            plt.plot(times, numpy.full(len(times), peak_exit))
    if box:
        print("  rectangle at", box_start_time, 0, box_end_time-box_start_time, 40)
        rect=mpatches.Rectangle((box_start_time, 0), box_end_time-box_start_time, 40,
                                fill=False, color="black", linewidth=2, zorder=4, clip_on=False)
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
    if units == "seconds2":
        plt.ylim(bottom=-5, top=45)  # a little more space for labels on bottom plot
    plt.tight_layout()
    # plt.legend()
    plt.savefig(outfile)

    # if freq:
    #     dfile = open("durations.csv", "w")
    #     for peak_time, peak_duration in zip(peak_times, peak_durations):
    #         dfile.write(f"{peak_time},{peak_duration}\n")
    #     dfile.close()


