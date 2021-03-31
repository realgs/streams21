import requests


currency = ['BTCPLN', 'ETHPLN', 'LSKPLN']
urls = [f'https://bitbay.net/API/Public/{currency[0]}/ticker.json',f'https://bitbay.net/API/Public/{currency[1]}/ticker.json',f'https://bitbay.net/API/Public/{currency[2]}/ticker.json']

def get_data(url):
    response = requests.get(url)
    data = response.json()
    return data
def show_ratio():
    for i in range(0,len(urls)):
        data = get_data(urls[i])
        print(f'Currency: {currency[i]} \n Bid: {data["bid"]} Ask: {data["ask"]}')


show_ratio()
