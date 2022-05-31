from matplotlib import pyplot as plt
import json
import math

data = {}

with open('train/training/metrics.json') as file:
    for line in file:
        row = json.loads(line)
        for key, val in row.items():
            if key not in data:
                data[key] = []
            data[key].append(val)

vals = data.keys()

ncols = 2
nrows = math.ceil(len(vals) / ncols)

fig, ax = plt.subplots(nrows, ncols)

col, row = 0, 0
for key in vals:
    ax[row][col].set_title(key)
    ax[row][col].plot(data[key])
    row += 1
    if row >= nrows:
        row = 0
        col += 1


plt.show()
