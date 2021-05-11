# Wykresy trzech zasobów z poprzedniego zadania wyświetlać na trzech osobnych wykresach
#
# - na wykresie lub pod wykresem dodać wolumen transakcji
#
# - oprócz linii wartości osiąganych przez zasób dodać innym kolorem średnią  ruchomą
# z wybranego przedziału próbek. Przedział do ustalenia przez użytkownika, można ograniczyć zakres.
#
# - dodać oscylator RSI (relative strength index / wskaźnik siły względnej) Przedział y do ustalenia
# przez użytkownika.
#
# - jeśli 1 i 3 kolidują u Was ze sobą na widoku wykresu to dać użytkownikowi możliwość wyboru
# czy życzy sobie wyświetlić volumen czy RSI.

import requests
import matplotlib.pyplot as plt
import time

PAIRS = [('LTC', 'PLN'), ('ETH', 'PLN'), ('BCC', 'PLN')]
PAIRS_COUNT = len(PAIRS)
FREQ = 5
num = None
volume, storage = ([] for _ in range(2))


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


def get_data(crypto_pairs, storage):

    global num
    curr_temp, vol_temp = ([] for _ in range(2))

    for pair in crypto_pairs:
        try:
            request = requests.get(
                f"https://bitbay.net/API/Public/{pair[0]}{pair[1]}/ticker.json"
            )
            orders = request.json()
            curr_temp.append([pair[0], (orders['ask'], orders['bid'])])
            vol_temp.append(orders['volume'])

        except requests.exceptions.RequestException:
            print("Connection problem.")
            return None
    volume.append(vol_temp)
    storage.append(curr_temp)
    num = len(storage[0])


if __name__ == '__main__':
    PAIRS = [('LTC', 'PLN'), ('ETH', 'PLN'), ('BCC', 'PLN')]
    PAIRS_COUNT = len(PAIRS)
    FREQ = 5

    draw_figure()
