#!/usr/bin/env python3

from hashlib import new
import dearpygui.dearpygui as dpg
import sys
import time
import threading
import serial
from serial.tools.list_ports import comports
import collections
import datetime
from itertools import islice
import platform

history = 200
pause = False
save_data = False
file_ready = False

ch0 = collections.deque(maxlen=history)
ch1 = collections.deque(maxlen=history)
ch2 = collections.deque(maxlen=history)
ch3 = collections.deque(maxlen=history)
ch4 = collections.deque(maxlen=history)
ch5 = collections.deque(maxlen=history)
ch6 = collections.deque(maxlen=history)
ch7 = collections.deque(maxlen=history)
meas = collections.deque(maxlen=history)

# port = ""
# usb_count = 0
# devices = os.listdir("/dev")
# for device in devices:
#     # if "cu.usbserial" in device:  <-- original
#     # Recent versions of MacOS seem to use cu.usbmodem
#     # so this version will catch both:
#     if "cu.usb" in device:
#         port = device
#         usb_count += 1
# if usb_count == 0:
#     sys.exit("No port found")
# if usb_count > 1:
#     sys.exit("Multiple ports found")
# port = "/dev/" + port
# print(port)


ports = 0
port = ""
for p in comports():
    if "USB" in str(p):
        port = p.name
        ports += 1

if ports == 0:
    sys.exit("❌ No port found - is the Pressurama plugged in?")

if ports >= 2:
    sys.exit("❌ Too many ports found - unplug everything but the Pressurama and try again")

if platform.system() == "Darwin":  # if MacOS...
    port = "/dev/" + port   # ...prepend /dev/

print("✅ Found a Pressurama at " + port)



data = []
ser = serial.Serial(port, 2000000, timeout=1)
ser.flush()
ser.readline()  # discard first measurement

