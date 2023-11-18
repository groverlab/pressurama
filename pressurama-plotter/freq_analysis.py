import plotter
import sys

plotter.filename = "oscillator.csv"
plotter.kept_channels = [7]  # was [7,1,3,6,2]
plotter.timing = "local"
plotter.peak_entry = 25.0
plotter.peak_exit = 15.0

# total lines in file:  14707395

lines = 14707395


print("first 3 hours >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
roi = [0, 850000]
plotter.plot(roi, units="seconds", outfile="freq.png", freq=True)

print("last 3 hours >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
roi = [lines-850000, lines]
plotter.plot(roi, units="seconds", outfile="freq.png", freq=True)


print("whole file >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
roi = [0, lines]
plotter.plot(roi, units="seconds", outfile="freq.png", freq=True)
