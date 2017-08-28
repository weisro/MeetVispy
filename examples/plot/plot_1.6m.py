import os
import numpy as np

from vispy import plot as vp
from vispy.color import get_colormap

#create plot widget
fig = vp.Fig(size=(800, 800), show=False)

#generate colors
pairs = ["EUR_CHF", "EUR_USD"]
weeks = [1]
cmap = get_colormap('hsl', value=0.5)
colors = cmap.map(np.linspace(0.1, 0.9, len(pairs)*len(weeks)*2))

j = 0
for pair in pairs:
    for week in weeks:
        file = pair + "_Week" + str(week)
        path = os.path.sep.join(["C:", "Users", "Roman", "fxdata", file, file + ".csv"])
        data = np.genfromtxt(path, skip_header=1, delimiter=",")
        for i in [4, 5]:
            y = data[:, i]
            x = np.arange(0, len(y), 1)
            #create line plot
            line = fig[0, 0].plot((x, y), symbol='o', width=3, title='~1.6 mill. points', xlabel='Time', ylabel='Price', color=colors[j])
            j += 1

# add grid to plot
grid = vp.visuals.GridLines(color=(0, 0, 0, 0.5))
grid.set_gl_state('translucent')
fig[0, 0].view.add(grid)

if __name__ == '__main__':
    fig.show(run=True)
