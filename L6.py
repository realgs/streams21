import requests
import time
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
from matplotlib.animation import FuncAnimation
from flask import Flask, render_template, request
from configing import updateconf, readconf
#__________________________#
#     FUNKCJE DLA API      # 
#__________________________#
def making_list(option,value,cryptocurr):
    print(cryptocurr)
    if cryptocurr == 'DASH':
        print("yes")
        if option == 1:
            DASH_buy.append(value)
        elif option == 2:
            DASH_sell.append(value)
    if cryptocurr == 'LTC':
        if option == 1:
            LTC_buy.append(value)
        elif option == 2:
            LTC_sell.append(value)
    if cryptocurr == 'LSK':
        if option == 1:
            LSK_buy.append(value)
        elif option == 2:
            LSK_sell.append(value)
def balanceUtil(crypto):
    if crypto == "DASH":
        return counter(DASH_buy)
    elif crypto == "LTC":
        return counter(LTC_buy)
    elif crypto == "LSK":
        return counter(LSK_buy)
def update_balance():
    balance = readconf("config.ini","balance")
    temp = profit()
    print(temp,type(temp),type(balance))
    profitU = str(int(balance) + temp)
    updateconf(profitU,"config.ini","balance")
def profitUtil(buys,sells):
    sells = sells[::-1]
    print(sells)
    sprzedaz = sells[0][0]*sells[0][1]
    profit = 0
    for i in range (len(buys)):
        zakup=(buys[i])[0]*(buys[i])[1]
        if (buys[i])[0]-sells[0][0] < 0:
            profit  += sells[0][0]*(sells[0][1]-(buys[i])[1])
            sprzedaz -= zakup
            (buys[i])[0] = 0
            sells[0][0] -= zakup//sells[0][1]
            sprzedaz = sells[0][0]*sells[0][1]
        else:
            profit  += sells[0][0]*(sells[0][1]-(buys[i])[1])
            (buys[i])[0] = (zakup-sells[0][0]*sells[0][1])
            return profit
def profit():
    cryptocurr = readconf("config.ini","crypto")
    if cryptocurr == "DASH":
        temp = profitUtil(DASH_buy,DASH_sell)
        return temp
    if cryptocurr == "LTC":
        temp = profitUtil(LTC_buy,LTC_sell)
        return temp
    if cryptocurr == "LSK":
        temp = profitUtil(LSK_buy,LSK_sell)
        return temp
def returndata(option):
    currency = readconf("config.ini","crypto")
    if currency == 'DASH':
        if option == 1:
            temp = DASH_buy[::-1][0][0]
            DASH_buy_value.append(int(temp))
            return True
        elif option == 2:
            temp = DASH_sell[::-1][0][0]
            DASH_sell_value.append(int(temp))
            return True
    if currency == 'LTC':
        if option == 1:
            temp = LTC_buy[::-1][0][0]
            LTC_buy_value.append(int(temp))
            return True
        elif option == 2:
            temp = LTC_sell[::-1][0][0]
            LTC_sell_value.append(int(temp))
            return True
    if currency == 'LSK':
        if option == 1:
            temp = LSK_buy[::-1][0][0]
            LSK_buy_value.append(int(temp))
            return True
        elif option == 2:
            temp =LSK_sell[::-1][0][0]
            LSK_sell_value.append(int(temp))
            return True
def status():
    if readconf("config.ini","user") == "1":
        return True
    return False
def avg(values): 
    if len(values) == 0:
        return 0
    mean = sum(values)/len(values)
    return mean
def json_save(crypto,option,datas):
    lista = [crypto,option,datas]
    with open('datas.csv', mode='a') as values:
        reader = csv.writer(values, delimiter=',')
        reader.writerow(lista)
def readUtil(data,option,crypto):
    if crypto == "DASH":
        if option == 1:
            print("yes",data)

            DASH_buy.append(data)
        elif option == 2:
            DASH_sell.append(data)
    if crypto == "LTC":
        if option == 1:
            print("yes",data)

            LTC_buy.append(data)
        elif option == 2:
            LTC_sell.append(data)
    if crypto == "LSK":
        if option == 1:
            print("yes",data)
            LSK_buy.append(data)
        elif option == 2:
            LSK_sell.append(data)
