import plotter
plotter.filename = "/Users/wgrover/Dropbox/pneumatic rocker/Lab_Vacuum_Pressure.csv"
plotter.kept_channels = [3]
plotter.timing = "local"

# total lines in file:  14707395

plotter.figsize = (8, 1.5)  # 12, 1.5
plotter.plot([1,100000], units="minutes", outfile="vacuum.png")
