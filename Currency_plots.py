import requests
import sys
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation
from statistics import mean
from tkinter import *
import json
import os
import threading


Currencies=['BCC' , 'LTC' , 'ETH']
Currency_category='PLN'
Url_beg="https://bitbay.net/API/Public/"
Url_end="/ticker.json"

Time_sleep=5

Trans_url = "https://api.bitbay.net/rest/trading/transactions/"
Volume_range=60

Window_RSI=40
Window_mean=20

S=1
X=10
Y=12

plik={0:'domyślny_plik.json'}

def download_data(currency,curr_category,url_beg,url_end): #c_currencies is a list
    url=url_beg+currency+curr_category+url_end
    status=requests.get(url).status_code
    if status==200:
        data = requests.get(url).json()
        return data['ask'],data['bid'],data['volume']
    else:
        print("Could not download data. Try again later!")
        sys.exit()

def download_trans(currency,curr_category,trans_url,Y): #c_currencies is a list
    url=trans_url+currency+'-'+curr_category
    status=requests.get(url).status_code
    trans=[]
    if status==200:
        par={"limit":Y}
        data = requests.get(url,params=par).json()
        for key in data["items"]:
            trans.append(float(key["a"]) * float(key["r"]))
        return trans
    else:
        print("Could not download data. Try again later!")
        sys.exit()


def plot_data(x_data,plt,volumes,i):
    x_data.append(datetime.now().strftime("%H:%M:%S"))
    ask, bid,volume = download_data(Currencies[i], Currency_category, Url_beg, Url_end)

    plt.append(ask)
    plt.append(bid)

    volumes.append(volume)
    return x_data,plt,volumes

def RSI(window_RSI,sell,wzrost,spadek,RSI_value):
    if len(sell)==1:
        wzrost.append(0)
        spadek.append(0)
    else:
        if (sell[-1]-sell[-2])>=0:
            wzrost.append(sell[-1]-sell[-2])
            spadek.append(0)
        else:
            wzrost.append(0)
            spadek.append(sell[-1] - sell[-2])

    if len(sell)<=window_RSI:
        if mean(spadek) == 0:
            RSI_value.append(0)
            return RSI_value
        RSI_value.append(100 - (100 / (1 + (mean(wzrost) / abs(mean(spadek))))))
    else:
        if mean(spadek[-window_RSI:]) == 0:
            RSI_value.append(0)
            return RSI_value
        RSI_value.append(100-(100/(1+(mean(wzrost[-window_RSI:])/abs(mean(spadek[-window_RSI:]))))))
    return RSI_value



def mean_data(window_mean,sell_data, buy_data,sell_data_mean,buy_data_mean):
    if len(sell_data)>=window_mean and len(buy_data)>=window_mean:
        sell_data_mean.append(mean(sell_data[-window_mean:]))
        buy_data_mean.append(mean(buy_data[-window_mean:]))
    else:
        sell_data_mean.append(mean(sell_data))
        buy_data_mean.append(mean(buy_data))
    return sell_data_mean,buy_data_mean

def find_volume(volumes,changed_volumes):
    if len(volumes)>=2:
        if volumes[-2]>=volumes[-1]:
            changed_volumes.append(0)
        else:
            changed_volumes.append(volumes[-1]-volumes[-2])
    else:
        changed_volumes.append(0)
    return changed_volumes


