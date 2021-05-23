# Trendy wzrostowe / spadkowe / boczne
#
# 1) Na podstawie wskaźnika RSI sklasyfikować każdy zasób i obok wykresu dodać informację
# (graficzną / tekstową) o typie trendu w jakim aktualnie się znajduje. (4pkt)
#
# 2) Pośród trzech wyświetlanych wykresów na bieżąco oznaczać zasób, który ma największy wolumen
# spośród zasobów nie będących w trendzie spadkowym.
# Przykładowo: wyświetlamy LTCBTC, DASHBTC, ETHBTC. Dwa pierwsze są w trendzie wzrostowym,
# ostatni w spadkowym. Pierwszy ma wyraźnie najwyższy wolumen. Oznaczamy go jako kandydata. (3pkt)
#
# 3) Do funkcjonalności wyświetlania zasobów na wykresach, klasyfikacji ich trendu i wyboru
# najbardziej interesującego dodać obserwację wartości transakcji oraz ofert w czasie rzeczywistym.
# Jeśli któryś z obserwowanych zasobów jest oznaczony jako kandydat - obserwujemy wartości
# zawieranych na nim transackji.
# a) jeśli w ciągu Y ostatnich próbek wystąpiły na nim wahania większe niż X % - podpisujemy go
# dodatkowo jako zmienny ('volatile asset'). (1.5pkt)
# b) jeśli różnica między ofertami kupna / sprzedaży jest mniejsza niż S % (spread)
# oznaczamy go dodatkowo jako 'liquid asset' (charakteryzujący się płynnym rynkiem). (1.5pkt)

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from pathlib import Path
from PIL import Image
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

    storage_slice = askbid_storage[-window_size:]
    temp = []

    for curr_pair in range(3):
        inner_temp = []

        for ask_or_bid in range(2):
            upward, upward_counter = 0, 0
            downward, downward_counter = 0, 0

            for sample in range(1, len(storage_slice)):
                if storage_slice[sample-1][curr_pair][ask_or_bid] \
                        < storage_slice[sample][curr_pair][ask_or_bid]:

                    up = storage_slice[sample][curr_pair][ask_or_bid] \
                           - storage_slice[sample-1][curr_pair][ask_or_bid]
                    upward += up
                    upward_counter += 1

                elif storage_slice[sample-1][curr_pair][ask_or_bid] \
                        > storage_slice[sample][curr_pair][ask_or_bid]:

                    down = storage_slice[sample-1][curr_pair][ask_or_bid] \
                           - storage_slice[sample][curr_pair][ask_or_bid]
                    downward += down
                    downward_counter += 1

            if upward_counter == 0:
                a = 1
            else:
                a = upward / upward_counter

            if downward_counter == 0:
                b = 1
            else:
                b = downward / downward_counter

            try:
                rsi = 100 - (100 / (1 + (a / b)))
            except ZeroDivisionError:
                a, b = 1, 1
                rsi = 100 - (100 / (1 + (a / b)))
            inner_temp.append(rsi)

        temp.append(inner_temp)

    rsi_storage.append(temp)


def get_transparent_icons(*icon_names):

    processed_list = []
    for icon_name in icon_names:

        path = Path.cwd() / 'icons' / f'{icon_name}-256p.png'
        icon_image = Image.open(path)

        alpha_channel = icon_image.getchannel('A')
        with_alpha = alpha_channel.point(lambda i: 32 if i > 0 else 0)
        icon_image.putalpha(with_alpha)

        processed_list.append(icon_image)

    return processed_list


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

        axes = plt.gca()

        latest_ask_rsi = rsi_storage[-1][curr_pair][0]
        if latest_ask_rsi >= 70:
            icon = upward_icon
        elif latest_ask_rsi <= 30:
            icon = downward_icon
        else:
            icon = question_icon

        imagebox = OffsetImage(icon, zoom=0.4)
        imagebox.image.axes = axes
        ab = AnnotationBbox(imagebox, (0.5, 0.5), xycoords='axes fraction',
                            boxcoords="offset points", pad=0.3, frameon=0)
        axes.add_artist(ab)


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
        ax = plt.gca()
        ax.margins(y=0.2)
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

    downward_icon, upward_icon, question_icon = get_transparent_icons('downward', 'upward', 'question')

    animation = FuncAnimation(plt.figure(), draw_figure, interval=1000*FREQ)
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()