def update_data():
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
            print(ser.inWaiting())
            tokens = s.split(" ")
            for token in tokens:
                if ":" in token:
                    channel = int(token.split(":")[0])
                    measurement = float(token.split(":")[1])
                    if channel == 0:
                        meas0 = measurement
                    if channel == 1:
                        meas1 = measurement
                    if channel == 2:
                        meas2 = measurement
                    if channel == 3:
                        meas3 = measurement
                    if channel == 4:
                        meas4 = measurement
                    if channel == 5:
                        meas5 = measurement
                    if channel == 6:
                        meas6 = measurement
                    if channel == 7:
                        meas7 = measurement
                    # print("%0.1f\t" % (measurement), end="")
                    # outfile.write("," + str(measurement))
            # print()
            # outfile.write("\n")


        # console_output = meas0
        # if console_output != "":
        ch0.append(meas0)
        ch1.append(meas1)
        ch2.append(meas2)
        ch3.append(meas3)
        ch4.append(meas4)
        ch5.append(meas5)
        ch6.append(meas6)
        ch7.append(meas7)
        meas.append(sample)
        if save_data:
            if file_ready:
                outfile.write(datetime.datetime.now().isoformat() + "," + str(meas0) + "\n")  # FIXME
            else:
                outfile = open(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv"), "w")
                file_ready = True
        dpg.set_value('freq_plot0', [list(meas), list(ch0)])          
        dpg.fit_axis_data('freq_plot_x_axis0')
        dpg.fit_axis_data('freq_plot_y_axis0')
        dpg.set_value('freq_plot1', [list(meas), list(ch1)])   
        dpg.fit_axis_data('freq_plot_x_axis1')
        dpg.fit_axis_data('freq_plot_y_axis1')
        dpg.set_value('freq_plot2', [list(meas), list(ch2)])   
        dpg.fit_axis_data('freq_plot_x_axis2')
        dpg.fit_axis_data('freq_plot_y_axis2')
        dpg.set_value('freq_plot3', [list(meas), list(ch3)])   
        dpg.fit_axis_data('freq_plot_x_axis3')
        dpg.fit_axis_data('freq_plot_y_axis3')
        dpg.set_value('freq_plot4', [list(meas), list(ch4)])   
        dpg.fit_axis_data('freq_plot_x_axis4')
        dpg.fit_axis_data('freq_plot_y_axis4')
        dpg.set_value('freq_plot5', [list(meas), list(ch5)])   
        dpg.fit_axis_data('freq_plot_x_axis5')
        dpg.fit_axis_data('freq_plot_y_axis5')
        dpg.set_value('freq_plot6', [list(meas), list(ch6)])   
        dpg.fit_axis_data('freq_plot_x_axis6')
        dpg.fit_axis_data('freq_plot_y_axis6')
        dpg.set_value('freq_plot7', [list(meas), list(ch7)])   
        dpg.fit_axis_data('freq_plot_x_axis7')
        dpg.fit_axis_data('freq_plot_y_axis7')
        # time.sleep(0.01)
        sample=sample+1

dpg.create_context()

def button_callback(sender, app_data, user_data):
    global pause, meas, ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7, sample, save_data, file_ready
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    if "CLEAR" in user_data:
        meas.clear()
        ch0.clear()
        ch1.clear()
        ch2.clear()
        ch3.clear()
        ch4.clear()
        ch5.clear()
        ch6.clear()
        ch7.clear()
        sample = 1
    if "GTFO" in user_data:
        print("QUITTING")
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
    global history, ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7, meas
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    new_history = app_data
    if new_history < history:  # if history is getting smaller
        ch0 = collections.deque(islice(ch0, 0, new_history), maxlen=new_history)
        ch1 = collections.deque(islice(ch1, 0, new_history), maxlen=new_history)
        ch2 = collections.deque(islice(ch2, 0, new_history), maxlen=new_history)
        ch3 = collections.deque(islice(ch3, 0, new_history), maxlen=new_history)
        ch4 = collections.deque(islice(ch4, 0, new_history), maxlen=new_history)
        ch5 = collections.deque(islice(ch5, 0, new_history), maxlen=new_history)
        ch6 = collections.deque(islice(ch6, 0, new_history), maxlen=new_history)
        ch7 = collections.deque(islice(ch7, 0, new_history), maxlen=new_history)
        meas = collections.deque(islice(meas, 0, new_history), maxlen=new_history)
    elif new_history > history:  # if history is getting larger
        ch0 = collections.deque(ch0, maxlen=new_history)
        ch1 = collections.deque(ch1, maxlen=new_history)
        ch2 = collections.deque(ch2, maxlen=new_history)
        ch3 = collections.deque(ch3, maxlen=new_history)
        ch4 = collections.deque(ch4, maxlen=new_history)
        ch5 = collections.deque(ch5, maxlen=new_history)
        ch6 = collections.deque(ch6, maxlen=new_history)
        ch7 = collections.deque(ch7, maxlen=new_history)
        meas = collections.deque(meas, maxlen=new_history)
    history = new_history

with dpg.window(label='Raw data', tag='win', width=800, height=1000):
    with dpg.plot(height=100, width=-1):
        x_axis0 = dpg.add_plot_axis(dpg.mvXAxis, tag='freq_plot_x_axis0', no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        y_axis0 = dpg.add_plot_axis(dpg.mvYAxis, label='Channel 0', tag='freq_plot_y_axis0')
        dpg.add_scatter_series(x=list(meas),y=list(ch0), label='Temp', parent='freq_plot_y_axis0', tag='freq_plot0')
    with dpg.plot(height=100, width=-1):
        x_axis1 = dpg.add_plot_axis(dpg.mvXAxis, tag='freq_plot_x_axis1', no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        y_axis1 = dpg.add_plot_axis(dpg.mvYAxis, label='Channel 1', tag='freq_plot_y_axis1')
        dpg.add_scatter_series(x=list(meas),y=list(ch1), label='Temp', parent='freq_plot_y_axis1', tag='freq_plot1')
    with dpg.plot(height=100, width=-1):
        x_axis2 = dpg.add_plot_axis(dpg.mvXAxis, tag='freq_plot_x_axis2', no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        y_axis2 = dpg.add_plot_axis(dpg.mvYAxis, label='Channel 2', tag='freq_plot_y_axis2')
        dpg.add_scatter_series(x=list(meas),y=list(ch2), label='Temp', parent='freq_plot_y_axis2', tag='freq_plot2')
    with dpg.plot(height=100, width=-1):
        x_axis3 = dpg.add_plot_axis(dpg.mvXAxis, tag='freq_plot_x_axis3', no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        y_axis3 = dpg.add_plot_axis(dpg.mvYAxis, label='Channel 3', tag='freq_plot_y_axis3')
        dpg.add_scatter_series(x=list(meas),y=list(ch3), label='Temp', parent='freq_plot_y_axis3', tag='freq_plot3')
    with dpg.plot(height=100, width=-1):
        x_axis4 = dpg.add_plot_axis(dpg.mvXAxis, tag='freq_plot_x_axis4', no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        y_axis4 = dpg.add_plot_axis(dpg.mvYAxis, label='Channel 4', tag='freq_plot_y_axis4')
        dpg.add_scatter_series(x=list(meas),y=list(ch4), label='Temp', parent='freq_plot_y_axis4', tag='freq_plot4')
    with dpg.plot(height=100, width=-1):
        x_axis5 = dpg.add_plot_axis(dpg.mvXAxis, tag='freq_plot_x_axis5', no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        y_axis5 = dpg.add_plot_axis(dpg.mvYAxis, label='Channel 5', tag='freq_plot_y_axis5')
        dpg.add_scatter_series(x=list(meas),y=list(ch5), label='Temp', parent='freq_plot_y_axis5', tag='freq_plot5')
    with dpg.plot(height=100, width=-1):
        x_axis6 = dpg.add_plot_axis(dpg.mvXAxis, tag='freq_plot_x_axis6', no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        y_axis6 = dpg.add_plot_axis(dpg.mvYAxis, label='Channel 6', tag='freq_plot_y_axis6')
        dpg.add_scatter_series(x=list(meas),y=list(ch6), label='Temp', parent='freq_plot_y_axis6', tag='freq_plot6')
    with dpg.plot(height=100, width=-1):
        x_axis7 = dpg.add_plot_axis(dpg.mvXAxis, tag='freq_plot_x_axis7', no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        y_axis7 = dpg.add_plot_axis(dpg.mvYAxis, label='Channel 7', tag='freq_plot_y_axis7')
        dpg.add_scatter_series(x=list(meas),y=list(ch7), label='Temp', parent='freq_plot_y_axis7', tag='freq_plot7')
    dpg.add_input_int(label="History", callback=input_callback, default_value=history, width=100)
    dpg.add_button(label="Clear", callback=button_callback, user_data="CLEAR", width=100)
    dpg.add_checkbox(label="Save data", callback=button_callback, user_data="SAVE DATA")
    dpg.add_button(label="Quit", callback=button_callback, user_data="GTFO", width=100)

            
dpg.create_viewport(title='Pressurama', width=800, height=1000)

dpg.setup_dearpygui()
dpg.show_viewport()

thread = threading.Thread(target=update_data)
thread.start()
dpg.start_dearpygui()

dpg.destroy_context()

