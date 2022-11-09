import plotter
plotter.filename = "oscillator.csv"
plotter.kept_channels = [7,1,3,6,2]

# total lines in file:  14707395

plotter.plot(10101100, 10101200, "seconds", "05.pdf")
plotter.plot(10101000, 10102000, "seconds", "04.pdf")
plotter.plot(10100000, 10200000, "minutes", "03.pdf")
plotter.plot(10000000, 11000000, "hours", "02.pdf")
plotter.plot(0, 14707395, "days", "01.pdf")

