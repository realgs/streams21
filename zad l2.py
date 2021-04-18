from requests import get
import matplotlib.pyplot as plt


def request_crypto(crypt, template):
    try:
        request = template[0] + crypt + template[1]
        resp = get(request)
        status = str(resp.status_code)
        assert status[0] == '2', "wrong status: " + status
        resp_dict = eval(resp.text)
        sell = resp_dict['ask']
        buy = resp_dict['bid']
        ratio_value = (1 - (sell - buy) / buy) * 100
        return sell, buy, ratio_value
    except KeyError:
        print(resp_dict['message'])


def update_data(data_storage, data, name, attrs):
    attr_num = len(attrs)
    for i in range(attr_num):
        attr = attrs[i]
        data_storage[name][attr].append(data[i])


def visualise(stop_interval, data_storage, names, attrs, axes, t, colors_storage, template):
    crypto_num = len(names)
    attr_num = len(attrs)
    possible_to_plot = False
    t_val = t[-1]
    for i in range(crypto_num):
        crypto = names[i]
        crypto_data = request_crypto(crypto, template)
        update_data(data_storage, crypto_data, crypto, attrs)
        print(f'{crypto} data at time: {t_val}s:')
        for j in range(attr_num - 1):
            attr = attrs[j]
            print(f'{attr}: {crypto_data[j]}')
            attr_data = crypt_values[crypto][attr]
            if len(attr_data) >= 2:
                possible_to_plot = True
                axes[i].plot(t, attr_data, color=colors_storage[attr], label=attr)
        print(f'{attrs[-1]}: {crypto_data[-1]}')
        last_attr_data = crypt_values[crypto][attrs[-1]]
        last_attr_data_len = len(last_attr_data)
        if last_attr_data_len >= 2:
            axes[-1].plot(t, last_attr_data, color=colors_storage[crypto], label=f'{crypto}')
        axes[i].set_title(crypto)
        axes[i].set_xlabel('time')
        axes[i].set_ylabel('value')
        if possible_to_plot:
            axes[i].legend()
            axes[i].set_xlim(xmin=0, xmax=t_val)
    if last_attr_data_len >= 2:
        axes[-1].set_xlim(xmin=0, xmax=t_val)
        axes[-1].legend()
    axes[-1].set_title('buy/sell ratio')
    axes[-1].set_xlabel('time')
    axes[-1].set_ylabel('value')

    plt.draw()
    if len(t) >= 2:
        plt.pause(stop_interval)
    ax_num = len(ax)
    for i in range(ax_num):
        ax[i].cla()


cryptos = ['BTC', 'LTC', 'ETH']
attributes = ['sell', 'buy', 'ratio']
colors = {'sell': 'r', 'buy': 'g', 'BTC': 'brown', 'LTC': 'orange', 'ETH': 'b'}
crypt_values = {'BTC': {'buy': [], 'sell': [], 'ratio': []},
                'LTC': {'buy': [], 'sell': [], 'ratio': []},
                'ETH': {'buy': [], 'sell': [], 'ratio': []}}
req_temp = ('https://bitbay.net/API/Public/', '/ticker.json')
time_values = []
plt.ion()
time_val = 0
actualisation_interval = 5

fig, ax = plt.subplots(4, 1, figsize=(10, 8), constrained_layout=True)
while True:
    fig.suptitle('Cryptocurrencies Data')
    time_values.append(time_val * 5)
    visualise(actualisation_interval, crypt_values, cryptos, attributes, ax, time_values, colors, req_temp)
    time_val += 1