def json_read():
    with open("datas.csv","r") as datas:
        csv_reader = csv.reader(datas, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count %2 == 0:
                data = row[2]
                option = int(row[1])
                crypto = row[0]
                print(data,type(option),crypto)
                readUtil(data,option,crypto)
            line_count +=1

#__________________________#
#   FUNKCJE DLA WYKRESOW   # 
#__________________________#
def responseerr(crypto):
    response = requests.get(f'https://bitbay.net/API/Public/{crypto}/ticker.json',timeout=5)
    # user = requests.get(f'http://127.0.0.1:5051/sell')
    try:
        response
    except requests.exceptions.Timeout as to:
        print(f'Request times out {to}')
    except requests.exceptions.TooManyRedirects as tmr:
        print(f'Request exceeds the configured number of maximum redirections {tmr}')
    except requests.exceptions.HTTPError as http:
        print(f'Request returned an unsuccessful status code {http}')
    except requests.exceptions.RequestException as e:
        print(f'In fact, something went wrong but nobody knows what ¯\_(ツ)_/¯ {e}')
    return response
def get_transactions(crypto, currency):
    response = requests.get(f"https://api.bitbay.net/rest/trading/transactions/{crypto}-{currency}?limit=10")
    transactions = json.loads(response.text)
    if transactions["status"] == "Ok":
        return transactions
    else:
        print("Failed to connect, try again")
def volume(crypto, currency):
    transactions = get_transactions(crypto, currency)
    volume = []
    for key in transactions["items"]:
        key["r"] = float(key["r"])
        volume.append(key["r"])
    volume_ = sum(volume)
    return volume_
def datas(crypto):
    response = responseerr(crypto)
    r1 = response.json()
    bid = r1['bid']
    ask = r1['ask']
    return bid,ask
def averange(data,parameter):
    mean = np.mean(data[-(parameter):])
    return mean
def calc_RSI(data, start, end):
    data = data[-20:]
    rsi_data = data[start:end]
    ups = 0
    up_count = 0
    downs = 0
    down_count = 0
    for i in range(1, len(rsi_data)):
        if rsi_data[i-1] < rsi_data[i]:
            up = rsi_data[i] - rsi_data[i-1]
            ups += up
            up_count += 1
        elif rsi_data[i-1] > rsi_data[i]:
            down = rsi_data[i-1] - rsi_data[i]
            downs += down
            down_count += 1
    if up_count == 0:
        a = 1
    else:
        a = ups/up_count
    if down_count == 0:
        b = 1
    else:
        b = downs/down_count
    rsi = 100 - (100/(1+(a/b)))
    return rsi
def trend(rsi_list):
    rsi = rsi_list[-1]
    if rsi >= 70:
        return 'upward trend'
    elif rsi <= 30:
        return 'downward trend'
    return 'sideways trend'
def volumelist(btc,eth,omg):
    volume_list = [btc[-1],eth[-1],omg[-1]]
    return volume_list
def trendlist(btc,eth,omg):
    trend_list = []
    for rsi in [btc,eth,omg]:
        trend_list.append(trend(rsi))
    return trend_list
def candidate():
    volume_list = volumelist(btc=BTCvol,eth=ETHvol,omg=OMGvol)
    trend_list = trendlist(btc=rsi_askBTC,eth=rsi_askETH,omg=rsi_askOMG)
    choosing_dict = {}

    for value in range (3):
        if trend_list[value] != "downward trend":   
            choosing_dict[volume_list[value]] = value
    if len(choosing_dict) != 0:
        candidate = max(choosing_dict)
        return CRYPTOS[choosing_dict[candidate]]
    print(f"Kandydat nie istnieje")
    return False
def candidateUtil():
    candidateUtil = candidate()
    if candidateUtil:
        for index,crypto in enumerate(CRYPTOS):
            if crypto == candidateUtil:
                return index
    return False  
def volatileUtil(buy_list, X=10, Y=5):
    Y_list = buy_list[-Y:]
    value = (abs(max(Y_list) - min(Y_list)) / max(Y_list)) * 100
    if value > X:
        return 1
    return 0
def liquidUtil(buy_list, sell_list, S=4):
    bid = sell_list[-1]
    ask = buy_list[-1]
    spread = ((ask - bid) / ask ) * 100
    if spread < S:
        return 1
    return 0
def titleUtil(bid,ask):
    volt = volatileUtil(bid)
    liquid = liquidUtil(bid,ask)

    if volt == 0 and liquid == 0:
        return "No assets"
    elif volt == 1 and liquid == 0:
        return "Volatile asset"
    elif volt == 1 and liquid == 1:
        return "Volatile and liquid assets"
    elif volt == 0 and liquid == 1:
        return "Liquid asset" 
def x_val_limit(x_val):
    if len(x_val) >= 5:
        x = int(len(x_val) // 5)
        x_val = x_val[::x + 1]
    return x_val
def dataslist(currency):
    bid, ask = datas(f"{CRYPTOS[0]}{currency}")
    BTCbid.append(bid)
    BTCask.append(ask)
    BTCvol.append(volume(CRYPTOS[0],CURRENCY))
    BTCaskavg.append(averange(BTCask,5))
    DASH_buy_avg.append(avg(DASH_buy_value))
    rsi_askBTC.append(calc_RSI(BTCask, 4, 7))
    rsi_bidBTC.append(calc_RSI(BTCbid, 4, 7))   
    bid, ask= datas(f"{CRYPTOS[1]}{currency}")
    ETHbid.append(bid)
    ETHask.append(ask)
    ETHvol.append(volume(CRYPTOS[1],CURRENCY))
    ETHaskavg.append(averange(ETHask,5))
    LTC_buy_avg.append(avg(LTC_buy_value))
    rsi_askETH.append(calc_RSI(ETHask, 4, 7))
    rsi_bidETH.append(calc_RSI(ETHbid, 4, 7))
    bid, ask= datas(f"{CRYPTOS[2]}{currency}")
    OMGbid.append(bid)
    OMGask.append(ask)
    OMGvol.append(volume(CRYPTOS[2],CURRENCY))  
    OMGaskavg.append(averange(OMGask,5))
    LSK_buy_avg.append(avg(LSK_buy_value))
    rsi_askOMG.append(calc_RSI(OMGask, 4, 7))
    rsi_bidOMG.append(calc_RSI(OMGbid, 4, 7))
def plot(i):
    time = dt.datetime.now()
    x.append(time.strftime('%H:%M:%S'))
    x_val = x_val_limit(x)
    dataslist("PLN")
    trendlist(rsi_askBTC,rsi_askETH,rsi_askOMG)
    candidate = candidateUtil()


    ax[0][0].cla()
    ax[0][0].plot(x,BTCbid,'b', label = "BTCbid")
    ax[0][0].plot(x,BTCask,'r',label = "BTCask")
    ax[0][0].set_xlim(auto = 1)
    ax[0][0].set_xticks(x_val)
    ax[0][0].set_xticklabels(x_val, rotation=45)
    ax[0][0].set_title(f"{CRYPTOS[0]} values")
    if candidate == 0:
        ax[0][0].set_title(f"Kandydat",loc="left",fontsize = "xx-small")
        ax[0][0].set_title(f"{titleUtil(BTCbid,BTCask)}",loc="right",fontsize = "xx-small")
    ax[0][0].set_ylabel('Value [PLN]')
    ax[0][0].set_xlabel('Time')
    ax[0][0].text(0.3, 0.2, f"Volume: {round(BTCvol[-1],3)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[0][0].transAxes)
    
    ax[0][1].cla()
    ax[0][1].plot(x,rsi_askBTC,'c', label = "BTCrsi")
    ax[0][1].set_xlim(auto = 1)
    ax[0][1].set_title(f"RSI for {CRYPTOS[0]} ")
    ax[0][1].set_xticks(x_val)
    ax[0][1].set_xticklabels(x_val, rotation=45)
    ax[0][1].set_ylabel('Points')
    ax[0][1].set_xlabel('Time')
    ax[0][1].text(0.3, 0.2, f"{trend(rsi_askBTC)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[0][1].transAxes)
    ax[0][2].cla()
    ax[0][2].plot(x,BTCaskavg,'k--',label = "BTCavgask")
    ax[0][2].set_title(f"Mean for {CRYPTOS[0]} ask")
    ax[0][2].set_xticks(x_val)
    ax[0][2].set_xticklabels(x_val, rotation=45)
    ax[0][2].set_ylabel('Value [PLN]')
    ax[0][2].set_xlabel('Time')
   
    ax[0][3].cla()
    ax[0][3].plot(x,DASH_buy_avg,'m--',label = "DASH_buy_avg")
    ax[0][3].set_xticks(x_val)
    ax[0][3].set_xticklabels(x_val, rotation=45)
    ax[0][3].set_title(f"Mean for {CRYPTOS[0]} buy")
    ax[0][3].set_ylabel('Value [PLN]')
    ax[0][3].set_xlabel('Time')


    ax[1][0].cla()
    ax[1][0].plot(x,ETHbid,'b', label = "ETHbid")
    ax[1][0].plot(x,ETHask,'r',label = "ETHask")
    ax[1][0].set_xlim(auto = 1)
    ax[1][0].set_xticks(x_val)
    ax[1][0].set_xticklabels(x_val, rotation=45)
    ax[1][0].set_title(f"{CRYPTOS[1]} values")
    if candidate == 1:
        ax[1][0].set_title(f"Kandydat",loc="left",fontsize = "xx-small")
        ax[1][0].set_title(f"{titleUtil(ETHbid,ETHask)}",loc="right",fontsize = "xx-small")
    ax[1][0].set_ylabel('Value [PLN]')
    ax[1][0].set_xlabel('Time')
    ax[1][0].text(0.3, 0.2, f"Volume: {round(ETHvol[-1],3)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[1][0].transAxes)
    ax[1][1].cla()
    ax[1][1].plot(x,rsi_askETH,'c', label = "ETHrsi")
    ax[1][1].set_xlim(auto = 1)
    ax[1][1].set_xticks(x_val)
    ax[1][1].set_xticklabels(x_val, rotation=45)
    ax[1][1].set_title(f"RSI for {CRYPTOS[1]} ")
    ax[1][1].set_ylabel('Points')
    ax[1][1].set_xlabel('Time')
    ax[1][1].text(0.3, 0.2, f"{trend(rsi_askETH)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[1][1].transAxes)
    ax[1][2].cla()
    ax[1][2].plot(x,ETHaskavg,'k--',label = "ETHavgask")
    ax[1][2].set_title(f"Mean for {CRYPTOS[1]} ask")
    ax[1][2].set_xticks(x_val)
    ax[1][2].set_xticklabels(x_val, rotation=45)
    ax[1][2].set_ylabel('Value [PLN]')
    ax[1][2].set_xlabel('Time')

    ax[1][3].cla()
    ax[1][3].plot(x,LTC_buy_avg,'m--',label = "LTC_buy_avg")
    ax[1][3].set_xticks(x_val)
    ax[1][3].set_xticklabels(x_val, rotation=45)
    ax[1][3].set_title(f"Mean for {CRYPTOS[1]} buy")
    ax[1][3].set_ylabel('Value [PLN]')
    ax[1][3].set_xlabel('Time')
    
    ax[2][0].cla()
    ax[2][0].plot(x,OMGbid,'b', label = "OMGbid")
    ax[2][0].plot(x,OMGask,'r',label = "OMGask")
    ax[2][0].set_xlim(auto = 1)
    ax[2][0].set_xticks(x_val)
    ax[2][0].set_xticklabels(x_val, rotation=45)
    ax[2][0].set_title(f"{CRYPTOS[2]} values")
    if candidate == 2:
        ax[2][0].set_title(f"Kandydat",loc="left",fontsize = "xx-small")
        ax[2][0].set_title(f"{titleUtil(OMGbid,OMGask)}",loc="right",fontsize = "xx-small")
    ax[2][0].set_ylabel('Value [PLN]')
    ax[2][0].set_xlabel('Time')
    ax[2][0].text(0.3, 0.2, f"Volume: {round(OMGvol[-1],3)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[2][0].transAxes)
    ax[2][1].cla()
    ax[2][1].plot(x,rsi_askOMG,'c', label = "OMGrsi")
    ax[2][1].set_xlim(auto = 1)
    ax[2][1].set_xticks(x_val)
    ax[2][1].set_xticklabels(x_val, rotation=45)
    ax[2][1].set_title(f"RSI for {CRYPTOS[2]} ")
    ax[2][1].set_ylabel('Points')
    ax[2][1].set_xlabel('Time')
    ax[2][1].text(0.3, 0.2, f"{trend(rsi_askOMG)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[2][1].transAxes)
    
    ax[2][2].cla()
    ax[2][2].plot(x,OMGaskavg,'k--',label = "OMGavgask")
    ax[2][2].set_title(f"Mean for {CRYPTOS[2]} ask")
    ax[2][2].set_xticks(x_val)
    ax[2][2].set_xticklabels(x_val, rotation=45)
    ax[2][2].set_ylabel('Value [PLN]')
    ax[2][2].set_xlabel('Time')

    ax[2][3].cla()
    ax[2][3].plot(x,LSK_buy_avg,'m--',label = "LSK_buy_avg")
    ax[2][3].set_title(f"Mean for {CRYPTOS[2]} buy")
    ax[2][3].set_xticks(x_val)
    ax[2][3].set_xticklabels(x_val, rotation=45)
    ax[2][3].set_ylabel('Value [PLN]')
    ax[2][3].set_xlabel('Time')
    fig.legend(["bid","ask","rsi","avg","buy"],loc = 'upper left', prop = {'size':10}, title =  "Legenda")



# CRYPTOS = ["BTC","ETH","OMG"]
CRYPTOS = ["DASH","LTC","LSK"]
CURRENCY = "PLN"


if __name__ == '__main__':
    
#__________________________#
#      ZMIENNE DLA API     # 
#__________________________#
    DASH_buy = []
    DASH_buy_value = []
    DASH_buy_avg = []
    DASH_sell = []
    DASH_sell_value = []
    DASH_sell_avg = []
    LTC_buy = []
    LTC_buy_value = []
    LTC_buy_avg = []
    LTC_sell = []
    LTC_sell_value = []
    LTC_sell_avg = []
    LSK_buy = []
    LSK_buy_value = []
    LSK_buy_avg = []
    LSK_sell = []
    LSK_sell_value = []
    LSK_sell_avg = []

#__________________________#
#           API            # 
#__________________________#
    app = Flask(__name__)
    @app.route('/')
    def main():
        json_read()
        return render_template('main.html')
    @app.route('/buy',methods=['GET','POST'])
    def buy():
        option = 1
        data = request.form.to_dict()
        print(data)
        volume = int(data['volume'])
        value = int(data['value'])
        crypto = readconf(file = "config.ini",topic="crypto")
        datas = [volume,value]
        making_list(option,datas,crypto)
        updateconf("1","config.ini","user")
        returndata(1)
        json_save(crypto,option,datas)
        return render_template('main.html')
    @app.route('/sell',methods=['GET','POST'])
    def sell():
        option = 2
        data = request.form.to_dict()
        volume = int(data['volume'])
        value = int(data['value'])
        crypto = readconf(file = "config.ini",topic="crypto")
        datas = [volume,value]
        making_list(option,datas,crypto)
        updateconf("1","config.ini","user")
        update_balance()
        return render_template('main.html')
    @app.route('/crypto',methods=['GET','POST'])
    def crypto():
        data = request.form.to_dict()
        print(data)
        cryptocurr = data['crypto']
        updateconf(cryptocurr,file = "config.ini",topic="crypto")
        return render_template('main.html')
    @app.route('/balance',methods=['GET','POST'])
    def balance():
        data = readconf("config.ini","balance")
        print(data)
        return render_template('main.html')
    
    app.run(port = 5050, debug = True)
  
    #__________________________#
    #   ZMIENNE DLA WYKRESOW   # 
    #__________________________#
    x = []
    BTCbid = []
    BTCask = []
    BTCvol = []
    BTCaskavg = []
    rsi_bidBTC = []
    rsi_askBTC = []
    ETHbid = []
    ETHask = []
    ETHvol = []
    ETHaskavg = []
    rsi_bidETH = []
    rsi_askETH = []
    OMGbid = []
    OMGask = []
    OMGvol = []
    OMGaskavg = []
    rsi_bidOMG = []
    rsi_askOMG = []
#__________________________#
#    OBSLUGA   WYKRESOW    # 
#__________________________#
    fig, ax = plt.subplots(3,4,tight_layout=True)
    ani = FuncAnimation(fig, plot, interval=5000)
    plt.show()