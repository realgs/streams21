#import tkinter as tk
from tkinter import *
from datetime import datetime
import json
import os


window = Tk()
window.geometry("400x600")
action = IntVar()
crypt = IntVar()

def start_chart():
    os.system('python main.py')

def erase_data():
    f = open("database.txt", 'r+')
    f.truncate()
    f.close()

    g = open("database.txt", 'w')
    data = {"average_OMG_json": 0, "average_BTC_json": 0, "average_ETH_json": 0, "saldo_OMG_json": 0, "saldo_BTC_json": 0, "saldo_ETH_json": 0, "list_OMG_json": [], "list_BTC_json": [], "list_ETH_json": []}
    json.dump(data, g)
    g.close()
    print(read_json())

def read_json(path = "database.txt"):
    f = open(path, 'r')
    data = json.load(f)
    return data

def count_average(action_ind, crypt, units, cost):
    currency_list = ['', 'OMG', 'BTC', 'ETH']
    action_list = ['', 'BUY', 'SELL']

    currency = currency_list[crypt]
    action = action_list[action_ind]

    f = open("database.txt", "r")
    data = json.load(f)

    transactions = data[f'list_{currency}_json']
    if action == 'BUY':

        for i in range(units):
            transactions.append(cost/units)
        data[f'saldo_{currency}_json'] -= cost

    elif action == 'SELL':

        del transactions[:units]
        data[f'saldo_{currency}_json'] += cost

    try:
        average = sum(transactions) / len(transactions)
        data[f'average_{currency}_json'] = average
    except ZeroDivisionError:
        data[f'average_{currency}_json'] = 0

    f.close()
    g = open("database.txt", 'w')
    json.dump(data, g)
    g.close()
    print(read_json("database.txt"))


def update_average():
    currency_list = ['', 'OMG', 'BTC', 'ETH']

    T = datetime.now().strftime("%H:%M:%S")

    crypt_ind = crypt.get()
    action_ind = action.get()
    units = int(entry1.get())
    cost = int(entry2.get())

    if action_ind == 1:
        listbox.insert(END, '{time} -- kupiono {units_val} {crypt_val} za {cost_val} PLN'.format(time= T, units_val= units,
                                                                                                  crypt_val= currency_list[crypt_ind],
                                                                                                  cost_val= cost))

    else:
        listbox.insert(END, '{time} -- sprzedano {units_val} {crypt_val} za {cost_val} PLN'.format(time=T, units_val=units,
                                                                                             crypt_val=currency_list[crypt_ind],
                                                                                                   cost_val=cost))

    count_average(action_ind, crypt_ind, units, cost)



start_label = Label(window, text="Choose the action", font=("arial bold", 14))
start1_label = Label(window, text = "buy / sell", font=("arial bold", 14))
start2_label = Label(window, text = "Choose the currency", font=("arial bold", 14))
start3_label = Label(window, text = "Enter the total cost", font=("arial bold", 14))
start4_label = Label(window, text = "Enter the number of units", font=("arial bold", 14))

entry1 = Entry(window, width= 30, font= ("arial bold", 11))
entry2 = Entry(window, width= 30, font= ("arial bold", 11))

rad1 = Radiobutton(window, text="OMG", value = 1, variable=crypt)
rad2 = Radiobutton(window, text="BTC", value = 2, variable=crypt)
rad3 = Radiobutton(window, text="ETH", value = 3, variable=crypt)

rad4 = Radiobutton(window, text="BUY", value = 1, variable=action)
rad5 = Radiobutton(window, text="SELL", value = 2, variable=action)

button1 = Button(window, text="Accept", command= update_average, bg="white", fg= 'green', font=("arial bold", 14), activebackground= 'green')
button2 = Button(window, text="Exit", command= exit, bg="white", fg="red", font=("arial bold", 14), activebackground= 'red')
button3 = Button(window, text= "Erase", command= erase_data, bg= "white", fg= "blue", font=("arial bold", 14), activebackground= 'blue')
#button4 = Button(window, text= "Start chart", command= start_chart, bg= 'white', font= ("arial bold", 14))
listbox = Listbox(window)

start_label.pack()
start1_label.pack()
rad4.pack()
rad5.pack()
start2_label.pack()
rad1.pack()
rad2.pack()
rad3.pack()

start4_label.pack()
entry1.pack()
start3_label.pack()
entry2.pack()

button1.pack(fill=X)
button2.pack(fill=X)
button3.pack(fill=X)
#button4.pack(fill=X)
listbox.pack(fill=X)

window.mainloop()