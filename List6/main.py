
import tkinter as tk
from tkinter import filedialog as fd
import time
from tkinter.constants import SINGLE
from PIL import ImageTk, Image
import pathlib
import json
import requests
import time
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

path = str(pathlib.Path(__file__).parent.absolute())


def get_data(currency_pair, method):
    try:
        req = requests.get(f'https://api.bitbay.net/rest/trading/{method}/{currency_pair}/10')
        if req.status_code == 200:
            data = req.json()
        else:
            print("Wystapil blad podczas pobierania -",currency_pair)
    except HTTPError:
        print('Error:', HTTPError)
        return None
    return float(data['buy'][0]['ra']), float(data['sell'][0]['ra']) ,datetime.now()


def get_volume(currency_pair):
    now = int(str(time.time()*1000)[:9]+'0000')
    try:
        req = requests.get(f'https://api.bitbay.net/rest/trading/candle/history/{currency_pair}/60?from={now - 600000}&to={now}')
        if req.status_code == 200:
            data = req.json()
            vol = 0
            for i in data['items']:
                vol += float(i[1]['v'])
        else:
            print("Wystapil blad podczas pobierania -",currency_pair)
    except HTTPError:
        print('Error:', HTTPError)
        return None
    
    return vol

def calc_avg(data, size):
    total = 0
    if len(data) > size:
        for i in data[len(data) - size:]:
            total += i
        total /= size
    else:
        for i in data:
            total += i
        total /= len(data)
    return total


def calc_rsi(data, size):
    inc = list()
    dec = list()
    if len(data) >= size:
        sample = data[len(data) - size:]
        for i in range(len(sample) - 1, 0, -1):
            temp = sample[i] - sample[i-1]
            if temp > 0:
                inc.append(temp)
            elif temp < 0:
                dec.append(abs(temp))
    else:
        return 50

    a = (sum(inc) + 1) / (len(inc) + 1)
    b = (sum(dec) + 1) / (len(dec) + 1)

    RSI = 100 - (100 / (1 + (a / b)))
    return RSI


