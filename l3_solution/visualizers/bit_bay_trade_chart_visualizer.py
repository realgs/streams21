import json

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from l3_solution.visualizers.wallet import Wallet, WalletItem


class BitbayTradeChartVisualizer:

    trade_buy = {'BTC': list(), 'LTC': list(), 'ETH': list()}
    trade_sell = {'BTC': list(), 'LTC': list(), 'ETH': list()}
    rsi_val = {'BTC': list(), 'LTC': list(), 'ETH': list()}
    wallets = {"BTC": Wallet(), "LTC": Wallet(), "ETH": Wallet()}
    plot_trade = {
        'BTC': {'BUY': None, 'SELL': None},
        'LTC': {'BUY': None, 'SELL': None},
        'ETH': {'BUY': None, 'SELL': None},
    }
    additional_plot = {'BTC': None, 'LTC': None, 'ETH': None}
    plot_trade_avg = {
        'BTC': {'BUY': None, 'SELL': None},
        'LTC': {'BUY': None, 'SELL': None},
        'ETH': {'BUY': None, 'SELL': None},
    }
    plot_customer_avg_buy = {
        'BTC': None,
        'LTC': None,
        'ETH': None,
    }
    plot_text = {
        'BTC': {
            "PROFIT": None,
            "CAND": None,
            "MARKET": None,
        },
        'LTC': {
            "PROFIT": None,
            "CAND": None,
            "MARKET": None,
        },
        'ETH': {
            "PROFIT": None,
            "CAND": None,
            "MARKET": None,
        },
    }
    fig, axs = None, None
    animation = None
    ax = None
    bit_bay_service = None

    # Config
    config = {"range": 20}
    shared_json = ""

    volume = {'BTC': list(), 'LTC': list(), 'ETH': list()}

    def visualize(self, bit_bay_service, shared_json):
        self.shared_json = shared_json
        self.bit_bay_service = bit_bay_service
        self.update_trades()
        self.plot_charts()

    def plot_charts(self):
        self.fig, self.axs = plt.subplots(6, 2, figsize=(25, 15))
        self.update_wallet()
        for i in range(len(self.trade_buy.keys())):

            # Prepare data
            crypto_name = list(self.trade_buy.keys())[i]
            price_buy = list(map(lambda price: price['price'], self.trade_buy[crypto_name]))[-20:]
            price_sell = list(map(lambda price: price['price'], self.trade_sell[crypto_name]))[-20:]
            range_avg = self.config["range"]
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

            # Plot buy avg
            avg_buy = self.wallets[crypto_name].avg_buy()
            if avg_buy is None:
                self.plot_customer_avg_buy[crypto_name], = self.axs[i * 2][0].plot(time, [sell_avg for i in range(len(time))], label='buy avg', color='r')
            else:
                self.plot_customer_avg_buy[crypto_name], = self.axs[i * 2][0].plot(time, [avg_buy for i in range(len(time))], label='buy avg', color='r')

            self.axs[i * 2][0].set(xlabel='time', ylabel='price', title=crypto_name + '/PLN')
            self.axs[i * 2][0].grid()
            self.fig.autofmt_xdate(rotation=40)
            self.axs[i * 2][0].legend()

            if avg_buy is None:
                self.plot_customer_avg_buy[crypto_name].set_visible(False)

            self.additional_plot[crypto_name], = self.axs[i * 2 - 1][0].plot(time, self.rsi_val[crypto_name])
            self.axs[i * 2 - 1][0].set(xlabel='time', ylabel='rsi')
            self.axs[i * 2 - 1][1].set_axis_off()

            self.axs[i * 2][1].set_axis_off()
            self.plot_text[crypto_name]["PROFIT"] = self.axs[i * 2][1].text(0, 0, 'Profit: ' + str(self.wallets[crypto_name].profit))
            self.plot_text[crypto_name]["WALLET"] = self.axs[i * 2][1].text(0, 1.0, '')

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
        self.update_wallet()
        for i in range(len(self.trade_buy.keys())):

            crypto_name = list(self.trade_buy.keys())[i]
            price_buy = list(map(lambda price: price['price'], self.trade_buy[crypto_name]))[-20:]
            price_sell = list(map(lambda price: price['price'], self.trade_sell[crypto_name]))[-20:]
            range_avg = self.config["range"]
            sell_avg = sum(price_sell[-1 * range_avg:]) / len(price_sell[-1 * range_avg:])
            buy_avg = sum(price_buy[-1 * range_avg:]) / len(price_buy[-1 * range_avg:])
            time = list(map(lambda price: price['time'], self.trade_sell[crypto_name]))[-20:]

            self.plot_trade[crypto_name]['BUY'].set_data(time, price_buy)
            self.plot_trade[crypto_name]['SELL'].set_data(time, price_sell)

            self.plot_trade_avg[crypto_name]['SELL'].set_data(self.get_avg_times(range_avg, time),
                                                              [sell_avg for i in range(len(time[-1 * range_avg:]))])
            self.plot_trade_avg[crypto_name]['BUY'].set_data(self.get_avg_times(range_avg, time),
                                                             [buy_avg for i in range(len(time[-1 * range_avg:]))])
            self.additional_plot[crypto_name].set_data(time, self.rsi_val[crypto_name][-20:])

            # Plot buy avg
            avg_buy = self.wallets[crypto_name].avg_buy()
            if avg_buy is None:
                self.plot_customer_avg_buy[crypto_name].set_data(time, [sell_avg for i in range(len(time))])
                self.plot_customer_avg_buy[crypto_name].set_visible(False)
            else:
                self.plot_customer_avg_buy[crypto_name].set_data(time, [avg_buy for i in range(len(time))])
                self.plot_customer_avg_buy[crypto_name].set_visible(True)

            self.plot_text[crypto_name]["PROFIT"].set_text('Profit: ' + str(self.wallets[crypto_name].profit))
            self.plot_text[crypto_name]["WALLET"].set_text(f'Wallet: {crypto_name}: {str(self.wallets[crypto_name].total_quantity())}')

            for ax in self.axs:
                ax[0].relim()
                ax[0].autoscale_view()
            self.fig.autofmt_xdate(rotation=40)

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

    def update_wallet(self):
        transactions = json.loads(self.shared_json.value)
        self.shared_json.value = """{"BTC": {"price": "0", "quantity": "0"}, "LTC": {"price": "0", "quantity": "0"}, "ETH": {"price": "0", "quantity": "0"}}"""
        if 'file' in transactions.keys():
            self.load_wallet_to_json(transactions['file'])
        else:
            for key in ["BTC", "ETH", "LTC"]:
                if transactions[key]["price"] == 'sell':
                    self.wallets[key].sell_crypto(
                            int(transactions[key]["quantity"]),
                            self.trade_sell[key][len(self.trade_sell[key]) - 1]['price'])
                else:
                    self.wallets[key].add_transaction(WalletItem(int(transactions[key]["quantity"]), int(transactions[key]["price"])))
            self.save_wallet_to_json()
        print(transactions)

    def save_wallet_to_json(self):
        f = open("backup_wallet.json", "w")
        json_dict = {}
        for key in self.wallets.keys():
            json_dict[key] = self.wallets[key].to_json_conventer()
        print(json_dict)
        f.write(json.dumps(json_dict))
        f.close()

    def load_wallet_to_json(self, file_name):
        f = open(file_name, "r")
        reconvery_json = json.load(f)
        f.close()
        for key in reconvery_json.keys():
            wallet = Wallet(profit=int(reconvery_json[key]["profit"]))
            [wallet.add_transaction(WalletItem(int(i['quantity']), int(i['price']))) for i in reconvery_json[key]["transactions"]]
            self.wallets[key] = wallet