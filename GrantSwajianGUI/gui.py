#import matplotlib and TKinter compatibility packages
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

#import tkinter and themedtk packages
import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk as themes

#import sensordata object
from sensordata import *

class PressureGUI(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)
        #Sensor Data object
        self.sd = SensorData()
        self.width = 1000
        self.height = 470
        #gui setup
        self.master = master
        self.master.title("Pressure")
        center_window(self)
        self.ContentFrame = ttk.Frame(self.master)
        self.ContentFrame.grid(row=1,column=1)
        ttk.Label(self.ContentFrame, text="Pressure",width=20, anchor=tk.N, font=("Arial", 25)).grid(row=1,column=1)
        #button frame
        self.ButtonFrame = ttk.Frame(self.ContentFrame)
        self.ButtonFrame.grid(row=2,column=1)
        #quit button
        self.QuitBtn = ttk.Button(self.ButtonFrame, text="Quit", command=self.master.destroy).grid(row=1,column=1)
        #pause button
        self.PauseBtn = ttk.Button(self.ButtonFrame, text="Pause")
        self.PauseBtn.config(command = lambda: pauseRead(self.PauseBtn, self.sd))
        self.PauseBtn.grid(row=1,column=2)
        #save button
        self.SaveBtn = ttk.Button(self.ButtonFrame, text = "Save")
        self.SaveBtn.config(command = self.savePopup)
        self.SaveBtn.grid(row=1,column=3)
        #create sensor graph
        plt.style.use('dark_background')
        self.figure = plt.Figure()
        self.a = self.figure.add_subplot(111)
        self.a.set_title(self.sd.sens_names[0])
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=1,column=2)

    def getData(self):
        #gets data from sensorData object
        self.sd.get()
    
    def plotData(self):
        #plots data from all sensors
        plotCols = ["red","lightcoral","pink","cyan","yellow","lightyellow","green","lightgreen","blue","lightblue","violet","lightviolet"]
        self.a.clear()
        activeRange = self.sd.total_sens - 2
        for i in range(activeRange):
            self.a.plot(self.sd.data[i],marker = '*', color = plotCols[i])
        self.a.relim()
        self.a.autoscale_view()
        self.canvas.draw_idle()

    def savePopup(self):
        self.w=popupWindow(self.master,self.sd)
        self.SaveBtn["state"] = "disabled" 
        self.master.wait_window(self.w.master)
        self.SaveBtn["state"] = "normal"


#popup window used for saving data
class popupWindow(object):
    def __init__(self,master,sd):
        self.sd = sd
        self.width = 200
        self.height = 200
        self.master=tk.Toplevel(master)
        self.ContentFrame = ttk.Frame(self.master)
        self.ContentFrame.place(in_=self.master, anchor="c", relx=.5, rely=.5)
        center_window(self)
        self.SaveLabel=ttk.Label(self.ContentFrame,text="Enter File Name")
        self.SaveLabel.pack()
        self.EntryBox=ttk.Entry(self.ContentFrame)
        self.EntryBox.pack()
        self.ButtonFrame = ttk.Frame(self.ContentFrame)
        self.ButtonFrame.pack()
        self.SaveBtn=ttk.Button(self.ButtonFrame,text='Save',command=self.saveFile)
        self.SaveBtn.grid(row=1,column=1)
        self.CancelBtn=ttk.Button(self.ButtonFrame,text='cancel',command=self.master.destroy)
        self.CancelBtn.grid(row=1,column=2)
    def saveFile(self):
        self.sd.saveData(self.EntryBox.get())
        self.master.destroy()