import plotter
plotter.filename = "oscillator.csv"
plotter.kept_channels = [7,1,3,6,2]
plotter.timing = "global"

# total lines in file:  14707395

plotter.plot([0, 1000], box=[400, 500], units="seconds", outfile="01.pdf")
plotter.plot([400, 500], units="seconds", outfile="02.pdf")

