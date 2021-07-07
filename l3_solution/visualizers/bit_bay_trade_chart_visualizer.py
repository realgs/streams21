import datetime

import matplotlib.pyplot as plt


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
    is_visualized = False
    fig, axs = None, None

    def update_crypto_values(self, buy_crypto_trades, sell_crypto_trades):
        for crypto in buy_crypto_trades.keys():
            self.trade_buy[crypto].extend(buy_crypto_trades[crypto])
        for crypto in sell_crypto_trades.keys():
            self.trade_sell[crypto].extend(sell_crypto_trades[crypto])

    def visualize(self, buy_crypto_trades, sell_crypto_trades):
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
            buy = self.trade_buy[crypto_name]
            sell = self.trade_sell[crypto_name]

            price_buy = list(map(lambda price: price['price'], buy))
            price_sell = map(lambda price: price['price'], sell)
            self.plot_trade_buy[crypto_name]['BUY'], = self.axs[i].plot(
                list(map(lambda data: datetime.datetime.fromtimestamp(data['date']), buy)),
                price_buy, label='buy')
            self.plot_trade_buy[crypto_name]['SELL'], = self.axs[i].plot(
                list(map(lambda data: datetime.datetime.fromtimestamp(data['date']), sell)),
                list(price_sell), label='sell')

            self.axs[i].set(xlabel='time', ylabel='price',
                            title=crypto_name)
            self.axs[i].grid()
            self.axs[i].legend()
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

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
