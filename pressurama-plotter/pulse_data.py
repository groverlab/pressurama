import plotter

plotter.filename = "pulse_data.csv"
plotter.kept_channels = [7, 1, 3, 6, 2]
plotter.timing = "local"

# total lines in file:  33984
# Pressurama channel:	Plot color:					Output number:
# 7						Blue						2
# 1						Orange						5
# 3						Green   <-- held down		3
# 6						Red							1
# 2						Purple						4

lines = 33984

roi = [4000, 8000]

plotter.figsize = (8, 1.5)  # 12, 1.5

plotter.kept_channels = [7]
plotter.plot(roi, units="seconds", outfile="pulse_data_ch2.png", color=0)
plotter.kept_channels = [1]
plotter.plot(roi, units="seconds", outfile="pulse_data_ch5.png", color=1)
plotter.kept_channels = [3]
plotter.plot(roi, units="seconds", outfile="pulse_data_ch3.png", color=2)
plotter.kept_channels = [6]
plotter.plot(roi, units="seconds", outfile="pulse_data_ch1.png", color=3)
plotter.kept_channels = [2]
plotter.plot(roi, units="seconds", outfile="pulse_data_ch4.png", color=4)


# plotter.figsize = (8, 3)  # 12, 5
# plotter.plot(roi[5], units="seconds2", outfile="06.png")
