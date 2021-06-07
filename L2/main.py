import requests
import time
from requests.exceptions import HTTPError
import csv
from datetime import datetime, date


class Finance():

    def __init__(self):
        self.currencies = ['ETH-PLN', 'BTC-PLN', 'DASH-PLN']
        self.pre_url = 'https://api.bitbay.net/rest/trading/ticker/'
        self.volumen_url = 'https://api.bitbay.net/rest/trading/transactions/'
        self.volumen24_url = 'https://api.bitbay.net/rest/trading/stats/'

    def get_data(self, url):
        try:
            response = requests.get(url)
            content = response.json()

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return 0
        except Exception as err:
            print(f'Other error occurred: {err}')
            return 0
        return content['ticker']

    def get_last_transaction(self, url):
        try:
            response = requests.get(url, params={'limit': 1})
            content = response.json()

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return 0
        except Exception as err:
            print(f'Other error occurred: {err}')
            return 0
        return content['items'][0]

    def get_volumen24(self, url):
        try:
            response = requests.get(url, params={'limit': 1})
            content = response.json()

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return 0
        except Exception as err:
            print(f'Other error occurred: {err}')
            return 0
        return content['stats']['v']

    def get_percentage(self, content):
        percentage = round(((float(content["lowestAsk"]) / float(content["highestBid"])) - 1) * 100, 2)
        return percentage


    def print_percentage(self, value, cur):
        print(f"Różnica między kupnem a sprzedażą {cur} wynosi {value}%")

    def get_full_url(self, cur):
        return self.pre_url + cur

    def get_volumen_url(self, cur):
        return self.volumen_url + cur

    def get_volumen24_url(self, cur):
        return self.volumen24_url + cur

    def create_csv(self):
        fieldnames = ['x_val', 'bid_cur1', 'ask_cur1','bid_cur2', 'ask_cur2','bid_cur3', 'ask_cur3', 'time', 'date']
        fieldnames2 = ['last_1_id', 'last_1_val', 'last_2_id', 'last_2_val', 'last_3_id', 'last_3_val']
        fieldnames3 = ['vol1', 'vol2', 'vol3']

        with open('data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            csv_writer.writeheader()

        with open('volumen.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames2)
            csv_writer.writeheader()

        with open('volumen24.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames3)
            csv_writer.writeheader()


    def write_csv(self, all_content, x_value):
        fieldnames = ['x_val', 'bid_cur1', 'ask_cur1','bid_cur2', 'ask_cur2','bid_cur3', 'ask_cur3', 'time', 'date']

        with open('data.csv', 'a+') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            current_time = datetime.now()
            current_time = current_time.strftime("%m/%d/%Y \n %H:%M:%S")

            today = date.today()

            info = {
                'x_val': x_value,
                'bid_cur1': all_content[0]['highestBid'],
                'ask_cur1': all_content[0]['lowestAsk'],
                'bid_cur2': all_content[1]['highestBid'],
                'ask_cur2': all_content[1]['lowestAsk'],
                'bid_cur3': all_content[2]['highestBid'],
                'ask_cur3': all_content[2]['lowestAsk'],
                'time': current_time,
                'date': today
            }

            csv_writer.writerow(info)

    def write_volumen(self, all_content):
        fieldnames2 = ['last_1_id', 'last_1_val', 'last_2_id', 'last_2_val', 'last_3_id', 'last_3_val']

        with open('volumen.csv', 'a+') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames2)


            info = {
                'last_1_id': all_content[0]['id'],
                'last_1_val': all_content[0]['a'],
                'last_2_id': all_content[1]['id'],
                'last_2_val': all_content[1]['a'],
                'last_3_id': all_content[2]['id'],
                'last_3_val': all_content[2]['a'],

            }

            csv_writer.writerow(info)

    def write_volumen24(self, all_content):
        fieldnames3 = ['vol1', 'vol2', 'vol3']

        with open('volumen24.csv', 'a+') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames3)


            info = {
                'vol1': all_content[0],
                'vol2': all_content[1],
                'vol3': all_content[2],
            }

            csv_writer.writerow(info)


    def main(self):
        x_val = 1
        self.create_csv()
        while True:
            all_content = []
            all_volumen = []
            all_volumen24 = []
            for currency in self.currencies:
                url = self.get_full_url(currency)
                content = self.get_data(url)
                all_content.append(content)
                percentage = self.get_percentage(content)
                self.print_percentage(percentage, currency)

                volumen_url = self.get_volumen_url(currency)
                volumen = self.get_last_transaction(volumen_url)
                all_volumen.append(volumen)

                volumen24_url = self.get_volumen24_url(currency)
                volumen24 = self.get_volumen24(volumen24_url)
                all_volumen24.append(volumen24)

                time.sleep(1)
            self.write_csv(all_content, x_val)
            self.write_volumen(all_volumen)
            self.write_volumen24(all_volumen24)
            time.sleep(5)
            x_val += 1

curr = Finance()
curr.main()