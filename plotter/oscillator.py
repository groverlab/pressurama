import plotter
plotter.filename = "oscillator.csv"
plotter.kept_channels = [7,1,3,6,2]

# total lines in file:  14707395


plotter.plot(4000, 6000, "seconds", "02.pdf")
plotter.plot(0, 10000,"minutes", "01.pdf")

