import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import requests
import time


time_samples, data_storage, avg_storage, rsi_storage, volume_storage, askbid_storage =\
    ([] for _ in range(6))


def get_data(crypto_pairs, data_storage, askbid_storage, volume_storage):

    curr_temp, askbid_temp, vol_temp = ([] for _ in range(3))

    for pair in crypto_pairs:
        try:
            request = requests.get(
                f"https://bitbay.net/API/Public/{pair[0]}{pair[1]}/ticker.json"
            )
            orders = request.json()
            curr_temp.append([f'{pair[0]}-{pair[1]}', (orders['ask'], orders['bid'])])
            askbid_temp.append((orders['ask'], orders['bid']))
            vol_temp.append(orders['volume'])

        except requests.exceptions.RequestException:
            print("Connection problem.")
            return None

    volume_storage.append(vol_temp)
    askbid_storage.append(askbid_temp)
    data_storage.append(curr_temp)


def calculate_mov_avg(askbid_storage, avg_storage, window_size):

    storage_slice = askbid_storage[-window_size:]
    temp = []

    for curr_pair in range(3):
        inner_temp = []

        for ask_or_bid in range(2):
            summation = 0

            for sample in range(0, len(storage_slice)):
                summation += storage_slice[sample][curr_pair][ask_or_bid]
            summation /= len(storage_slice)
            inner_temp.append(summation)

        temp.append(inner_temp)

    avg_storage.append(temp)


def calculate_rsi(askbid_storage, rsi_storage, window_size):
    pass

def draw_figure(frame_number):

    plt.style.use('Solarize_Light2')
    time_samples.append(time.strftime("%H:%M:%S", time.localtime()))

    get_data(PAIRS, data_storage, askbid_storage, volume_storage)
    calculate_mov_avg(askbid_storage, avg_storage, AVG_WINDOW)
    calculate_rsi(askbid_storage, rsi_storage, RSI_WINDOW)

    plt.ion()
    plt.clf()
    plt.suptitle("Cryptocurrency Exchange Rates, RSI and Volume")

    for curr_pair in range(3):

        plt.subplot(3, 3, curr_pair+1)

        asks, bids, avg_asks, avg_bids = ([] for _ in range(4))

        for sample in data_storage:
            asks.append(sample[curr_pair][1][0])
            bids.append(sample[curr_pair][1][1])
        for avg_sample in avg_storage:
            avg_asks.append(avg_sample[curr_pair][0])
            avg_bids.append(avg_sample[curr_pair][1])

        plt.plot(time_samples, asks, "-o", label=data_storage[0][curr_pair][0] + " ask")
        plt.plot(time_samples, bids, "-o", label=data_storage[0][curr_pair][0] + " bid")
        plt.plot(time_samples, avg_asks, "o:", color = "#185986",
                 label=data_storage[0][curr_pair][0] + " ask mov avg")
        plt.plot(time_samples, avg_bids, "o:", color = "#1b6762",
                 label=data_storage[0][curr_pair][0] + " bid mov avg")
        plt.xlabel("Time", fontsize=9)
        plt.ylabel("Exchange Rates", fontsize=9)
        plt.xticks(rotation='vertical', fontsize=7)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                   ncol=2, mode="expand", borderaxespad=0.)

    for curr_pair in range(3):

        plt.subplot(3, 3, curr_pair+4)
        rsi_asks, rsi_bids = ([] for _ in range(2))

        for rsi_sample in rsi_storage:
            rsi_asks.append(rsi_sample[curr_pair][0])
            rsi_bids.append(rsi_sample[curr_pair][1])

        plt.plot(time_samples, rsi_asks, "o:", label=data_storage[0][curr_pair][0] + " ask RSI")
        plt.plot(time_samples, rsi_bids, "o:", label=data_storage[0][curr_pair][0] + " bid RSI")
        plt.xlabel("Time", fontsize=9)
        plt.ylabel("RSI", fontsize=9)
        plt.xticks(rotation='vertical', fontsize=7)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                   ncol=2, mode="expand", borderaxespad=0.)

    for curr_pair in range(3):

        plt.subplot(3, 3, curr_pair+7)
        volume = []

        for volume_sample in volume_storage:
            volume.append(volume_sample[curr_pair])

        plt.bar(time_samples, volume, align="center")
        plt.xlabel("Time", fontsize=9)
        plt.ylabel("Volume", fontsize=9)
        axes = plt.gca()
        axes.margins(y=0.2)
        plt.xticks(rotation='vertical', fontsize=7)

    if len(time_samples) > 9:
        del time_samples[0]
        del data_storage[0]
        del avg_storage[0]
        del volume_storage[0]
        del askbid_storage[0]
        del rsi_storage[0]

    plt.tight_layout()


if __name__ == '__main__':

    PAIRS = [('LTC', 'PLN'), ('ETH', 'PLN'), ('DASH', 'PLN')]
    FREQ = 5
    AVG_WINDOW = int(input('Przedział z jakiego liczyć średnią (max 10): '))
    RSI_WINDOW = int(input('Przedział z jakiego liczyć wskaźnik RSI? (max 10): '))

    animation = FuncAnimation(plt.figure(), draw_figure, interval=1000*FREQ)
    plt.show()
