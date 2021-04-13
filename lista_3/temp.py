import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from matplotlib import style

FILE_PATH = 'market.csv'



counter = 0
time = 0
x1 = []
x2 = []
y1 = []
y2 = []
y3 = []
y4 = []
z1 = []
z2 = []
z3 = []
z4 = []

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)
fig.legend(loc=3)

def animation(i):
    df = pd.read_csv(FILE_PATH, names=['bids','asks','key'])
    global counter
    global time
    counter += 1
    if counter % 4 == 0:    
        x1.append(time)
        y1.append(df['bids'][counter])
        z1.append(df['asks'][counter])
        legend = df['key'][counter]
        ax1.cla()
        ax1.plot(x1, y1,'g-d', label='bids ' + legend)
        ax1.plot(x1, z1,'r-d', label='asks ' + legend)
        ax1.legend(loc=1)
    elif counter % 4 == 1:
        x2.append(time)
        y2.append(df['bids'][counter])
        z2.append(df['asks'][counter])
        legend = df['key'][counter]
        ax2.cla()
        ax2.plot(x2, y2,'g-d', label='bids ' + legend)
        ax2.plot(x2, z2,'r-d', label='asks ' + legend)
        ax2.legend(loc=1)
    # elif counter % 4 == 2:
    #     x.append(time)
    #     y3.append(df['bids'][counter])
    #     z3.append(df['asks'][counter])
    #     legend = df['key'][counter]
    #     ax3.cla()
    #     ax3.plot(x, y3,'g-d', label='bids ' + legend)
    #     ax3.plot(x, z3,'r-d', label='asks ' + legend)
    #     ax3.legend(loc=1)
    # elif counter % 4 == 3:
    #     x.append(time)
    #     y4.append(df['bids'][counter])
    #     z4.append(df['asks'][counter])
    #     legend = df['key'][counter]
    #     ax4.cla()
    #     ax4.plot(x, y4,'g-d', label='bids ' + legend)
    #     ax4.plot(x, z4,'r-d', label='asks ' + legend)
    #     ax4.legend(loc=1)
        time +=1 
ani = FuncAnimation(plt.gcf(), animation, interval=250)

plt.tight_layout()
plt.show() 