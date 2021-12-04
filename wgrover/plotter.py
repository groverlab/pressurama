import matplotlib.pyplot as plt
from datetime import datetime
infile = open("out.csv", "r")
times = []
ch0 = []
ch1 = []
ch2 = []
ch3 = []
ch4 = []
ch5 = []
ch6 = []
ch7 = []
for line in infile:
    tokens = line.split(",")
    times.append(datetime.fromisoformat(tokens[0]))
    for i, ch in enumerate((ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7)):
        ch.append(float(tokens[i+1]))
for i, ch in enumerate((ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7)):
    plt.plot(times, ch, label=i)
plt.legend()
plt.show()

