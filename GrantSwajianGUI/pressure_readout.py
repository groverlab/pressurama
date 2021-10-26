from gui import *

#initializing Tkinter with themed addon
root = themes.ThemedTk(theme="equilux", toplevel = True, themebg = True)
g = PressureGUI(root)


#main loop
while True:
    #gets the data
    g.getData()
    g.plotData()
    #updating tkinter gui (not using mainloop)
    root.update()
    root.update_idletasks()