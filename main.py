# 1. Dajemy możliwość naniesienia na wykres punktu odniesienia - ceny kupna zasobów.
# - Wykres jest odświeżany w czasie rzeczywistym i reprezentuje strumienie danych dotyczące
#   trzech zasobów giełdowych, jak w poprzedniej liście.
# - Podczas działania programu użytkownik ma mieć możliwość wielokrotnego wprowadzenia
#   informacji co, w jakiej ilości i za ile kupił. Może to robić w odstępach czasowych
#   i dla różnych zasobów, w nieokreślonej kolejności.
# - Na podstawie wprowadzonych przez użytkownika danych wyliczamy dotychczasową średnią zakupu
#   danego waloru i nanosimy poziomą, przerywaną linią na wykres wartości zasobu.
# - Zwrócić uwagę na zakresy wartości na osi y, wszystko ma się mieścić w zakresie wartości.

# 2. Dodajemy możliwość wprowadzenia sprzedaży zasobów analogicznie do kupna.
# - Po sprzedaży aktualizujemy obecną średnią cenę zakupu (nie uwzględniającą już tych jednostek,
#   które zostały sprzedane. Zasada FIFO - first in first out)
#   przykład: jeśli kupiliśmy 10 jednostek po 4000$, następnie 20 jednostek po 6000$, a na końcu
#   20 jednostek po 10000$, a następnie sprzedaliśmy 10 jednostek za 50000$ to nasz zysk wynosi
#   460000$ a obecna średnia cena zakupu to 8000$.
# - Przy sprzedaży obliczamy osiągnięty zysk/stratę i nanosimy informację o zysku/stracie
#   w okolicy wykresu danego zasobu.

# 3. Program ma umożliwiać zapis (i odczyt) wprowadzonych danych w formacie .json
#    tak, by po ponownym uruchomieniu można było wprowadzić nazwę pliku przechowującego dane
#    i nie gromadzić danych od nowa.

from utils import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
import time


time_samples, data_storage, avg_storage, rsi_storage, vol_storage, askbid_storage, trans_storage \
    = ([] for _ in range(7))


def get_data(crypto_pairs, data_storage, askbid_storage):

    curr_temp, askbid_temp = ([] for _ in range(2))

    for pair in crypto_pairs:
        try:
            request_orders = requests.get(
                f"https://bitbay.net/API/Public/{pair[0]}{pair[1]}/ticker.json"
            )
            orders = request_orders.json()
            curr_temp.append([f'{pair[0]}-{pair[1]}', (orders['ask'], orders['bid'])])
            askbid_temp.append((orders['ask'], orders['bid']))

        except requests.exceptions.RequestException:
            print("Connection problem with the ticker API.")
            return None

    askbid_storage.append(askbid_temp)
    data_storage.append(curr_temp)


def get_transactions(crypto_pairs, transaction_storage, limit, timeframe):

    trans_temp = []

    for pair in crypto_pairs:

        unix_epoch_time = get_unix_time(timeframe)

        try:
            request_volume = requests.get(
                f"https://api.bitbay.net/rest/trading/transactions/{pair[0]}-{pair[1]}",
                params={'limit': limit, 'fromTime': unix_epoch_time}
            )
            transactions = request_volume.json()
            trans_temp.append(transactions)

        except requests.exceptions.RequestException:
            print("Connection problem with the transactions API.")
            trans_temp.append(None)

    transaction_storage.append(trans_temp)


def get_volume(transaction_storage, volume_storage):

    vol_temp = []

    for curr_pair in range(3):
        latest_trans = transaction_storage[-1][curr_pair]
        trans_amount = len(latest_trans['items'])
        volume = sum([float(latest_trans['items'][tran]['a']) for tran in range(trans_amount)])
        vol_temp.append(volume)

    volume_storage.append(vol_temp)


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


def classify_trend(rsi_storage, trend_list):

    for curr_pair in range(3):

        latest_ask_rsi = rsi_storage[-1][curr_pair][0]
        if latest_ask_rsi >= 65:
            trend_list[curr_pair] = 'upward'
        elif latest_ask_rsi <= 35:
            trend_list[curr_pair] = 'downward'
        else:
            trend_list[curr_pair] = 'horizontal'


def select_candidate(trends_list, volume_slice):

    temp = []
    for curr_pair in range(3):

        if trends_list[curr_pair] != 'downward':
            temp.append(volume_slice[curr_pair])

    if temp:
        highest_volume = max(temp)
        return volume_slice.index(highest_volume)
    else:
        return None


def check_volatility(transaction_storage, pair, threshold, samples):

    trans_slice = transaction_storage[-samples:]
    temp = []
    for sample in range(len(trans_slice)):
        curr_trans = trans_slice[sample][pair]
        trans_amount = len(curr_trans['items'])
        inner_temp = [float(curr_trans['items'][tran]['r']) for tran in range(trans_amount)]
        temp.extend(inner_temp)

    try:
        percentage = calculate_percent_diff(max(temp), min(temp))
    except ValueError:
        percentage = 0

    return (lambda perc: True if perc > threshold else False)(percentage)


def check_liquidity(transaction_storage, pair, threshold):

    trans_slice = transaction_storage[-1:]
    curr_trans = trans_slice[0][pair]
    trans_amount = len(curr_trans['items'])

    temp_asks = [float(curr_trans['items'][tran]['r']) for tran in range(trans_amount)
                 if curr_trans['items'][tran]['ty'] == "Buy"]
    temp_bids = [float(curr_trans['items'][tran]['r']) for tran in range(trans_amount)
                 if curr_trans['items'][tran]['ty'] == "Sell"]

    try:
        ask = sum(temp_asks) / len(temp_asks)
    except ZeroDivisionError:
        return 0

    try:
        bid = sum(temp_bids) / len(temp_bids)
    except ZeroDivisionError:
        return 0

    try:
        percentage = calculate_percent_diff(ask, bid)
    except ValueError:
        percentage = 0

    return (lambda spread: True if spread < threshold else False)(percentage)


