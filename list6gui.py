from tkinter import *
import json


def file_to_read():
    print("Podaj nazwe pliku do odczytu, lub wpisz 0 jesli chcesz skorzystac z domyslnego pliku:")
    entered_name = str(input())
    if entered_name == '0':
        entered_name = 'buy_json.json'

    text_file = open('file_name.txt', 'w')
    text_file.write(entered_name)
    text_file.close()
    return entered_name


def save_data():
    total_amount = 0
    buying_price = 0
    which_crypto = v.get()
    buy_sell = v1.get()
    how_much = int(amount_value.get())
    price = int(price_value.get())

    if buy_sell == "BUY":
        file = open(FILE_NAME, 'r')
        json_data = json.load(file)
        file.close()

        json_data[which_crypto].append([how_much, price])
        file = open(FILE_NAME, 'w')
        json.dump(json_data, file)
        file.close()

    if buy_sell == "SELL":
        file = open(FILE_NAME, 'r')
        json_data = json.load(file)
        file.close()
        crypto_amount = json_data[which_crypto]
        for i in range(len(crypto_amount)):
            total_amount += crypto_amount[i][0]

        if how_much > total_amount:
            print("Nie masz tylu dostepnych kryptowalut")

        else:

            counter = 0
            j = 0
            while counter < how_much:
                if crypto_amount[j][0] > 0:
                    buying_price += crypto_amount[j][1]
                    crypto_amount[j][0] = crypto_amount[j][0] - 1
                    counter += 1
                elif crypto_amount[j][0] == 0:
                    j = j + 1
            seling_price = (how_much * price)
            profit = seling_price - buying_price

            for i in range(0, len(crypto_amount)):
                if crypto_amount[0][0] == 0:
                    del crypto_amount[0]
                else:
                    break

            json_data[which_crypto] = crypto_amount
            file = open(FILE_NAME, 'w')
            json.dump(json_data, file)
            file.close()

            file_profit = open('sell_values_json.json', 'r')
            profit_data = json.load(file_profit)
            file_profit.close()
            profit_data[which_crypto].append(profit)

            file_profit = open('sell_values_json.json', 'w')
            json.dump(profit_data, file_profit)
            file_profit.close()


def clearing_json():
    file = open(FILE_NAME, 'r')
    json_data = json.load(file)
    file.close()
    json_data["BTC"] = []
    json_data["ETH"] = []
    json_data["ZEC"] = []
    file = open(FILE_NAME, 'w')
    json.dump(json_data, file)
    file.close()


def clearing_profit():
    file = open('sell_values_json.json', 'r')
    json_data = json.load(file)
    file.close()
    json_data["BTC"] = []
    json_data["ETH"] = []
    json_data["ZEC"] = []
    file = open('sell_values_json.json', 'w')
    json.dump(json_data, file)
    file.close()


def gui():
    global v, v1, amount_value, price_value, file_name
    window = Tk()

    window.configure(background='slategray')
    window.title('Buy & Sell')
    window.geometry("300x600")
    crypto_currencies = ["BTC", "ETH", "ZEC"]
    buy_or_sell = ["BUY", "SELL"]

    chose_crypto = Label(window, text='Chose crypto id:', font=('Calibri', 17), fg='white')
    chose_crypto.pack(expand=True)
    chose_crypto.configure(background='slategray')

    v = StringVar(window)
    options = OptionMenu(window, v, *crypto_currencies)
    v.set("-----")
    options.config(width=32, background='#6B6969', font=('Calibri', 17), fg='white')
    options.pack(expand=True)
    options.configure(background='steelblue', width=20)

    b_or_s = Label(window, text='Do you want to buy or sell?', font=('Calibri', 17), fg='white')
    b_or_s.pack(expand=True)
    b_or_s.configure(background='slategray')

    v1 = StringVar(window)
    v1.set("-----")
    what_to_do = OptionMenu(window, v1, *buy_or_sell)
    what_to_do.config(width=32, background='#6B6969', font=('Calibri', 17), fg='white')
    what_to_do.pack(expand=True)
    what_to_do.configure(background='steelblue', width=20)

    amount_label = Label(window, text='Amount:', font=('Calibri', 17), fg='white')
    amount_label.pack(expand=True)
    amount_label.configure(background='slategray')

    amount_value = Entry(window, font=('Calibri', 17), fg='white')
    amount_value.configure(background='steelblue', width=20)
    amount_value.pack(expand=True)

    price_label = Label(window, text='Price:', font=('Calibri', 17), fg='white')
    price_label.pack(expand=True)
    price_label.configure(background='slategray')

    price_value = Entry(window, font=('Calibri', 17), fg='white')
    price_value.configure(background='steelblue', width=20)
    price_value.pack(expand=True)

    confirmation = Button(window, text='CONFIRM', font=('Calibri', 17), fg='white', command=save_data)
    confirmation.pack(expand=True)
    confirmation.configure(background='seagreen')

    clearing = Button(window, text='CLEAR JSON FILE', font=('Calibri', 17), fg='white', command=clearing_json)
    clearing.pack(expand=True)
    clearing.configure(background='firebrick')

    clearing = Button(window, text='CLEAR PROFIT FILE', font=('Calibri', 17), fg='white', command=clearing_profit)
    clearing.pack(expand=True)
    clearing.configure(background='firebrick')

    window.mainloop()


FILE_NAME = file_to_read()
gui()
