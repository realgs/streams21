import time as timelib

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class BitbayTradeChartVisualizer:
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
        self.trade_sell = self.bit_bay_service.get_trades_buy()
        self.trade_buy = self.bit_bay_service.get_trades_sell()
        self.plot_charts()

    def plot_charts(self):
        self.fig, self.axs = plt.subplots(6, 1, sharex=True, figsize=(25, 15))

        for i in range(len(self.trade_buy.keys())):
            crypto_name = list(self.trade_buy.keys())[i]

            price_buy = list(map(lambda price: price['price'], self.trade_buy[crypto_name]))[-20:]
            price_sell = list(map(lambda price: price['price'], self.trade_sell[crypto_name]))[-20:]
            range_avg = int(self.config["range"])
            sell_avg = sum(price_sell[-1 * range_avg:]) / len(price_sell[-1 * range_avg:])
            buy_avg = sum(price_buy[-1 * range_avg:]) / len(price_buy[-1 * range_avg:])
            time = list(map(lambda price: price['time'], self.trade_sell[crypto_name]))[-20:]

            self.plot_trade[crypto_name]['BUY'], = self.axs[i * 2].plot(time, price_buy, label='buy')
            self.plot_trade[crypto_name]['SELL'], = self.axs[i * 2].plot(time, price_sell, label='sell')

            self.plot_trade_avg[crypto_name]['SELL'], = self.axs[i * 2].plot(
                self.get_avg_times(range_avg, time),
                [sell_avg for i in range(len(time[-1 * range_avg:]))], color='g',
                label='avg sell')
            self.plot_trade_avg[crypto_name]['BUY'], = self.axs[i * 2].plot(
                self.get_avg_times(range_avg, time),
                [buy_avg for i in range(len(time[-1 * range_avg:]))], color='y',
                label='avg buy')

            self.axs[i * 2].set(xlabel='time', ylabel='price',
                                title=crypto_name + '/PLN')
            self.axs[i * 2].grid()
            self.fig.autofmt_xdate(rotation=40)

            self.axs[i * 2].legend()

            if self.config["is_volume_active"]:
                self.volume_val[crypto_name].append(self.bit_bay_service.get_volume(crypto_name, 'PLN', 600000))
                self.additional_plot[crypto_name], = self.axs[i * 2 - 1].bar(time, self.volume_val[crypto_name], color='r', width=0.2)
                self.axs[i * 2 - 1].set(xlabel='time', ylabel='volume',
                                    title='volume transaction')
            else:
                self.rsi_val[crypto_name].append(self.rsi(price_buy))
                self.additional_plot[crypto_name], = self.axs[i * 2 - 1].plot(time, self.rsi_val[crypto_name])
                self.axs[i * 2 - 1].set(xlabel='time', ylabel='rsi',
                                        title='volume transaction')

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

            self.volume_val[crypto_name].append(self.bit_bay_service.get_volume(crypto_name, 'PLN', 600000))

            if self.config["is_volume_active"]:
                self.axs[i * 2 - 1].bar(time, self.volume_val[crypto_name], color='r', width=0.2)
            else:
                self.rsi_val[crypto_name].append(self.rsi(price_buy))
                self.additional_plot[crypto_name], = self.axs[i * 2 - 1].plot(time, self.rsi_val[crypto_name])

            for ax in self.axs:
                ax.relim()
                ax.autoscale_view()
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
        upers = []
        downers = []
        for i in range(1, len(price)):
            if price[i - 1] < price[i]:
                upers.append(price[i] - price[i - 1])
            elif price[i - 1] > price[i]:
                downers.append(price[i - 1] - price[i])

        if len(upers) == 0:
            a = 1
        else:
            a = sum(upers) / len(upers)
        if len(downers) == 0:
            b = 1
        else:
            b = sum(downers) / len(downers)
        return 100 - (100 / (1 + (a / b)))

    def update_trades(self):
        self.bit_bay_service.update_crypto_trades()
        self.trade_sell = self.bit_bay_service.get_trades_buy()
        self.trade_buy = self.bit_bay_service.get_trades_sell()
