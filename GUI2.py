from tkinter import *
import json
import time

window = Tk()
window.geometry('390x230')
choose = IntVar()

window.title('Crypto to visualize')
introduce_label = Label(window, text='Choose currency and input values', font=('Helvetica', 15, 'bold'))
button_BTC = Radiobutton(window, text='BTC',font=('Helvetica', 7, 'bold'), variable=choose, value=0)
button_LTC = Radiobutton(window, text='LTC', font=('Helvetica', 7, 'bold'), variable=choose, value=1)
button_TRX = Radiobutton(window, text='TRX', font=('Helvetica', 7, 'bold'), variable=choose, value=2)
label_buy_amount = Label(window, text='Input the amount of currency purchased:', font=('Helvetica', 10, 'normal'))
entry_buy_amount = Entry(window)
label_buy_price = Label(window, text='Input the price of the purchased currency:', font=('Helvetica', 10, 'normal'))
entry_buy_price = Entry(window)
label_sell_amount = Label(window, text='Input the amount of currency sold:', font=('Helvetica', 10, 'normal'))
entry_sell_amount = Entry(window)
label_sell_cost = Label(window, text='Input the price of the sold currency:', font=('Helvetica', 10, 'normal'))
entry_sell_cost = Entry(window)


def check():
    buy_amount = int(entry_buy_amount.get())
    buy_price = float(entry_buy_price.get())
    sell_amount = int(entry_sell_amount.get())
    sell_price = float(entry_sell_cost.get())
    currency = float(choose.get())

    def choose_value():
        if currency == 0:
            value = 'BTC-PLN'
            return value
        elif currency == 1:
            value = 'LTC-PLN'
            return value
        elif currency == 2:
            value = 'TRX-PLN'
            return value
    value = choose_value()
    data = {'currency': value, 'buy amount': buy_amount, 'buy price': buy_price, 'sell amount': sell_amount, 'sell_price': sell_price, 'time': time.strftime('%H:%M:%S', time.localtime())}
    with open('CRYPTO2.json', 'a') as file:
        file.write(json.dumps(data) + '\n')

submit = Button(window, text='Submit', command=check).grid(row=8, column=1)

introduce_label.grid(row=0, column=0, columnspan=2)
button_LTC.grid(row=1, column=0)
button_BTC.grid(row=2, column=0)
button_TRX.grid(row=3, column=0)
label_buy_amount.grid(row=4, column=0)
entry_buy_amount.grid(row=4, column=1)
label_buy_price.grid(row=5, column=0)
entry_buy_price.grid(row=5, column=1)
label_sell_amount.grid(row=6, column=0)
entry_sell_amount.grid(row=6, column=1)
label_sell_cost.grid(row=7, column=0)
entry_sell_cost.grid(row=7, column=1)


window.mainloop()