#!/usr/bin/env python3

from hashlib import new
import dearpygui.dearpygui as dpg
import sys
import time
import threading
import serial
import os
import numpy
import collections
import datetime
from itertools import islice
import random

history = 200
stdev_window = 30
pause = False
save_data = False
file_ready = False

global freqs
global meas
freqs = collections.deque(maxlen=history)
meas = collections.deque(maxlen=history)

def update_data():
    global sample, file_ready
    port = ""
    usb_count = 0
    devices = os.listdir("/dev")
    for device in devices:
        # if "cu.usbserial" in device:  <-- original
        # Recent versions of MacOS seem to use cu.usbmodem
        # so this version will catch both:
        if "cu.usb" in device:
            port = device
            usb_count += 1
    if usb_count == 0:
        sys.exit("No port found")
    if usb_count > 1:
        sys.exit("Multiple ports found")
    port = "/dev/" + port
    print(port)
    data = []
    ser = serial.Serial(port, 115200, timeout=1)
    ser.flush()
    
    ser.readline()  # discard first measurement

    sample = 1
    while not pause:
        # message = ser.readline().decode("utf-8")
        # if message.startswith("<") and message.strip().endswith(">"):
        #     freq = float((message.split("<"))[1].split(">")[0])
        # freq = random.random()
        s = ser.readline().decode("utf-8")
        if s.startswith("X") and s.strip().endswith("Y") and \
        s.count("X") == 1 and s.count("Y") == 1 and \
        s.count(" ") == 9 and s.count(":") == 8:
            # print(ser.inWaiting(), datetime.datetime.now().isoformat(), end="\t")
            # outfile.write(datetime.datetime.now().isoformat())
            tokens = s.split(" ")
            for token in tokens:
                if ":" in token:
                    channel = int(token.split(":")[0])
                    measurement = float(token.split(":")[1])
                    if channel == 0:
                        freq = measurement
                    # print("%0.1f\t" % (measurement), end="")
                    # outfile.write("," + str(measurement))
            # print()
            # outfile.write("\n")


        console_output = freq
        if console_output != "":
            freqs.append(freq)
            meas.append(sample)
            if save_data:
                if file_ready:
                    outfile.write(datetime.datetime.now().isoformat() + "," + str(freq) + "\n")
                else:
                    outfile = open(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv"), "w")
                    file_ready = True
            dpg.set_value('freq_plot', [list(meas), list(freqs)])          
            dpg.fit_axis_data('freq_plot_x_axis')
            dpg.fit_axis_data('freq_plot_y_axis')
            time.sleep(0.01)
            sample=sample+1

dpg.create_context()

def button_callback(sender, app_data, user_data):
    global pause, meas, freqs, sample, save_data, file_ready
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    if "CLEAR" in user_data:
        meas.clear()
        freqs.clear()
        sample = 1
    if "GTFO" in user_data:
        print("PAUSING")
        pause = True
        time.sleep(0.1)
        dpg.stop_dearpygui()
    if "SAVE DATA" in user_data:
        if app_data:  # if turning on saving:
            save_data = True
            print("SAVING")
        else:  # if turning off saving:
            save_data = False
            file_ready = False

def input_callback(sender, app_data, user_data):
    global history, freqs, meas, s, sa
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    new_history = app_data
    if new_history < history:  # if history is getting smaller
        freqs = collections.deque(islice(freqs, 0, new_history), maxlen=new_history)
        meas = collections.deque(islice(meas, 0, new_history), maxlen=new_history)
    elif new_history > history:  # if history is getting larger
        freqs = collections.deque(freqs, maxlen=new_history)
        meas = collections.deque(meas, maxlen=new_history)
    history = new_history

with dpg.window(label='Raw data', tag='win',width=800, height=700):
    with dpg.plot(height=250, width=-1):
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, tag='freq_plot_x_axis', no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label='Resonance frequency [Hz]', tag='freq_plot_y_axis')
        dpg.add_scatter_series(x=list(meas),y=list(freqs), label='Temp', parent='freq_plot_y_axis', tag='freq_plot')
    dpg.add_input_int(label="History", callback=input_callback, default_value=history, width=100)
    dpg.add_button(label="Clear", callback=button_callback, user_data="CLEAR", width=100)
    dpg.add_checkbox(label="Save data", callback=button_callback, user_data="SAVE DATA")
    dpg.add_button(label="Quit", callback=button_callback, user_data="GTFO", width=100)

            
dpg.create_viewport(title='3D printed vibrating tube mass sensors', width=850, height=640)

dpg.setup_dearpygui()
dpg.show_viewport()

thread = threading.Thread(target=update_data)
thread.start()
dpg.start_dearpygui()

dpg.destroy_context()

