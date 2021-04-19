import requests
import matplotlib.pyplot as plt
import time


def get_data(first_currency, second_currency):

  try:
    request = requests.get(
      f"https://bitbay.net/API/Public/{first_currency}{second_currency}/ticker.json"
    )
    orders = request.json()

  except requests.exceptions.RequestException:
    print("Connection problem.")
    return None

  return orders


def draw_figure():

  plt.style.use('ggplot')
  asks, bids = ({pair[0]: [] for pair in PAIRS} for _ in range(2))
  req_numbers, subplots = ([] for _ in range(2))
  num = 0

  plt.ion()
  figure, ax = plt.subplots(nrows=PAIRS_COUNT, figsize=(10, 10))

  for i in range(PAIRS_COUNT):
    subplots.append(ax[i].plot(req_numbers, asks[PAIRS[i][0]], color = 'red', label="Asks")[0])
    subplots.append(ax[i].plot(req_numbers, bids[PAIRS[i][0]], color = 'blue', label="Bids")[0])
    ax[i].set_xlim(0, 50)
    ax[i].set_title(PAIRS[i][0])
    ax[i].legend()


  while num < 50:

    for pair in PAIRS:
      request = get_data(pair[0], pair[1])
      asks[pair[0]].append(request['ask'])
      bids[pair[0]].append(request['bid'])

    num += 1
    req_numbers.append(num)

    temp = 0
    for i in range(len(subplots)):
      if i % 2 == 0:
        subplots[i].set_data(req_numbers, asks[PAIRS[temp][0]])
      else:
        subplots[i].set_data(req_numbers, bids[PAIRS[temp][0]])
        temp += 1

    for i in range(PAIRS_COUNT):
      ax[i].relim()
      ax[i].autoscale_view(scalex=False)


    figure.canvas.draw()

    if num == 50:
      plt.savefig('graph.png')

    figure.canvas.flush_events()
    time.sleep(FREQ)


if __name__ == '__main__':

  PAIRS = [('LTC', 'PLN'), ('ETH', 'PLN'), ('BCC', 'PLN')]
  PAIRS_COUNT = len(PAIRS)
  FREQ = 5

  draw_figure()
