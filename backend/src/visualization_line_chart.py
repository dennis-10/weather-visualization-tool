import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

station = [{ "number": 0, "name": "Vidigal", "volume" : [30, 90, 10, 30, 40, 30, 100, 80, 90, 70, 30, 30, 90, 10, 30, 40, 30, 100, 80, 90, 70, 30]},
{ "number": 1, "name": "Tijuca", "volume" : [10, 20, 10, 20, 20, 20, 10, 10, 20, 20, 0, 30, 90, 10, 30, 40, 30, 100, 80, 90, 70, 30]}, 
{ "number": 2, "name": "Alemão", "volume" : [100, 90, 80, 100, 70, 80, 100, 90, 90, 80, 80, 30, 90, 10, 30, 40, 30, 100, 80, 90, 70, 30]}]

choice = 1

title = 'Station: ' + station[choice]['name']

x = np.arange(0,len(station[choice]['volume']),1)
y = station[choice]['volume']

tfinal = max(x)
x0 = 0

fig, ax = plt.subplots(1, 1, figsize = (6, 3))


def animate(i):
    ax.cla() # clear the previous image
    ax.plot(x[:i], y[:i]) # plot the line
    ax.set_xlim([x0, tfinal]) # fix the x axis
    ax.set_ylim([1.1*np.min(y), 1.1*np.max(y)]) # fix the y axis
    ax.set_title(title)

anim = animation.FuncAnimation(fig, animate, frames = len(x) + 1, interval = 350, blit = False)
plt.show()