
import serial
import time
import csv
import numpy as np
from statistics import mean
from funcs import *
from datetime import datetime
from datetime import date

today = date.today()
day = today.strftime("%m%d%Y")
now = datetime.now()

dt_string = now.strftime("%m/%d/%Y")
readtime = (now.strftime("%H:%M:%S") )
dataVec = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"] #new

name = "masterfile" #name the file here
tracker = 0
sample_size = 1800    #this number designates data points in the save data 
#If we are getting data each hour use (time/1.125) and edit arduino code delay to be 1125
#if we are getting data each half hour use (time) and edit arduino code delay to be 1000 

class SensorData(object):
    def __init__(self):
        #make connection to arduino
        try:
            self.ser = serial.Serial('COM4', 9600, timeout = 0.1)
            # I'm assuming this clears out all of the data beforehand.
            self.ser.flushInput()
            print("Connected")
            print("date and time =", dt_string)
        except:
            try:
                self.ser = serial.Serial('COM6', 9600, timeout = 0.1)
                self.ser.flushInput()
                print("Connected")
            except:
                print("No connection")
                

        #total sensors/current sensor
        self.sens_names = ["sensor1","sensor2","sensor3","sensor4","sensor5","sensor6","sensor7","sensor8","time","date"]
        with open(name+".csv", 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(self.sens_names)
            #csvfile.close() # may be the reason why masterfile doesn't take in code
        self.current_sens = 0
        self.total_sens = len(self.sens_names) 

        #pause the sensor input
        self.paused = False
        #data storage
        self.sample_size = sample_size    #this number designates data points in the save data
        self.data = []
        for i in range(self.total_sens):
            self.data.append(np.array(np.zeros([self.sample_size])))



    #gets data from sensors
    def get(self):
        global tracker
        try:
            #try to read and decode bytes
            ser_bytes = self.ser.readline()
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            db = float(decoded_bytes/100)
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y")
            readtime = (now.strftime("%H:%M:%S") )
            if(not self.paused):
                #update data array if not paused
                if(self.current_sens<self.total_sens - 2):
                    self.data[self.current_sens] = np.append(self.data[self.current_sens], db)
                    self.data[self.current_sens] = self.data[self.current_sens][1:self.sample_size]
                    #print(db)
                    dataVec[self.current_sens] =  db
                #print(dataVec)
                if(self.current_sens==self.total_sens - 2):
                    self.data[self.current_sens] = np.append(self.data[self.current_sens], readtime)
                    self.data[self.current_sens] = self.data[self.current_sens][1:self.sample_size]
                    #print(readtime)  
                    dataVec[self.current_sens] =  readtime
                if(self.current_sens==self.total_sens - 1):
                    self.data[self.current_sens] = np.append(self.data[self.current_sens], dt_string)
                    self.data[self.current_sens] = self.data[self.current_sens][1:self.sample_size]
                    #print(dt_string)
                    dataVec[self.current_sens] =  dt_string
                    tracker+=1
                    print(dataVec)  
            
                if(tracker > sample_size):
                    timeread = (now.strftime("%d_%H_%M_%S") )
                    with open(timeread+".csv", 'w') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(self.sens_names)
                        dataT = transpose(self.data)
                        csvwriter.writerows(dataT)
                        with open(name+".csv", 'a') as csvfile:
                            csvwriter = csv.writer(csvfile)
                            csvwriter.writerows(dataT)  #Pretransposed information
                            csvfile.close()
                        csvfile.close()
                        tracker = 0
            self.current_sens+=1
        except Exception as e:
            print("no data")
            return
        
        if(self.current_sens>=self.total_sens):
            self.current_sens = 0

    def pause(self):
        self.ser.flushInput()
        self.current_sens = 0
        self.paused = not self.paused

    def saveData(self,filename):
        #save raw data to csv file
        with open(filename+day+".csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(self.sens_names)
            dataT = transpose(self.data)
            csvwriter.writerows(dataT)
            csvfile.close()
