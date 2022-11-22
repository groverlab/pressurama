import plotter

plotter.filename = "pulse_data.csv"
plotter.kept_channels = [7, 1, 3, 6, 2]
plotter.timing = "local"

plotter.peak_entry = 15
plotter.peak_exit = 10

# total lines in file:  33984
# Pressurama channel:	Plot color:					Output number:
# 7						Blue						2
# 1						Orange						5
# 3						Green   <-- held down		3
# 6						Red							1
# 2						Purple						4  <-- freq analysis of this one

lines = 33984

# roi = [0000, 12000]  # this roi shows the whole dataset of interest



plotter.figsize = (8, 1.5)  # 12, 1.5
plotter.kept_channels = [2]



roi = [1450, 5930]  # first segment with free bellows
plotter.plot(roi, units="seconds", outfile="pulse_data_freq_1.png", freq=True, color=4)

roi = [6080, 10530]  # second segment with compressed bellows
plotter.plot(roi, units="seconds", outfile="pulse_data_freq_2.png", freq=True, color=4)