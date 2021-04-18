import matplotlib.pyplot as plt
from crypto import fetchOffers
import random


RESOURCES = ['ETHPLN']
FREQUENCY = 5  # seconds
OFFSET = 0.1  # percentage


plt.ion()
fig, ax = plt.subplots()

x, ys, lines = [],[],[]
for resource in RESOURCES:
  ys.append( [[],[]] )  # new blank space for values: [[bids list],[asks list]]
  line1, = ax.plot([],[], label=f'{resource}_1', marker='o')
  line2, = ax.plot([],[], label=f'{resource}_2', marker='o', linestyle='--')
  lines.append([line1,line2])

ax.set_title('Crypto')
ax.set_xlabel('time in seconds')
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
    # add values to the plots
    lines[i][0].set_xdata(x)
    lines[i][0].set_ydata(ys[i][0])
    lines[i][1].set_xdata(x)
    lines[i][1].set_ydata(ys[i][1])
    plt.pause(0.1)  # so that I don't get blocked on the API
  print(f'Sleeping for {FREQUENCY}s...')
  plt.pause(FREQUENCY)
  interval += 1
