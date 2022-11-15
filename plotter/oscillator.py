import plotter
import sys

plotter.filename = sys.argv[1]
plotter.kept_channels = [7,1,3,6,2]
plotter.timing = "local"

# total lines in file:  14707395

lines = 14707395

roi = ([0, lines],
       [int(0.7*lines), int(0.8*lines)],
       [int(0.77*lines), int(0.78*lines)],
       [int(0.777*lines), int(0.778*lines)],
       [int(0.7777*lines), int(0.7778*lines)],
       [int(0.77777*lines), int(0.77778*lines)])

plotter.figsize = (8, 1.5)  # 12, 1.5
plotter.plot(roi[0], box=roi[1], units="days", outfile="01.png")
plotter.plot(roi[1], box=roi[2], units="hours", outfile="02.png")
plotter.plot(roi[2], box=roi[3], units="minutes", outfile="03.png")
plotter.plot(roi[3], box=roi[4], units="seconds", outfile="04.png")
plotter.plot(roi[4], box=roi[5], units="seconds", outfile="05.png")

plotter.figsize = (8, 5)  # 12, 5
plotter.plot(roi[5], units="seconds", outfile="06.png")
