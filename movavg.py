# Wykresy trzech zasobów z poprzedniego zadania wyświetlać na trzech osobnych wykresach
# - na wykresie lub pod wykresem dodać wolumen transakcji
# - oprócz linii wartości osiąganych przez zasób dodać innym kolorem średnią  ruchomą
# z wybranego przedziału próbek. Przedział do ustalenia przez użytkownika, można ograniczyć zakres.
# - dodać oscylator RSI (relative strength index / wskaźnik siły względnej) Przedział y do ustalenia
# przez użytkownika.
# - jeśli 1 i 3 kolidują u Was ze sobą na widoku wykresu to dać użytkownikowi możliwość wyboru
# czy życzy sobie wyświetlić volumen czy RSI.

import requests
import matplotlib.pyplot as plt
import time


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
