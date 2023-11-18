import csv

def center_window(w):
    # get screen width and height
    screen_width = w.master.winfo_screenwidth()
    screen_height = w.master.winfo_screenheight()
    window_width = w.width
    window_height = w.height

    # calculate position x and y coordinates
    x = (screen_width/2) - (window_width/2)
    y = (screen_height/2) - (window_height/2)
    w.master.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

def pauseRead(button, sd):
    #handles pause button
    sd.pause()
    if(button['text'] == "Pause"):
        button['text'] = "Read"
    else:
        button['text'] = "Pause"

def transpose(l1):
    #transposes 2d array
    l2 =[[row[i] for row in l1] for i in range(len(l1[0]))]
    return l2

def appendcsv(filename,data):
    with open("../"+filename+".csv", 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)
        csvfile.close()
