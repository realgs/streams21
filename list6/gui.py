from tkinter import *
from datetime import datetime
import json
import os

window = Tk()
window.title('Buy or sell cryptocurrencies')
window.geometry("400x600")
CURRENCIES = ['BTC', 'BCC', 'ETH']


def getFileName():
    which_file = int(if_new_file.get())
    if which_file == 1:
        name = str(e1.get()) + '.txt'
        f = open(name, 'a+')

        if os.path.getsize(name) == 0:
            data = {"average_BTC_json": 0, "average_BCC_json": 0, "average_ETH_json": 0, "saldo_BTC_json": 0,
                    "saldo_BCC_json": 0, "saldo_ETH_json": 0, "list_BTC_json": [], "list_BCC_json": [],
                    "list_ETH_json": []}
            json.dump(data, f)
        f.close()

        return name
    if which_file == 2:
        return str('database.txt')


def buy():
    t, amount, index, price, crypto_amt = update_average('BUY')
    listbox.insert(END,
                   '{time} - kupiono {units_val} {crypt_val} po {price_val} PLN'.format(time=t, units_val=amount,
                                                                                        crypt_val=CURRENCIES[
                                                                                            index],
                                                                                        price_val=price))


def sell():
    t, amount, index, price, crypto_amt = update_average('SELL')
    if amount <= crypto_amt:
        listbox.insert(END,
                       '{time} - sprzedano {units_val} {crypt_val} po {price_val} PLN'.format(time=t, units_val=amount,
                                                                                              crypt_val=CURRENCIES[
                                                                                                  index],
                                                                                              price_val=price))


def count_average(action, index, amt, price, file_name, time):
    currency = CURRENCIES[index]

    f = open(file_name, "r")
    data = json.load(f)

    transactions = data[f'list_{currency}_json']
    currency_amt = len(transactions)

    if action == 'BUY':

        for i in range(amt):
            transactions.append(price)
        data[f'saldo_{currency}_json'] -= price * amt

    elif action == 'SELL':
        if amt > currency_amt:
            listbox.insert(END,
                           '{time} - za mało waluty, aktualnie posiadasz {units_val} {crypt_val}'.format(time=time,
                                                                                                         units_val=currency_amt,
                                                                                                         crypt_val=currency))
            return currency_amt
        else:
            del transactions[:amt]
            data[f'saldo_{currency}_json'] += price * amt

    try:
        average = sum(transactions) / len(transactions)
        if average == 0 or data[f'average_{currency}_json'] == 0:
            data[f'average_{currency}_json'] = None
        else:
            data[f'average_{currency}_json'] = average
    except ZeroDivisionError:
        data[f'average_{currency}_json'] = None

    f.close()
    g = open(file_name, 'w')
    json.dump(data, g)
    g.close()
    return currency_amt


def update_average(sell_or_buy):
    t = datetime.now().strftime("%H:%M:%S")

    action = sell_or_buy

    index = currency.get()
    amount = int(e2.get())
    price = float(e3.get())
    f_name = getFileName()

    no_of_cryptocurrency = count_average(action, index, amount, price, f_name, t)
    return t, amount, index, price, no_of_cryptocurrency


if_new_file = IntVar()
l1 = Label(window, text="Would you like to open your file or use default?", font=("arial bold", 14))
r1 = Radiobutton(window, text="My file", value=1, variable=if_new_file, font=('arial', 10))
r2 = Radiobutton(window, text="Default", value=2, variable=if_new_file, font=('arial', 10))
l2 = Label(window, text="Enter name for your file", font=("arial bold", 12))
e1 = Entry(window, width=30, font=("arial bold", 11))
l1.pack()
r1.pack(anchor=W)
r2.pack(anchor=W)
l2.pack(anchor=W)
e1.pack(fill=X)

currency = IntVar()
l3 = Label(window, text="Choose the currency you'd like to buy or sell", font=("arial bold", 14))
r3 = Radiobutton(window, text="BTC", value=0, variable=currency, font=('arial', 10))
r4 = Radiobutton(window, text="BCC", value=1, variable=currency, font=('arial', 10))
r5 = Radiobutton(window, text="ETH", value=2, variable=currency, font=('arial', 10))
l3.pack(anchor=W)
r3.pack(anchor=W)
r4.pack(anchor=W)
r5.pack(anchor=W)

l4 = Label(window, text="Enter the amount", font=("arial bold", 14))
e2 = Entry(window, width=30, font=("arial bold", 11))
l4.pack(anchor=W)
e2.pack(fill=X)


l5 = Label(window, text="Enter the price", font=("arial bold", 14))
e3 = Entry(window, width=30, font=("arial bold", 11))
l5.pack(anchor=W)
e3.pack(fill=X)

button1 = Button(window, text="Buy", command=buy, bg="green", fg='white', font=("arial bold", 14),
                 activebackground='white')
button2 = Button(window, text="Sell", command=sell, bg="red", fg="white", font=("arial bold", 14),
                 activebackground='white')
button3 = Button(window, text="Exit", command=exit, bg="blue", fg="white", font=("arial bold", 14),
                 activebackground='white')
listbox = Listbox(window)

button1.pack(fill=X)
button2.pack(fill=X)
button3.pack(fill=X)
listbox.pack(fill=X)

window.mainloop()
