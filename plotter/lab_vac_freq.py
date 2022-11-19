import plotter
import sys

plotter.filename = "lab_vacuum.csv"
plotter.kept_channels = [3]  # was [7,1,3,6,2]
plotter.timing = "local"
plotter.peak_entry = 25.0
plotter.peak_exit = 15.0

lines = 383860


# # First and last three hours:

roi = [0, 850000*2]
plotter.plot(roi, units="seconds", outfile="freq.png", freq=True)

roi = [lines-850000*2, lines]
plotter.plot(roi, units="seconds", outfile="freq.png", freq=True)


# whole file:

roi = [0, lines]
plotter.plot(roi, units="seconds", outfile="lab_vac_freq.png", freq=True)
