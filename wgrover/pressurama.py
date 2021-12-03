import serial, os, sys, datetime
port = ""
usb_count = 0
devices = os.listdir("/dev")
for device in devices:
    if "cu.usbmodem" in device:
        port = device
        usb_count += 1
if usb_count == 0:
    sys.exit("No port found")
if usb_count > 1:
    sys.exit("Multiple ports found")
port = "/dev/" + port
data = []
ser = serial.Serial(port, 2000000)
ser.flush()
while True:
    s = ser.readline().decode("utf-8")
    channel = int(s.split("\t")[0])
    measurement = float(s.split("\t")[1])
    print(datetime.datetime.now().isoformat(), channel, ":", measurement, "\t", ser.inWaiting())
    