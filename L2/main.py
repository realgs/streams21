import requests
import time
from requests.exceptions import HTTPError

def get_data(url1,url2,url3):

    content = []
    for url in [url1, url2,url3]:
        try:
            response = requests.get(url)
            content.append(response.json())

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
    return content

def print_data():

    cur1,cur2,cur3 = "BTC","GNT","DASH"
    url1 = f"https://bitbay.net/API/Public/{cur1}/ticker.json"
    url2 = f"https://bitbay.net/API/Public/{cur2}/ticker.json"
    url3 = f"https://bitbay.net/API/Public/{cur3}/ticker.json"
    while True:
        content =  get_data(url1,url2,url3)
        percentage_1 = round(((content[0]["ask"]/content[0]["bid"])-1)*100,2)
        percentage_2 = round(((content[1]["ask"] / content[1]["bid"]) - 1) * 100, 2)
        percentage_3 = round(((content[2]["ask"] / content[2]["bid"]) - 1) * 100, 2)
        print(f"Różnica między kupnem a sprzedażą {cur1} za USD wynosi {percentage_1}%")
        print(f"Różnica między kupnem a sprzedażą {cur2} za USD wynosi {percentage_2}%")
        print(f"Różnica między kupnem a sprzedażą {cur1} za USD wynosi {percentage_3}%")
        time.sleep(30)

print_data()