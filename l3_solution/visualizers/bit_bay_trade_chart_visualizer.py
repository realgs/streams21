import datetime

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class BitbayTradeChartVisualizer:
    trade_buy = {
        'BTC': list(),
        'LTC': list(),
        'DASH': list(),
    }
    trade_sell = {
        'BTC': list(),
        'LTC': list(),
        'DASH': list(),
    }
    plot_trade_buy = {
        'BTC': {
            'BUY': None,
            'SELL': None,
        },
        'LTC': {
            'BUY': None,
            'SELL': None,
        },
        'DASH': {
            'BUY': None,
            'SELL': None,
        },
    }
    plot_trade_sell = {
        'BTC': {
            'BUY': None,
            'SELL': None,
        },
        'LTC': {
            'BUY': None,
            'SELL': None,
        },
        'DASH': {
            'BUY': None,
            'SELL': None,
        },
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
        'DASH': {
            'BUY': None,
            'SELL': None,
        },
    }
    is_visualized = False
    fig, axs = None, None

    # Config
    config = {
        "range_elements": None,
        "range_rsi": None
    }

    volume = {
        'BTC': None,
        'LTC': None,
        'DASH': None,
    }

    def update_crypto_values(self, buy_crypto_trades, sell_crypto_trades):
        for crypto in buy_crypto_trades.keys():
            self.trade_buy[crypto].extend(buy_crypto_trades[crypto])
        for crypto in sell_crypto_trades.keys():
            self.trade_sell[crypto].extend(sell_crypto_trades[crypto])

    def visualize(self, buy_crypto_trades, sell_crypto_trades, volume):
        self.set_config()
        self.volume = volume
        self.update_crypto_values(buy_crypto_trades, sell_crypto_trades)
        self.plot_charts()

    ax = None
    i = 1

    def plot_charts(self):
        if self.is_visualized:
            self.update_plot()
        else:
            self.first_plot()

    def first_plot(self):
        plt.ion()
        self.fig, self.axs = plt.subplots(3, 1)

        for i in range(len(self.trade_buy.keys())):
            crypto_name = list(self.trade_buy.keys())[i]
            buy = self.trade_buy[crypto_name][-1 * 20:]
            sell = self.trade_sell[crypto_name][-1 * 20:]

            price_buy = list(map(lambda price: price['price'], buy))
            price_sell = list(map(lambda price: price['price'], sell))

            self.plot_trade_buy[crypto_name]['BUY'], = self.axs[i].plot(
                list(map(lambda data: datetime.datetime.fromtimestamp(data['date']), buy)),
                price_buy, label='buy')
            self.plot_trade_buy[crypto_name]['SELL'], = self.axs[i].plot(
                list(map(lambda data: datetime.datetime.fromtimestamp(data['date']), sell)),
                list(price_sell), label='sell')

            sell_avg = sum(price_sell[-1 * self.config["range_elements"]:]) / self.config["range_elements"]
            self.plot_trade_avg[crypto_name]['SELL'] = self.axs[i].axhline(y=sell_avg, label='avg sell', color='r')

            buy_avg = sum(price_buy[-1 * self.config["range_elements"]:]) / self.config["range_elements"]
            self.plot_trade_avg[crypto_name]['BUY'] = self.axs[i].axhline(y=buy_avg, label='avg buy', color='g')

            self.axs[i].set(xlabel='time', ylabel='price',
                            title=crypto_name)

            self.axs[i].grid()
            extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
            extra2 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
            extra3 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)

            self.axs[i].legend([
                extra,
                extra2,
                extra3,
                self.plot_trade_buy[crypto_name]['BUY'],
                self.plot_trade_buy[crypto_name]['SELL'],
                self.plot_trade_avg[crypto_name]['SELL'],
                self.plot_trade_avg[crypto_name]['BUY']],
                [
                    'Trans volume (Last 24h) = ' + str(self.volume[crypto_name]),
                    'RSI buy = ' + str(self.rsi(price_buy)),
                    'RSI sell = ' + str(self.rsi(price_sell)),
                    'buy', 'sell', 'avg sell', 'avg buy'
                ]
            )
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.is_visualized = True

    def update_plot(self):

        for i in range(len(self.trade_buy.keys())):
            crypto_name = list(self.trade_buy.keys())[i]
            buy = self.trade_buy[crypto_name]
            sell = self.trade_sell[crypto_name]

            price_buy = sorted(list(map(lambda price: price['price'], buy)))
            price_sell = sorted(list(map(lambda price: price['price'], sell)))

            self.plot_trade_buy[crypto_name]['BUY'].set_ydata(price_buy)

            self.plot_trade_buy[crypto_name]['BUY'].set_xdata(
                sorted(list(map(lambda data: datetime.datetime.fromtimestamp(data['date']), buy))))

            self.plot_trade_buy[crypto_name]['SELL'].set_ydata(price_sell)
            self.plot_trade_buy[crypto_name]['SELL'].set_xdata(
                sorted(list(map(lambda data: datetime.datetime.fromtimestamp(data['date']), sell))))

            sell_avg = sum(price_sell[-1 * self.config["range_elements"]:]) / self.config["range_elements"]
            self.plot_trade_avg[crypto_name]['SELL'].set_ydata(sell_avg)

            buy_avg = sum(price_buy[-1 * self.config["range_elements"]:]) / self.config["range_elements"]
            self.plot_trade_avg[crypto_name]['BUY'].set_ydata(buy_avg)

            self.axs[i].grid()
            extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
            extra2 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
            extra3 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)

            self.axs[i].legend([
                extra,
                extra2,
                extra3,
                self.plot_trade_buy[crypto_name]['BUY'],
                self.plot_trade_buy[crypto_name]['SELL'],
                self.plot_trade_avg[crypto_name]['SELL'],
                self.plot_trade_avg[crypto_name]['BUY']],
                [
                    'Trans volume (Last 24h) = ' + str(self.volume[crypto_name]),
                    'RSI buy = ' + str(self.rsi(price_buy)),
                    'RSI sell = ' + str(self.rsi(price_sell)),
                    'buy', 'sell', 'avg sell', 'avg buy'
                ]
            )

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def set_config(self):
        if self.config["range_elements"] is None or self.config["range_rsi"] is None:
            self.config["range_elements"] = int(input('Podaj ilość ostatnich elementów do obliczenia średniej: '))
            self.config["range_rsi"] = int(input('Podaj przedział oscylatora RSI: '))

    def rsi(self, price):
        price = price[-1 * self.config["range_rsi"]:]
        ups = 0
        up_count = 0
        downs = 0
        down_count = 0
        for i in range(1, len(price)):
            if price[i - 1] < price[i]:
                up = price[i] - price[i - 1]
                ups += up
                up_count += 1
            elif price[i - 1] > price[i]:
                down = price[i - 1] - price[i]
                downs += down
                down_count += 1

        if up_count == 0:
            a = 1
        else:
            a = ups / up_count
        if down_count == 0:
            b = 1
        else:
            b = downs / down_count
        return 100 - (100 / (1 + (a / b)))
