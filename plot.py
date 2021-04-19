import matplotlib.pyplot as plt
from crypto import fetchOffers
import random
import numpy as np


RESOURCES = ['BTCPLN','ETHPLN','LTCPLN']
FREQUENCY = 5  # seconds
OFFSET = 0.1  # percentage
NORMALIZE = True


plt.ion()
fig, ax = plt.subplots()

x, ys, lines = [],[],[]
for resource in RESOURCES:
  ys.append( [[],[]] )  # new blank space for values: [[bids list],[asks list]]
  line_bids, = ax.plot([],[], label=f'{resource}_bids', marker='o')
  line_asks, = ax.plot([],[], label=f'{resource}_asks', marker='o', linestyle='--')
  lines.append([line_bids,line_asks])

ax.set_title('Crypto')
ax.set_xlabel('time [s]')
ax.set_ylabel('value')
ax.legend()

interval = 0
while 1:
  x.append(interval*FREQUENCY)  # add x axis point (frequency interval)
  print('\nFetching data from an external API...')
  for i, resource in enumerate(RESOURCES):
    # get data from the API
    offers = fetchOffers(resource)
    if len(offers):
      print('Data received!')
      bids, asks = offers
      best_bid = bids[0][0]
      best_ask = asks[0][0]
      ys[i][0].append(best_bid)
      ys[i][1].append(best_ask)
    else:
      print('No data. Trying again...')
      ys[i][0].append(None)
      ys[i][1].append(None)
    # adjust both axes based on all plot values
    Y = [el for y in [y[0]+y[1] for y in ys] for el in y]  # flatten ys
    offset = (OFFSET*max(x), OFFSET*(max(Y)-min(Y)))
    ax.set_xlim(min(x)-offset[0], max(x)+offset[0])
    ax.set_ylim(min(Y)-offset[1], max(Y)+offset[1])
    # get bids and asks lists
    yb = ys[i][0] # bids
    ya = ys[i][1] # asks
    # normalize data
    if NORMALIZE:
      ax.set_ylim(0-OFFSET,1+OFFSET)
      yb = np.array(ys[i][0])  # y normalized bids
      yb = (yb-min(yb))/(max(yb)-min(yb))
      ya = np.array(ys[i][1])  # y normalized asks
      ya = (ya-min(ya))/(max(ya)-min(ya))
    # add values to the plots
    lines[i][0].set_xdata(x)
    lines[i][0].set_ydata(yb)
    lines[i][1].set_xdata(x)
    lines[i][1].set_ydata(ya)
    plt.pause(0.1)  # so that I don't get blocked on the API
  print(f'Sleeping for {FREQUENCY}s...')
  plt.pause(FREQUENCY)
  interval += 1