class App():
    def __init__(self):
        self.CURR = ['LTC','ETH']
        self.BASE = ['PLN']
        self.INTERVAL = 3000
        self.MAX_POINTS = 50
        self.SAMPLE_SIZE = 5
        self.CHOICE = 'r'
        if self.CHOICE == 'r':
            self.RSI_SAMPLE_SIZE = 5
        self.trends = {}

        self.root = tk.Tk()
        self.root.title('API')
        self.root.geometry("1600x900")
        
        self.draw_app()
        self.root.mainloop()

    def draw_app(self):
        self.left_frame =tk.Frame()
        self.left_frame.grid(row=0, column=0)

        self.generate_plot(self.create_pairs())
        image = Image.open(path +'\\test.png')
        resized_image = image.resize((962,473))
        self.img = ImageTk.PhotoImage(resized_image)
        self.label = tk.Label(self.left_frame, image=self.img)
        self.label.grid(row=0, column=0, columnspan = 5, sticky = tk.W+tk.E)

        self.start_button = tk.Button(self.left_frame, text = 'Start', command=self.update_image).grid(row=1, column = 0)
        self.save_button = tk.Button(self.left_frame, text = 'Zapisz', command=self.save_data).grid(row=1, column = 1)
        self.load_button = tk.Button(self.left_frame, text = 'Wczytaj', command=self.load_data).grid(row=1, column = 2)

        self.right_frame =tk.Frame()
        self.right_frame.grid(row=0, column=1)

        self.width_label = tk.Label(self.right_frame, text='Przedział wyświetlania').grid(row = 0, column=0)
        self.width_input = tk.Entry(self.right_frame)
        self.width_input.grid(row = 1, column=0)
        self.width_input.insert(0,'50')
        
        self.mean_label = tk.Label(self.right_frame, text='Średnia z').grid(row = 0, column=1)
        self.mean_input = tk.Entry(self.right_frame)
        self.mean_input.grid(row = 1, column=1)
        self.mean_input.insert(0,'5')

        self.rsimean_label = tk.Label(self.right_frame, text='Średnia RSI z:').grid(row = 0, column=2)
        self.rsimean_input = tk.Entry(self.right_frame)
        self.rsimean_input.grid(row = 1, column=2)
        self.rsimean_input.insert(0,'5')

        self.save_values_button = tk.Button(self.right_frame, text = 'Zapisz', command=self.update_values).grid(row=2, column = 0)
        self.blank_line_row3 = tk.Label(self.right_frame, text='\n').grid(row=3,column=0)

        self.buy_label = tk.Label(self.right_frame, text="Kupno").grid(row=4, column=0)
        self.buy_frame = tk.Frame(self.right_frame, highlightbackground="black", highlightthickness=1)
        self.buy_frame.grid(row=5, column=0, columnspan = 3, sticky = tk.W+tk.E)
        self.buy_list_frame = tk.Frame(self.buy_frame)
        self.buy_list_frame.grid(row=0, column=0)
        self.buy_list = tk.Listbox(self.buy_list_frame, selectmode=SINGLE, height=4)
        self.buy_list.grid(row=4, column=0)
        [self.buy_list.insert(i, self.currency_pairs[i]) for i in range(len(self.currency_pairs))]

        self.buy_values_frame = tk.Frame(self.buy_frame)
        self.buy_values_frame.grid(row=0, column=1)

        self.buy_value_label = tk.Label(self.buy_values_frame, text='Wartość: ').grid(row = 0, column=0)
        self.buy_value_input = tk.Entry(self.buy_values_frame)
        self.buy_value_input.grid(row = 0, column=1)

        self.buy_amount_label = tk.Label(self.buy_values_frame, text='Ilość:').grid(row = 1, column=0)
        self.buy_amount_input = tk.Entry(self.buy_values_frame)
        self.buy_amount_input.grid(row = 1, column=1)

        self.buy_button = tk.Button(self.buy_frame, text = 'Kup', command=self.update_buy_values).grid(row=1, column = 0)

        self.sell_label = tk.Label(self.right_frame, text="Sprzedaż").grid(row=6, column=0)
        self.sell_frame = tk.Frame(self.right_frame, highlightbackground="black", highlightthickness=1)
        self.sell_frame.grid(row=7, column=0, columnspan = 3, sticky = tk.W+tk.E)
        self.sell_list_frame = tk.Frame(self.sell_frame)
        self.sell_list_frame.grid(row=0, column=0)
        self.sell_list = tk.Listbox(self.sell_list_frame, selectmode=SINGLE, height=4)
        self.sell_list.grid(row=4, column=0)
        [self.sell_list.insert(i, self.currency_pairs[i]) for i in range(len(self.currency_pairs))]

        self.sell_values_frame = tk.Frame(self.sell_frame)
        self.sell_values_frame.grid(row=0, column=1)

        self.sell_value_label = tk.Label(self.sell_values_frame, text='Wartość: ').grid(row = 0, column=0)
        self.sell_value_input = tk.Entry(self.sell_values_frame)
        self.sell_value_input.grid(row = 0, column=1)

        self.sell_amount_label = tk.Label(self.sell_values_frame, text='Ilość:').grid(row = 1, column=0)
        self.sell_amount_input = tk.Entry(self.sell_values_frame)
        self.sell_amount_input.grid(row = 1, column=1)

        self.buy_button = tk.Button(self.sell_frame, text = 'Sprzedaj', command=self.update_sell_values).grid(row=1, column = 0)
        
        self.blank_line_row8 = tk.Label(self.right_frame, text='\n').grid(row=8,column=0)
        self.income_label = tk.Label(self.right_frame, text='')
        self.income_label.grid(row=9, column=0)


    def update_values(self):
        self.MAX_POINTS = int(self.width_input.get())
        self.SAMPLE_SIZE = int(self.mean_input.get())
        self.RSI_SAMPLE_SIZES = int(self.rsimean_input.get())
        print(self.MAX_POINTS)


    def update_image(self):
        global path
        self.update_plot()
        temp = Image.open(path +'\\test.png')
        resized_image = temp.resize((962,473))
        self.img = ImageTk.PhotoImage(resized_image)
        self.label.configure(image=self.img)
        self.root.after(3000, self.update_image)


    def create_pairs(self):
        self.currency_pairs = []
        for i in self.CURR:
            for j in self.BASE:
                self.currency_pairs.append(i+'-'+j)
        return self.currency_pairs


    def create_lists(self, n):
        self.buy, self.sell, self.date, self.avg_sell, self.avg_buy, self.vol, self.rsi, self.buy_history, self.buy_mean, self.income = [],[],[],[],[],[],[],[],[],[]
        for _ in range(n):
            self.sell.append([])
            self.buy.append([])
            self.date.append([])
            self.avg_sell.append([])
            self.avg_buy.append([])
            self.vol.append([])
            self.rsi.append([])
            self.buy_history.append([])
            self.buy_mean.append([])
            self.income.append(0.0)


    def generate_plot(self, currency_pairs):
        self.n = len(currency_pairs)
        self.create_lists(self.n)


        self.fig, self.axs = plt.subplots(2*self.n, sharex=True, figsize=(16, 9))
        self.data_lines = []
        self.text_frames = []
        
        for i in range(self.n):
            self.data_lines.append(self.axs[2*i].plot([], [],'k-' ,label='Sell offer'))
            self.data_lines.append(self.axs[2*i].plot([], [],'k--', label='Avg sell offer'))
            self.data_lines.append(self.axs[2*i].plot([], [],'r-', label='Buy offer'))
            self.data_lines.append(self.axs[2*i].plot([], [],'r--', label='Avg buy offer'))
            self.data_lines.append(self.axs[2*i].plot([], [],'g--', label='Your avg buy'))
            self.data_lines.append(self.axs[2*i+1].plot([], [],'k-o', label='RSI'))

            self.text_frames.append(self.axs[2*i].text(1.02,0.5,'', transform=self.axs[2*i].transAxes))
            self.text_frames.append(self.axs[2*i].text(1.02,0.4,'', transform=self.axs[2*i].transAxes))
            self.text_frames.append(self.axs[2*i].text(1.02,0.3,'', transform=self.axs[2*i].transAxes))
            self.text_frames.append(self.axs[2*i].text(1.02,0.2,'', transform=self.axs[2*i].transAxes))
            
            self.axs[2*i].set_title(currency_pairs[i])
            self.axs[2*i].grid()
            self.axs[2*i].legend(loc=6)
            self.axs[2*i].xaxis.set_major_formatter(DateFormatter('%H:%M:%S %d-%m-%y '))
            self.axs[2*i+1].grid()
            self.axs[2*i+1].legend(loc=6)
            self.axs[2*i+1].xaxis.set_major_formatter(DateFormatter('%d-%m-%y %H:%M:%S'))

        self.fig.autofmt_xdate(rotation=35)
        plt.savefig(str(pathlib.Path(__file__).parent.absolute())+'\\test.png',bbox_inches='tight')


    def update_buy_values(self):
        id = self.buy_list.curselection()[0]
        amount = int(self.buy_amount_input.get())
        for _ in range(amount):
            self.buy_history[id].append(float(self.buy_value_input.get()))
        self.calc_avg_buy(id)
        

    def calc_avg_buy(self, id):
        counter = 0
        summary = 0
        for i in self.buy_history[id]:
            counter += 1
            summary += i
        self.buy_mean[id] = summary / counter
    

    def update_sell_values(self):
        id = self.sell_list.curselection()[0]
        amount = int(self.sell_amount_input.get())
        value = float(self.sell_value_input.get())
        for _ in range(amount):
            if len(self.buy_history[id]) == 0:
                break
            cost = float(self.buy_history[id].pop(0))
            self.income[id] += (value - cost)
        self.print_income()

    def print_income(self):
        self.income_data = ''
        for p in range(len(self.currency_pairs)):
            self.income_data += 'Zysk ' + str(self.currency_pairs[p]) + ' :' + str(self.income[p])+'\n'
        self.income_label['text'] = self.income_data
        self.calc_avg_buy(id)


    def save_data(self):
        filename = fd.asksaveasfilename(filetypes=[("Plik JSON","*.json")], defaultextension = "*.json")
        data = {}
        for d in range(len(self.currency_pairs)):
            data[self.currency_pairs[d]] = [self.buy_history[d],self.buy_mean[d],self.income[d]]
        if filename:
            with open(filename, 'w') as json_file:
                json.dump(data , json_file)


    def load_data(self):
        filename = fd.askopenfilename(filetypes=[("Plik JSON","*.json")])
        if filename:
            with open(filename, 'r') as json_file:
                data = json.load(json_file)

        
        for i in range(len(self.currency_pairs)):
            for k in data.keys():
                if self.currency_pairs[i] == k:
                    self.buy_history[i] = data[k][0]
                    self.buy_mean[i] = data[k][1]
                    self.income[i] = data[k][2]
        self.print_income()              



    def update_plot(self):
        vol = [get_volume(i) for i in self.currency_pairs]

        for i in range(len(self.currency_pairs)):
            data = get_data(self.currency_pairs[i], 'orderbook-limited')
        
            self.buy[i].append(data[0])
            self.sell[i].append(data[1])
            self.date[i].append(data[2])
            self.avg_sell[i].append(calc_avg(self.sell[i], self.SAMPLE_SIZE))
            self.avg_buy[i].append(calc_avg(self.buy[i], self.SAMPLE_SIZE))
            self.rsi[i].append(calc_rsi(self.buy[i], self.RSI_SAMPLE_SIZE))
            
            self.data_lines[i*6][0].set_data(self.date[i], self.sell[i])
            self.data_lines[i*6+1][0].set_data(self.date[i], self.avg_sell[i])
            self.data_lines[i*6+2][0].set_data(self.date[i], self.buy[i])
            self.data_lines[i*6+3][0].set_data(self.date[i], self.avg_buy[i])
            if self.buy_mean[i]:
                self.data_lines[i*6+4][0].set_data(self.date[i], self.buy_mean[i])
            self.data_lines[i*6+5][0].set_data(self.date[i], self.rsi[i])
            
            if len(self.rsi[i]) > 2:
                if self.rsi[i][-1] > self.rsi[i][-2]:
                    self.trend = 'raise'
                    self.trends[i] = 1
                elif self.rsi[i][-1] == self.rsi[i][-2]:
                    self.trend = 'stable'
                    self.trends[i] = 1
                elif self.rsi[i][-1] < self.rsi[i][-2]:
                    self.trend = 'decrease'
                    self.trends[i] = 0
                self.text_frames[i*4].set_text(self.trend)

            self.axs[2*i].relim()
            self.axs[2*i].autoscale_view()
            self.axs[2*i+1].relim()
            self.axs[2*i+1].autoscale_view()

            while len(self.buy[i]) > self.MAX_POINTS:
                self.buy[i].pop(0)
                self.sell[i].pop(0)
                self.date[i].pop(0)
                self.avg_sell[i].pop(0)
                self.avg_buy[i].pop(0)
                if self.CHOICE == 'r':
                    self.rsi[i].pop(0)
                elif self.CHOICE == 'w':   
                    vol[i].pop(0)
            
        Y = 3
        X = 0.5
        S = 0.1
        
        if len(self.rsi[0]) > 2:
            vol = [self.trends[j]*vol[j] for j in range(len(vol))]
            max_id = vol.index(max(vol))
            for k in range(len(vol)):
                if k == max_id and self.trends[k] != 0:
                    self.text_frames[k*4 + 1].set_text('candidate')
                    fluctuation = (abs(max(self.buy[k][-Y:])-min(self.sell[k][-Y:])) / max(self.buy[k][-Y:]))*100
                    if fluctuation > X:
                        self.text_frames[k*4 + 2].set_text('volatile asset')
                    else:
                        self.text_frames[k*4 + 2].set_text(' ')

                    spread = (abs(self.buy[k][-1]-self.sell[k][-1]) / self.buy[k][-1])*100
                    if spread > S:
                        self.text_frames[k*4 + 3].set_text('liquid asset')
                    else:
                        self.text_frames[k*4 + 3].set_text(' ')
                else:
                    self.text_frames[k*4 + 1].set_text(' ')
                    self.text_frames[k*4 + 2].set_text(' ')
                    self.text_frames[k*4 + 3].set_text(' ')
                    
        plt.savefig(str(pathlib.Path(__file__).parent.absolute())+'\\test.png',bbox_inches='tight')

app=App()