def draw_figure(frame_number):

    plt.style.use('Solarize_Light2')
    time_samples.append(time.strftime("%H:%M:%S", time.localtime()))

    get_data(PAIRS, data_storage, askbid_storage)
    get_transactions(PAIRS, trans_storage, limit=30, timeframe=15)
    get_volume(trans_storage, vol_storage)
    calculate_mov_avg(askbid_storage, avg_storage, AVG_WINDOW)
    calculate_rsi(askbid_storage, rsi_storage, RSI_WINDOW)

    trends_of_pairs = ['']*3
    classify_trend(rsi_storage, trends_of_pairs)
    candidate = select_candidate(trends_of_pairs, vol_storage[-1])

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
        plt.plot(time_samples, avg_asks, "o:", color="#185986",
                 label=data_storage[0][curr_pair][0] + " ask mov avg")
        plt.plot(time_samples, avg_bids, "o:", color="#1b6762",
                 label=data_storage[0][curr_pair][0] + " bid mov avg")

        axes = plt.gca()

        icon_trend = (lambda trend: upward_icon if trend == 'upward'
                      else (downward_icon if trend == 'downward'
                            else question_icon))(trends_of_pairs[curr_pair])
        imagebox_trend = OffsetImage(icon_trend, zoom=0.4)
        imagebox_trend.image.axes = axes
        ab_trend = AnnotationBbox(imagebox_trend, (0.5, 0.5), xycoords='axes fraction',
                                  boxcoords="offset points", pad=0.3, frameon=0)
        axes.add_artist(ab_trend)

        volatile_test = check_volatility(trans_storage, curr_pair, VOLATILE_PERC, VOLATILE_SAMPLES)
        vol_icon = (lambda test: volatile_icon if test else tp_volatile_icon)(volatile_test)
        imagebox_volatile = OffsetImage(vol_icon, zoom=0.1)
        imagebox_volatile.image.axes = axes
        ab_volatile = AnnotationBbox(imagebox_volatile, (0.95, 1.4), xycoords='axes fraction',
                                     boxcoords="offset points", pad=0, frameon=0,
                                     annotation_clip=False)
        axes.add_artist(ab_volatile)

        liquid_test = check_liquidity(trans_storage, curr_pair, SPREAD_PERC)
        liq_icon = (lambda test: liquid_icon if test else tp_liquid_icon)(liquid_test)
        imagebox_liquid = OffsetImage(liq_icon, zoom=0.1)
        imagebox_liquid.image.axes = axes
        ab_liquid = AnnotationBbox(imagebox_liquid, (0.9, 1.4), xycoords='axes fraction',
                                   boxcoords="offset points", pad=0, frameon=0,
                                   annotation_clip=False)
        axes.add_artist(ab_liquid)

        if candidate == curr_pair:
            for loc, spine in axes.spines.items():
                if loc == 'bottom' or loc == 'top':
                    spine.set_position(("outward", 1))
                    spine.set_capstyle('butt')
                else:
                    spine.set_position(("outward", -1))
                spine.set_linewidth(3)
                # spine.set_edgecolor('#859900')
                spine.set_edgecolor('#ffae1a')
                # spine.set_edgecolor('#ff751a')
                spine.set_alpha(0.7)

        # nanosimy poziomą, przerywaną linią
        # global counter
        # counter += 1
        # if counter >= 4 and counter < 10:
        #     axes.axhline(y=999, color='r', linestyle='dashed')
        # elif counter >= 10 and counter < 15:
        #     axes.axhline(y=99, color='r', linestyle='dashed')
        # else:
        #     axes.axhline(y=999, color='r', linestyle='dashed')

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

        for vol_sample in vol_storage:
            volume.append(vol_sample[curr_pair])

        plt.bar(time_samples, volume, align="center")
        plt.xlabel("Time", fontsize=9)
        plt.ylabel("Volume", fontsize=9)
        ax = plt.gca()
        ax.margins(y=0.2)
        plt.xticks(rotation='vertical', fontsize=7)

    clear_older_data(data_storage, avg_storage, vol_storage, askbid_storage, rsi_storage,
                     trans_storage, trigger_list=time_samples, treshold=10)

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)


if __name__ == '__main__':

    PAIRS = [('LTC', 'PLN'), ('ETH', 'PLN'), ('BCC', 'PLN')]
    FREQ = 5
    # AVG_WINDOW = int(input('Przedział z jakiego liczyć średnią (max 10): '))
    # RSI_WINDOW = int(input('Przedział z jakiego liczyć wskaźnik RSI? (max 10): '))
    # VOLATILE_SAMPLES = int(input('Przedział z jakiego badać zmienność zasobu? (max 10): '))
    # VOLATILE_PERC = float(input('Procentowy próg do uznania zasobu za zmienny? (%): '))
    # SPREAD_PERC = float(input('Maksymalny procent spreadu do uznania zasobu za charakteryzujący '
    #                           'się płynnym rynkiem? (%): '))
    AVG_WINDOW = 5
    RSI_WINDOW = 10
    VOLATILE_SAMPLES = 5
    VOLATILE_PERC = 5
    SPREAD_PERC = 2.85

    counter = 0

    downward_icon, upward_icon, question_icon, tp_volatile_icon, tp_liquid_icon \
        = get_icons('downward', 'upward', 'question', 'fire', 'liquidity')
    volatile_icon, liquid_icon = get_icons('fire', 'liquidity', transparent=False)

    animation = FuncAnimation(plt.figure(), draw_figure, interval=1000*FREQ)
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()