def x_range_plot(data):
    if len(data)>=10:
        l=int(len(data)//10)
        data=data[::l+1]
    return data

def x_data(data):
    data=x_range_plot(data)
    return data

def buy_sell(Currencies,Currency_category,srednia_kupna_BTC,srednia_kupna_LTC,srednia_kupna_ETH,zysk_strata_BTC,zysk_strata_LTC,zysk_strata_ETH):
    # Currencies = ['BCC', 'LTC', 'ETH']
    # Currency_category = 'PLN'
    kupno = []
    sprzedaz = []
    kupno_BTC = []
    kupno_LTC = []
    kupno_ETH = []
    sprzedaz_BTC = []
    sprzedaz_LTC = []
    sprzedaz_ETH = []
    suma_BTC = {0: 0}
    suma_LTC = {0: 0}
    suma_ETH = {0: 0}
    s_BTC = {0: 0}
    s_LTC = {0: 0}
    s_ETH = {0: 0}
    suma_sell_BTC=0
    suma_sell_LTC=0
    suma_sell_ETH=0
    kupione=['-']
    sprzedane=['-']

    master = Tk()
    master.title("Kupno i sprzedaż")
    w = 900
    h = 200
    my_w = 1366
    my_h = 768
    x = int(my_w / 2 - w / 2)
    y = int(my_h / 2 - h / 2)
    master.geometry(f"{w}x{h}+{x}+{y}")

    Label(master, text=f"Kupno [{Currency_category}]").grid(row=0)
    Label(master, text=f"Sprzedaż [{Currency_category}]").grid(row=2)
    Label(master, text="Wpisz ilość jednostek:").grid(row=1)
    Label(master, text="Wpisz ilość jednostek:").grid(row=3)
    Label(master, text="").grid(row=4)
    Label(master, text="Kupione:").grid(row=5)
    Label(master, text="Sprzedane:").grid(row=6)

    E1 = Entry(master)
    E1.grid(row=1, column=1)

    E2 = Entry(master)
    E2.grid(row=3, column=1)

    Label(master, text="Wpisz cenę za jednostkę:").grid(row=1, column=2)
    Label(master, text="Wpisz cenę za jednostkę:").grid(row=3, column=2)
    Label(master, text="Wpisz nazwę pliku:").grid(row=1, column=8)
    E = Entry(master)
    E.grid(row=2, column=8)

    E3 = Entry(master)
    E3.grid(row=1, column=3)

    E4 = Entry(master)
    E4.grid(row=3, column=3)

    choices_buy = kupione
    variable_buy = StringVar(master)
    variable_buy.set('Wyświetl')

    choices_sell = sprzedane
    variable_sell = StringVar(master)
    variable_sell.set('Wyświetl')

    choices = Currencies
    variable_1 = StringVar(master)
    variable_1.set('Wybierz walutę')
    variable_2 = StringVar(master)
    variable_2.set('Wybierz walutę')

    W1 = OptionMenu(master, variable_1, *choices).grid(row=1, column=5)
    W2 = OptionMenu(master, variable_2, *choices).grid(row=3, column=5)
    W_buy = OptionMenu(master, variable_buy, *choices_buy).grid(row=5, column=1)
    W_sell = OptionMenu(master, variable_sell, *choices_sell).grid(row=6, column=1)

    def pobierz_dane(plik,zysk_strata_BTC,zysk_strata_LTC,zysk_strata_ETH,suma_sell_BTC,suma_sell_LTC,suma_sell_ETH,W_buy,W_sell):
        if E.get()!='':
            plik=E.get()
        srednia_kupna_BTC[0]=0
        srednia_kupna_LTC[0]=0
        srednia_kupna_ETH[0]=0
        zysk_strata_BTC[0]=0
        zysk_strata_LTC[0]=0
        zysk_strata_ETH[0]=0
        kupno = []
        sprzedaz = []
        kupno_BTC = []
        kupno_LTC = []
        kupno_ETH = []
        sprzedaz_BTC = []
        sprzedaz_LTC = []
        sprzedaz_ETH = []
        suma_BTC = {0: 0}
        suma_LTC = {0: 0}
        suma_ETH = {0: 0}
        s_BTC = {0: 0}
        s_LTC = {0: 0}
        s_ETH = {0: 0}
        suma_sell_BTC = 0
        suma_sell_LTC = 0
        suma_sell_ETH = 0
        kupione = ['-']
        sprzedane = ['-']
        filesize = os.path.getsize(plik)
        if filesize == 0:
            print()
        else:
            with open(plik) as json_file:
                data = json.load(json_file)
                for p in range(len(data)):
                    if data[p] == 'K':
                        kupno.append(data[p - 3])
                        kupno.append(data[p - 2])
                        kupno.append(data[p - 1])
                        kupno.append(data[p])
                        kupione.append(f'Kupiono {data[p - 3]} {data[p - 1]} po {data[p - 2]} za jednostkę')
                        if data[p - 1] == Currencies[0]:
                            suma_BTC[0] += float(data[p - 3])
                            kupno_BTC.append([data[p - 3], data[p - 2]])
                        if data[p - 1] == Currencies[1]:
                            suma_LTC[0] += float(data[p - 3])
                            kupno_LTC.append([data[p - 3], data[p - 2]])
                        if data[p - 1] == Currencies[2]:
                            suma_ETH[0] += float(data[p - 3])
                            kupno_ETH.append([data[p - 3], data[p - 2]])
                    if data[p] == 'S':
                        sprzedaz.append(data[p - 3])
                        sprzedaz.append(data[p - 2])
                        sprzedaz.append(data[p - 1])
                        sprzedaz.append(data[p])
                        sprzedane.append(f'Sprzedano {data[p - 3]} {data[p - 1]} po {data[p - 2]} za jednostkę')
                        if data[p - 1] == Currencies[0]:
                            sprzedaz_BTC.append([data[p - 3], data[p - 2]])
                        if data[p - 1] == Currencies[1]:
                            sprzedaz_LTC.append([data[p - 3], data[p - 2]])
                        if data[p - 1] == Currencies[2]:
                            sprzedaz_ETH.append([data[p - 3], data[p - 2]])

        if len(sprzedaz_BTC)>=1:
            for i in range(len(sprzedaz_BTC)):
                zysk_strata_BTC[0]+=(float(sprzedaz_BTC[i][0])*float(sprzedaz_BTC[i][1]))
                suma_BTC[0]-=float(sprzedaz_BTC[i][0])
                suma_sell_BTC+=float(sprzedaz_BTC[i][0])
            id_BTC=[]
            for i in range(len(kupno_BTC)):
                if float(kupno_BTC[i][0])<=suma_sell_BTC:
                    id_BTC.append(i)
                    suma_sell_BTC-=float(kupno_BTC[i][0])
                    zysk_strata_BTC[0] -= (float(kupno_BTC[i][0]) * float(kupno_BTC[i][1]))
                elif float(kupno_BTC[i][0])>suma_sell_BTC:
                    Old_kupno_BTC = kupno_BTC[i][0]
                    kupno_BTC[i][0]=float(kupno_BTC[i][0])-suma_sell_BTC
                    zysk_strata_BTC[0]-=((float(Old_kupno_BTC)-float(kupno_BTC[i][0]))*float(kupno_BTC[i][1]))
                    suma_sell_BTC=0
                    break
            id_BTC.sort(reverse=True)
            for d in id_BTC:
                kupno_BTC.pop(d)

        if len(kupno_BTC) == 0:
            srednia_kupna_BTC[0] = 0
            s_BTC = {0: 0}
        else:
            for i in range(len(kupno_BTC)):
                srednia_kupna_BTC[0] += (float(kupno_BTC[i][0]) * float(kupno_BTC[i][1]))
            s_BTC = {0: srednia_kupna_BTC[0]}
            srednia_kupna_BTC[0] = srednia_kupna_BTC[0] / suma_BTC[0]

        if len(sprzedaz_LTC)>=1:
            for i in range(len(sprzedaz_LTC)):
                zysk_strata_LTC[0]+=(float(sprzedaz_LTC[i][0])*float(sprzedaz_LTC[i][1]))
                suma_LTC[0] -= float(sprzedaz_LTC[i][0])
                suma_sell_LTC+=float(sprzedaz_LTC[i][0])
            id_LTC=[]
            for i in range(len(kupno_LTC)):
                if float(kupno_LTC[i][0])<=suma_sell_LTC:
                    id_LTC.append(i)
                    suma_sell_LTC-=float(kupno_LTC[i][0])
                    zysk_strata_LTC[0] -= (float(kupno_LTC[i][0]) * float(kupno_LTC[i][1]))
                elif float(kupno_LTC[i][0])>suma_sell_LTC:
                    Old_kupno_LTC = kupno_LTC[i][0]
                    kupno_LTC[i][0]=float(kupno_LTC[i][0])-suma_sell_LTC
                    zysk_strata_LTC[0]-=((float(Old_kupno_LTC)-float(kupno_LTC[i][0]))*float(kupno_LTC[i][1]))
                    suma_sell_LTC=0
                    break
            id_LTC.sort(reverse=True)
            for d in id_LTC:
                kupno_LTC.pop(d)

        if len(kupno_LTC) == 0:
            s_LTC = {0: 0}
            srednia_kupna_LTC[0] = 0
        else:
            for j in range(len(kupno_LTC)):
                srednia_kupna_LTC[0] += (float(kupno_LTC[j][0]) * float(kupno_LTC[j][1]))
            s_LTC = {0: srednia_kupna_LTC[0]}
            srednia_kupna_LTC[0] = srednia_kupna_LTC[0] / suma_LTC[0]

        if len(sprzedaz_ETH)>=1:
            for i in range(len(sprzedaz_ETH)):
                zysk_strata_ETH[0]+=(float(sprzedaz_ETH[i][0])*float(sprzedaz_ETH[i][1]))
                suma_ETH[0] -= float(sprzedaz_ETH[i][0])
                suma_sell_ETH+=float(sprzedaz_ETH[i][0])
            id_ETH=[]
            for i in range(len(kupno_ETH)):
                if float(kupno_ETH[i][0])<=suma_sell_ETH:
                    id_ETH.append(i)
                    suma_sell_ETH-=float(kupno_ETH[i][0])
                    zysk_strata_ETH[0]-= (float(kupno_ETH[i][0]) * float(kupno_ETH[i][1]))
                elif float(kupno_ETH[i][0])>suma_sell_ETH:
                    Old_kupno_ETH=kupno_ETH[i][0]
                    kupno_ETH[i][0]=float(kupno_ETH[i][0])-suma_sell_ETH
                    zysk_strata_ETH[0]-=((float(Old_kupno_ETH)-float(kupno_ETH[i][0]))*float(kupno_ETH[i][1]))
                    suma_sell_ETH=0
                    break
            id_ETH.sort(reverse=True)
            for d in id_ETH:
                kupno_ETH.pop(d)

        if len(kupno_ETH) == 0:
            s_ETH = {0: 0}
            srednia_kupna_ETH[0] = 0
        else:
            for g in range(len(kupno_ETH)):
                srednia_kupna_ETH[0] += (float(kupno_ETH[g][0]) * float(kupno_ETH[g][1]))
            s_ETH = {0: srednia_kupna_ETH[0]}
            srednia_kupna_ETH[0] = srednia_kupna_ETH[0] / suma_ETH[0]
        W_buy = OptionMenu(master, variable_buy, *kupione).grid(row=5, column=1)
        W_sell = OptionMenu(master, variable_sell, *sprzedane).grid(row=6, column=1)

    def kup(srednia_kupna_BTC, srednia_kupna_LTC, srednia_kupna_ETH, s_BTC, s_LTC, s_ETH, suma_BTC, suma_LTC, suma_ETH,plik,W_buy):
        if E.get() != '':
            plik = E.get()
        with open(plik) as json_file:
            d = json.load(json_file)
            list = []
            for dane in d:
                list.append(dane)

            q = E1.get()
            p = E3.get()
            v = variable_1.get()
            list.append(q)
            list.append(p)
            list.append(v)
            list.append('K')
            kupno.append(q)
            kupno.append(p)
            kupno.append(v)
            kupno.append('K')
            kupione.append(f'Kupiono {q} {v} po {p} za jednostkę')
            with open(plik, 'w') as outfile:
                json.dump(list, outfile)
            if v == choices[0]:
                kupno_BTC.append([q, p])
                suma_BTC[0] += float(q)
                s_BTC[0] += (float(q) * float(p))
                srednia_kupna_BTC[0] = s_BTC[0]
                srednia_kupna_BTC[0] /= suma_BTC[0]
            if v == choices[1]:
                kupno_LTC.append([q, p])
                suma_LTC[0] += float(q)
                s_LTC[0] += (float(q) * float(p))
                srednia_kupna_LTC[0] = s_LTC[0]
                srednia_kupna_LTC[0] /= suma_LTC[0]
            if v == choices[2]:
                kupno_ETH.append([q, p])
                suma_ETH[0] += float(q)
                s_ETH[0] += (float(q) * float(p))
                srednia_kupna_ETH[0] = s_ETH[0]
                srednia_kupna_ETH[0] /= suma_ETH[0]
        W_buy = OptionMenu(master, variable_buy, *choices_buy).grid(row=5, column=1)



    def sprzedaj(plik,zysk_strata_BTC,zysk_strata_LTC,zysk_strata_ETH,srednia_kupna_BTC, srednia_kupna_LTC, srednia_kupna_ETH, s_BTC, s_LTC, s_ETH, suma_BTC, suma_LTC, suma_ETH,suma_sell_BTC,suma_sell_LTC,suma_sell_ETH,kupno_BTC,kupno_LTC,kupno_ETH,W_sell):
        if E.get() != '':
            plik = E.get()
        with open(plik) as json_file:
            d = json.load(json_file)
            list = []
            for dane in d:
                list.append(dane)
            q = E2.get()
            p = E4.get()
            v = variable_2.get()
            list.append(q)
            list.append(p)
            list.append(v)
            list.append('S')
            sprzedaz.append(q)
            sprzedaz.append(p)
            sprzedaz.append(v)
            sprzedaz.append('S')
            sprzedane.append(f'Sprzedano {q} {v} po {p} za jednostkę')
            if v == choices[0]:
                if int(q)>suma_BTC[0]:
                    print('Zła ilość, wprowadź inną wartość!')
                    return
                zysk_strata_BTC[0] += (float(q) * float(p))
                suma_BTC[0] -= float(q)
                suma_sell_BTC+=float(q)
                id_BTC = []
                for i in range(len(kupno_BTC)):
                    if float(kupno_BTC[i][0]) <= suma_sell_BTC:
                        id_BTC.append(i)
                        suma_sell_BTC -= float(kupno_BTC[i][0])
                        zysk_strata_BTC[0] -= (float(kupno_BTC[i][0]) * float(kupno_BTC[i][1]))
                    elif float(kupno_BTC[i][0]) > suma_sell_BTC:
                        Old_kupno_BTC = kupno_BTC[i][0]
                        kupno_BTC[i][0] = float(kupno_BTC[i][0]) - suma_sell_BTC
                        zysk_strata_BTC[0] -= ((float(Old_kupno_BTC) - float(kupno_BTC[i][0])) * float(kupno_BTC[i][1]))
                        break
                id_BTC.sort(reverse=True)
                for d in id_BTC:
                    kupno_BTC.pop(d)
                if len(kupno_BTC) == 0:
                    s_BTC[0] =0
                    srednia_kupna_BTC[0] = 0
                else:
                    srednia_kupna_BTC[0] = 0
                    for i in range(len(kupno_BTC)):
                        srednia_kupna_BTC[0] += (float(kupno_BTC[i][0]) * float(kupno_BTC[i][1]))
                    s_BTC[0]=srednia_kupna_BTC[0]
                    srednia_kupna_BTC[0] = srednia_kupna_BTC[0] / suma_BTC[0]

            if v == choices[1]:
                if int(q)>suma_LTC[0]:
                    print('Zła ilość, wprowadź inną wartość!')
                    return
                zysk_strata_LTC[0] += (float(q) * float(p))
                suma_LTC[0] -= float(q)
                suma_sell_LTC+=float(q)

                id_LTC = []
                for i in range(len(kupno_LTC)):
                    if float(kupno_LTC[i][0]) <= suma_sell_LTC:
                        id_LTC.append(i)
                        suma_sell_LTC -= float(kupno_LTC[i][0])
                        zysk_strata_LTC[0] -= (float(kupno_LTC[i][0]) * float(kupno_LTC[i][1]))
                    elif float(kupno_LTC[i][0]) > suma_sell_LTC:
                        Old_kupno_LTC = kupno_LTC[i][0]
                        kupno_LTC[i][0] = float(kupno_LTC[i][0]) - suma_sell_LTC
                        zysk_strata_LTC[0] -= ((float(Old_kupno_LTC) - float(kupno_LTC[i][0])) * float(kupno_LTC[i][1]))
                        suma_sell_LTC = 0
                        break
                id_LTC.sort(reverse=True)
                for d in id_LTC:
                    kupno_LTC.pop(d)

            if len(kupno_LTC) == 0:
                s_LTC[0]=0
                srednia_kupna_LTC[0] = 0
            else:
                srednia_kupna_LTC[0]=0
                for j in range(len(kupno_LTC)):
                    srednia_kupna_LTC[0] += (float(kupno_LTC[j][0]) * float(kupno_LTC[j][1]))
                s_LTC[0] = srednia_kupna_LTC[0]
                srednia_kupna_LTC[0] = srednia_kupna_LTC[0] / suma_LTC[0]


            if v == choices[2]:
                if int(q)>suma_ETH[0]:
                    print('Zła ilość, wprowadź inną wartość!')
                    return
                zysk_strata_ETH[0] += (float(q) * float(p))
                suma_ETH[0] -= float(q)
                suma_sell_ETH+=float(q)

                id_ETH = []
                for i in range(len(kupno_ETH)):
                    if float(kupno_ETH[i][0]) <= suma_sell_ETH:
                        id_ETH.append(i)
                        suma_sell_ETH -= float(kupno_ETH[i][0])
                        zysk_strata_ETH[0] -= (float(kupno_ETH[i][0]) * float(kupno_ETH[i][1]))
                    elif float(kupno_ETH[i][0]) > suma_sell_ETH:
                        Old_kupno_ETH = kupno_ETH[i][0]
                        kupno_ETH[i][0] = float(kupno_ETH[i][0]) - suma_sell_ETH
                        zysk_strata_ETH[0] -= ((float(Old_kupno_ETH) - float(kupno_ETH[i][0])) * float(kupno_ETH[i][1]))
                        suma_sell_ETH = 0
                        break
                id_ETH.sort(reverse=True)
                for d in id_ETH:
                    kupno_ETH.pop(d)

            if len(kupno_ETH) == 0:
                s_ETH[0]=0
                srednia_kupna_ETH[0] = 0
            else:
                srednia_kupna_ETH[0]=0
                for g in range(len(kupno_ETH)):
                    srednia_kupna_ETH[0] += (float(kupno_ETH[g][0]) * float(kupno_ETH[g][1]))
                s_ETH[0] = srednia_kupna_ETH[0]
                śsrednia_kupna_ETH[0] = srednia_kupna_ETH[0] / suma_ETH[0]
        with open(plik, 'w') as outfile:
            json.dump(list, outfile)

        W_sell = OptionMenu(master, variable_sell, *choices_sell).grid(row=6, column=1)


    B1 = Button(master, text="Kupiono",
                command=lambda: kup(srednia_kupna_BTC, srednia_kupna_LTC, srednia_kupna_ETH, s_BTC, s_LTC, s_ETH,
                                    suma_BTC, suma_LTC, suma_ETH,plik[0],W_buy)).grid(row=1, column=6)
    B2 = Button(master, text="Sprzedano", command=lambda:sprzedaj(plik[0],zysk_strata_BTC,zysk_strata_LTC,zysk_strata_ETH,srednia_kupna_BTC,srednia_kupna_LTC, srednia_kupna_ETH, s_BTC, s_LTC, s_ETH, suma_BTC, suma_LTC, suma_ETH,suma_sell_BTC,suma_sell_LTC,suma_sell_ETH,kupno_BTC,kupno_LTC,kupno_ETH,W_sell)).grid(row=3, column=6)

    B = Button(master, text="Pobierz dane", command=lambda:pobierz_dane(plik[0],zysk_strata_BTC,zysk_strata_LTC,zysk_strata_ETH,suma_sell_BTC,suma_sell_LTC,suma_sell_ETH,W_buy,W_sell)).grid(row=3, column=8)

    master.mainloop()


def plot(data,y_data,volumes,window_mean,currency,axs,l,sell_mean,buy_mean,wzrost,spadek,RSI_value,choice,changed_volumes,m_s,win_loss):
    RSI_vol=RSI(Window_RSI,y_data[::2],wzrost,spadek,RSI_value)
    volume = find_volume(volumes,changed_volumes)
    x=x_data(data)
    sell,buy=mean_data(window_mean,y_data[::2], y_data[1::2],sell_mean,buy_mean)

    s=[m_s[0] for i in range(len(data))]


    plt.show()
    axs[0][l].plot(data,sell,label=currency+'_ask_mean',alpha=0.5,ls='--')
    axs[0][l].plot(data, y_data[::2],label=currency+'_ask')

    axs[0][l].plot(data, buy,label=currency+'_bid_mean',alpha=0.5,ls='--')
    axs[0][l].plot(data, y_data[1::2],label=currency+'_bid')

    axs_m = axs[0][l].twinx()

    axs_m.plot(data, s, label=currency+'_buy_average', alpha=0.5, ls='--',color='olive')
    axs_m.set_ylabel('Buy average', color='olive')
    if float(win_loss[0])>=0:
        sign='Zysk'
    else:
        sign='Strata'
    val_m = f'{sign} {win_loss[0]}'
    axs_m.text(0.95, 1.1, val_m, horizontalalignment='center',
                   verticalalignment='center', transform=axs_m.transAxes)

    axs[1][l].bar(data, volume,color='r',alpha=0.7)
    axs[1][l].set_ylim(bottom=0,top=None)
    axs[1][l].set_ylabel('Wolumen',color='r')
    val=f'Wolumen: {round(sum(volume[-int(Volume_range/Time_sleep):]),3)}'
    axs[1][l].text(0.2, 0.05, val, horizontalalignment='center',
                  verticalalignment='center', transform=axs[1][l].transAxes)

    axs2= axs[1][l].twinx()
    axs2.plot(data, RSI_vol)
    axs2.set_ylim(0, 100)
    axs2.set_ylabel('RSI',color='b')
    val=f'RSI: {round((RSI_vol[-1]),2)}'
    axs2.text(0.15, 0.95, val, horizontalalignment='center',
                   verticalalignment='center', transform=axs2.transAxes)


    axs[1][l].set_xlabel('Czas')
    axs[0][l].set_ylabel('Cena')
    axs[1][l].set_xticks((x))
    axs[1][l].set_xticklabels(x, rotation=45)

    axs[0][l].legend(bbox_to_anchor=(0, 1.2), loc='center',prop={'size': 6})

    fig.tight_layout()

    return RSI_vol,volume,y_data

def volatile_asset(X, Y,i):
    data=download_trans(Currencies[i],Currency_category,Trans_url,Y)

    minimum = min(data)
    maximum = max(data)

    diff = (abs(maximum - minimum) / maximum) * 100
    diff = round(diff, 2)

    if diff > X:
        return 'Volatile asset'
    else:
        return ''

def spread(S,y_data):
    diff = 100*((y_data[-2]- y_data[-1]) / y_data[-1])

    if diff<S:
        return 'Liquid asset'
    else:
        return ''



def increase_decrease_RSI(RSI_list,volume_list,axs,y_data):
    decisions=[]
    volume_max=0
    for r in range(len(RSI_list)):
        if RSI_list[r][-1] <= 40:
            decisions.append("Trend spadkowy")
        if RSI_list[r][-1] >= 60:
            decisions.append("Trend wzrostowy")
            if volume_max<=round(sum(volume_list[r][-int(Volume_range/Time_sleep):]),3):
                volume_max=round(sum(volume_list[r][-int(Volume_range/Time_sleep):]),3)
        if RSI_list[r][-1] > 40 and RSI_list[r][-1] <60:
            decisions.append('Trend boczny')
    for i in range(len(decisions)):
        if RSI_list[i][-1]!=0:
            axs[1][i].text(0.5, 0.95, decisions[i], horizontalalignment='center',
                       verticalalignment='center', transform=axs[1][i].transAxes)
            if decisions[i]=='Trend wzrostowy' and round(sum(volume_list[i][-int(Volume_range/Time_sleep):]),3)==volume_max:
                s=spread(S,y_data[i])
                v=volatile_asset(X, Y,i)
                axs[0][i].set_title("Najlepszy kandydat \n"+s+'\n'+v)

def draw_plot(i):
    x_data_BCC_d,plt_BCC_d,BCC_volumes_d=plot_data(x_data_BCC,plt_BCC, BCC_volumes,0)
    x_data_LTC_d, plt_LTC_d, LTC_volumes_d = plot_data(x_data_LTC, plt_LTC, LTC_volumes,1)
    x_data_ETH_d, plt_ETH_d, ETH_volumes_d = plot_data(x_data_ETH, plt_ETH, ETH_volumes,2)
    plt.clf()
    gs = fig.add_gridspec(2, 3, hspace=0)
    axs = gs.subplots(sharex=True)

    BCC_RSI,BCC_volume,BCC_plt=plot(x_data_BCC_d,plt_BCC_d,BCC_volumes_d, Window_mean, 'BCC',axs,0,sell_mean_BCC,buy_mean_BCC,wzrost_BCC,spadek_BCC,RSI_BCC,choice,changed_volumes_BCC,srednia_kupna_BTC,zysk_strata_BTC)
    LTC_RSI,LTC_volume,LTC_plt=plot(x_data_LTC_d, plt_LTC_d, LTC_volumes_d, Window_mean, 'LTC',axs, 1,sell_mean_LTC,buy_mean_LTC,wzrost_LTC,spadek_LTC,RSI_LTC,choice,changed_volumes_LTC,srednia_kupna_LTC,zysk_strata_LTC)
    ETH_RSI,ETH_volume,ETH_plt=plot(x_data_ETH_d, plt_ETH_d, ETH_volumes_d, Window_mean, 'ETH',axs, 2,sell_mean_ETH,buy_mean_ETH,wzrost_ETH,spadek_ETH,RSI_ETH,choice,changed_volumes_ETH,srednia_kupna_ETH,zysk_strata_ETH)

    increase_decrease_RSI([BCC_RSI,LTC_RSI,ETH_RSI],[BCC_volume,LTC_volume,ETH_volume],axs,[BCC_plt,LTC_plt,ETH_plt])


if __name__=="__main__":
    x_data_BCC= [];x_data_LTC = [];x_data_ETH = []
    plt_BCC= [];plt_LTC = [];plt_ETH = []
    BCC_volumes=[];LTC_volumes=[];ETH_volumes=[]
    sell_mean_BCC=[];buy_mean_BCC=[]
    sell_mean_LTC=[];buy_mean_LTC=[]
    sell_mean_ETH=[];buy_mean_ETH=[]
    wzrost_BCC = [];spadek_BCC = []
    wzrost_LTC = [];spadek_LTC = []
    wzrost_ETH=[];spadek_ETH=[]
    RSI_BCC=[];RSI_LTC=[];RSI_ETH=[]
    changed_volumes_BCC=[];changed_volumes_LTC=[];changed_volumes_ETH=[]
    fig = plt.figure()
    choice='RSI and volume'
    srednia_kupna_BTC = {0: 0}
    srednia_kupna_LTC = {0: 0}
    srednia_kupna_ETH = {0: 0}
    zysk_strata_BTC={0:0}
    zysk_strata_LTC={0:0}
    zysk_strata_ETH={0:0}
    T_animation=animation(fig,draw_plot,interval=1000*Time_sleep)
    th = threading.Thread(target=buy_sell, args=(Currencies,Currency_category,srednia_kupna_BTC,srednia_kupna_LTC,srednia_kupna_ETH,zysk_strata_BTC,zysk_strata_LTC,zysk_strata_ETH))
    th.start()

    plt.show()



