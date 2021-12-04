import matplotlib.pyplot as plt
from datetime import datetime
infile = open("out.csv", "r")
times = []
values = []
for line in infile:
    tokens = line.split(",")
    times.append(datetime.fromisoformat(tokens[0]))
    values.append(float(tokens[1]))
plt.plot(times, values)
plt.show()

