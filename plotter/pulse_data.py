import plotter
import sys

plotter.filename = "pulse_data.csv"
plotter.kept_channels = [7,1,3,6,2]
plotter.timing = "local"

# total lines in file:  33984

lines = 33984

plotter.figsize = (8, 1.5)  # 12, 1.5
plotter.plot([5000, 7000], units="seconds", outfile="pulse_data.png")
# plotter.plot(roi[1], box=roi[2], units="hours", outfile="02.png")
# plotter.plot(roi[2], box=roi[3], units="minutes", outfile="03.png")
# plotter.plot(roi[3], box=roi[4], units="minutes", outfile="04.png")
# plotter.plot(roi[4], box=roi[5], units="seconds1", outfile="05.png")

# plotter.figsize = (8, 3)  # 12, 5
# plotter.plot(roi[5], units="seconds2", outfile="06.png")
