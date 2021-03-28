import requests
import sys


def purchase_selling_diff(purchase_cost, selling_cost):
    result = round((1 - (selling_cost - purchase_cost) / purchase_cost), 3)
    return '{}{}'.format(result, " %")


def get_data(currency):
    url = 'https://bitbay.net/API/Public/{}/ticker.json'.format(currency)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            selling_cost = resp_json['ask']
            purchase_cost = resp_json['bid']
            print('{}: Cena kupna: {}, cena sprzedaży: {}, wynik procentowy:{}'
                  .format(currency, purchase_cost, selling_cost, purchase_selling_diff(purchase_cost, selling_cost)))
        else:
            print("Unable to access API on BitBay. Error: {}".format(response.status_code))
            sys.exit()
    except requests.exceptions.ConnectionError:
        print("Cannot reach the server.")
        sys.exit()


get_data('BTC')
