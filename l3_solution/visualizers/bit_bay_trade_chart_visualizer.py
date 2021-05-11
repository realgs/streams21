import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class BitbayTradeChartVisualizer:
    fluctuations_X = 0.000001
    difference_S = 0.99999

    trade_buy = {
        'BTC': list(),
        'LTC': list(),
        'ETH': list(),
    }
    trade_sell = {
        'BTC': list(),
        'LTC': list(),
        'ETH': list(),
    }
    rsi_val = {
        'BTC': list(),
        'LTC': list(),
        'ETH': list(),
    }
    volume_val = {
        'BTC': list(),
        'LTC': list(),
        'ETH': list(),
    }
    plot_trade = {
        'BTC': {
            'BUY': None,
            'SELL': None,
        },
        'LTC': {
            'BUY': None,
            'SELL': None,
        },
        'ETH': {
            'BUY': None,
            'SELL': None,
        },
    }
    additional_plot = {
        'BTC': None,
        'LTC': None,
        'ETH': None,
    }
    plot_trade_avg = {
        'BTC': {
            'BUY': None,
            'SELL': None,
        },
        'LTC': {
            'BUY': None,
            'SELL': None,
        },
        'ETH': {
            'BUY': None,
            'SELL': None,
        },
    }
    plot_text = {
        'BTC': {
            "RSI": None,
            "CAND": None,
            "MARKET": None,
        },
        'LTC': {
            "RSI": None,
            "CAND": None,
            "MARKET": None,
        },
        'ETH': {
            "RSI": None,
            "CAND": None,
            "MARKET": None,
        },
    }
    fig, axs = None, None
    animation = None
    ax = None
    i = 1
    bit_bay_service = None

    # Config
    config = {
        "range": None,
        "is_volume_active": False
    }

    volume = {
        'BTC': list(),
        'LTC': list(),
        'ETH': list(),
    }

    def visualize(self, bit_bay_service):
        self.set_config()
        self.bit_bay_service = bit_bay_service
        self.update_trades()
        self.plot_charts()

    def plot_charts(self):
        self.fig, self.axs = plt.subplots(6, 2, figsize=(25, 15))

        for i in range(len(self.trade_buy.keys())):

            # Prepare data
            crypto_name = list(self.trade_buy.keys())[i]
            price_buy = list(map(lambda price: price['price'], self.trade_buy[crypto_name]))[-20:]
            price_sell = list(map(lambda price: price['price'], self.trade_sell[crypto_name]))[-20:]
            range_avg = int(self.config["range"])
            sell_avg = sum(price_sell[-1 * range_avg:]) / len(price_sell[-1 * range_avg:])
            buy_avg = sum(price_buy[-1 * range_avg:]) / len(price_buy[-1 * range_avg:])
            time = list(map(lambda price: price['time'], self.trade_sell[crypto_name]))[-20:]

            # Plot trades
            self.plot_trade[crypto_name]['BUY'], = self.axs[i * 2][0].plot(time, price_buy, label='buy')
            self.plot_trade[crypto_name]['SELL'], = self.axs[i * 2][0].plot(time, price_sell, label='sell')

            # Plot avg
            self.plot_trade_avg[crypto_name]['SELL'], = self.axs[i * 2][0].plot(
                self.get_avg_times(range_avg, time),
                [sell_avg for i in range(len(time[-1 * range_avg:]))], color='g',
                label='avg sell')
            self.plot_trade_avg[crypto_name]['BUY'], = self.axs[i * 2][0].plot(
                self.get_avg_times(range_avg, time),
                [buy_avg for i in range(len(time[-1 * range_avg:]))], color='y',
                label='avg buy')

            self.axs[i * 2][0].set(xlabel='time', ylabel='price', title=crypto_name + '/PLN')
            self.axs[i * 2][0].grid()
            self.fig.autofmt_xdate(rotation=40)
            self.axs[i * 2][0].legend()

            if self.config["is_volume_active"]:
                self.additional_plot[crypto_name], = self.axs[i * 2 - 1][0].bar(time, self.volume_val[crypto_name],
                                                                                color='r', width=0.2)
                self.axs[i * 2 - 1][0].set(xlabel='time', ylabel='volume', title='volume transaction')
            else:
                self.additional_plot[crypto_name], = self.axs[i * 2 - 1][0].plot(time, self.rsi_val[crypto_name])
                self.axs[i * 2 - 1][0].set(xlabel='time', ylabel='rsi',
                                           title='volume transaction')
            self.axs[i * 2 - 1][1].set_axis_off()

            self.axs[i * 2][1].set_axis_off()
            self.plot_text[crypto_name]["RSI"] = self.axs[i * 2][1].text(0, 0, self.get_trend_by_rsi(crypto_name))
            self.plot_text[crypto_name]["CAND"] = self.axs[i * 2][1].text(0, 0.5, '')
            self.plot_text[crypto_name]["MARKET"] = self.axs[i * 2][1].text(0, 1.0, '')

            if self.get_candidate() == crypto_name:
                self.plot_text[crypto_name]["CAND"].set_text('Kandydat')
                informations = ''
                if self.volatile_asset(crypto_name):
                    informations += 'volatile asset '
                if self.liquid_asset(crypto_name):
                    informations += 'liquid asset'
                self.plot_text[crypto_name]["MARKET"].set_text(informations)
            else:
                self.plot_text[crypto_name]["CAND"].set_text('')
                self.plot_text[crypto_name]["MARKET"].set_text('')

        # Set shared indexes
        for i in [i[0] for i in self.axs]:
            self.axs[0][0].get_shared_x_axes().join(i)

        self.animation = FuncAnimation(self.fig, self.update_plot, fargs=(self,), interval=5000)
        plt.show()

    def get_avg_times(self, range_avg, time):
        avg_times = time[-1 * range_avg:]
        avg_times.reverse()
        return avg_times

    def update_plot(self, *args):
        self.update_trades()

        for i in range(len(self.trade_buy.keys())):

            crypto_name = list(self.trade_buy.keys())[i]
            price_buy = list(map(lambda price: price['price'], self.trade_buy[crypto_name]))[-20:]
            price_sell = list(map(lambda price: price['price'], self.trade_sell[crypto_name]))[-20:]
            range_avg = int(self.config["range"])
            sell_avg = sum(price_sell[-1 * range_avg:]) / len(price_sell[-1 * range_avg:])
            buy_avg = sum(price_buy[-1 * range_avg:]) / len(price_buy[-1 * range_avg:])
            time = list(map(lambda price: price['time'], self.trade_sell[crypto_name]))[-20:]

            self.plot_trade[crypto_name]['BUY'].set_data(time, price_buy)
            self.plot_trade[crypto_name]['SELL'].set_data(time, price_sell)

            self.plot_trade_avg[crypto_name]['SELL'].set_data(self.get_avg_times(range_avg, time),
                                                              [sell_avg for i in range(len(time[-1 * range_avg:]))])
            self.plot_trade_avg[crypto_name]['BUY'].set_data(self.get_avg_times(range_avg, time),
                                                             [buy_avg for i in range(len(time[-1 * range_avg:]))])

            if self.config["is_volume_active"]:
                self.axs[i * 2 - 1][0].bar(time, self.volume_val[crypto_name][-20:], color='r', width=0.2)
            else:
                self.additional_plot[crypto_name], = self.axs[i * 2 - 1][0].plot(time, self.rsi_val[crypto_name][-20:])

            self.plot_text[crypto_name]["RSI"].set_text(self.get_trend_by_rsi(crypto_name))
            if self.get_candidate() == crypto_name:
                self.plot_text[crypto_name]["CAND"].set_text('Kandydat')
                informations = ''
                if self.volatile_asset(crypto_name):
                    informations += 'volatile asset '
                if self.liquid_asset(crypto_name):
                    informations += 'liquid asset'
                self.plot_text[crypto_name]["MARKET"].set_text(informations)
            else:
                self.plot_text[crypto_name]["CAND"].set_text('')
                self.plot_text[crypto_name]["MARKET"].set_text('')

            for ax in self.axs:
                ax[0].relim()
                ax[0].autoscale_view()
            self.fig.autofmt_xdate(rotation=40)

    def set_config(self):
        choice = str(input('Wolumen czy rsi? [w]/[r]: '))
        if choice == 'w':
            self.config["is_volume_active"] = True
        else:
            self.config["is_volume_active"] = False
        self.config["range"] = int(input('Ile punktów chcesz liczyć? [int] (max 20) : '))
        if self.config["range"] > 20:
            self.config["range"] = 20

    def rsi(self, price):
        price = price[-1 * self.config["range"]:]
        price.reverse()
        uppers = []
        downers = []
        for i in range(1, len(price)):
            if price[i - 1] < price[i]:
                uppers.append(price[i] - price[i - 1])
            elif price[i - 1] > price[i]:
                downers.append(price[i - 1] - price[i])

        if len(uppers) == 0:
            a = 1
        else:
            a = sum(uppers) / len(uppers)
        if len(downers) == 0:
            b = 1
        else:
            b = sum(downers) / len(downers)
        return 100 - (100 / (1 + (a / b)))

    def update_trades(self):
        self.bit_bay_service.update_crypto_trades()
        self.bit_bay_service.update_crypto_volume()
        self.trade_sell = self.bit_bay_service.get_trades_buy()
        self.trade_buy = self.bit_bay_service.get_trades_sell()
        self.volume_val = self.bit_bay_service.get_volume()
        for crypto_name in self.bit_bay_service.CRYPTO_CURRENCIES:
            self.rsi_val[crypto_name].append(self.rsi([i["price"] for i in self.trade_buy[crypto_name]]))

    def get_trend_by_rsi(self, crypto_currency):
        rsi = self.rsi_val[crypto_currency][len(self.rsi_val[crypto_currency]) - 1]
        if rsi == 100:
            return 'RSI: increased likelihood of a reversal to a downward trend'
        elif rsi >= 70:
            return 'RSI: sell signal'
        elif rsi == 0:
            return 'RSI: increases the likelihood of a trend reversal to an upward trend'
        elif rsi <= 30:
            return 'RSI: buy signal'
        else:
            return 'RSI: Nic nie rób'

    def get_candidate(self):
        candidate = [
            (i,
             self.rsi_val[i][len(self.rsi_val[i]) - 1],
             self.volume_val[i][len(self.volume_val[i]) - 1]
             ) for i in self.bit_bay_service.CRYPTO_CURRENCIES]

        candidate = list(filter(lambda cand: cand[1] <= 30, candidate))
        for i in candidate:
            if max([i[2] for i in candidate]) == i[2]:
                return i[0]

    def volatile_asset(self, crypto_name):
        buy_min = min([i['price'] for i in self.trade_buy[crypto_name][-1 * self.config["range"]:]])
        buy_max = max([i['price'] for i in self.trade_buy[crypto_name][-1 * self.config["range"]:]])
        return (1 - (buy_min / buy_max)) > self.fluctuations_X

    def liquid_asset(self, crypto_name):
        sell = sum([i['price'] for i in self.trade_sell[crypto_name][-1 * self.config["range"]:]])
        buy = sum([i['price'] for i in self.trade_buy[crypto_name][-1 * self.config["range"]:]])
        if sell > buy:
            return 1 - (buy / sell) < self.difference_S
        else:
            return 1 - (sell / buy) < self.difference_S
