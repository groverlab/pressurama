import plotter
import sys

plotter.filename = sys.argv[1]
plotter.kept_channels = [7]  # was [7,1,3,6,2]
plotter.timing = "local"
plotter.peak_entry = 25.0
plotter.peak_exit = 15.0

# total lines in file:  14707395

lines = 14707395

roi = [0, lines]

plotter.figsize = (8, 1.5) 
plotter.plot(roi, units="seconds", outfile="freq.png", freq=True)
