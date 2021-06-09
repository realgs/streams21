from tkinter import *
import json
import tkinter.ttk as ttk



def check():
    samples = float(Amount.get())
    value = float(Price.get())
    currencies = float(action.get())
    action_ = 'buy' if currencies == 1.0 else 'sell'
    currency_= combobox.get()
    print(samples)
    print(value)
    data = {'Currencies': currency_, 'Samples': samples, 'Value': value, 'Action': action_}
    print(data)
    with open('file.json', 'a') as file:
        file.write(json.dumps(data) + '\n')

if __name__ == '__main__':

    window = Tk()
    window.geometry('340x200')
    window.title('Market')

    CURRENCIES = ['ETH-PLN', 'BTC-PLN', 'LTC-PLN']
    box_value = StringVar()
    currency = Label(window, text="Currencies:")
    combobox = ttk.Combobox(window)
    combobox['Values'] = CURRENCIES

    action = IntVar()
    buy_button = Radiobutton(window, text="Buy", variable=action, value=1)
    sell_button = Radiobutton(window, text="Sell", variable=action, value=2)

    amount = Label(window, text="Samples:")
    Amount = Entry(window)

    price = Label(window, text="Price:")
    Price = Entry(window)
    test = 1

    submit_button = Button(window, text='Accept', command=check).grid(row=4, column=1)

    buy_button.grid(row=0, column=0)
    sell_button.grid(row=0, column=1)
    currency.grid(row = 1,column = 0)
    combobox.grid(row=1, column=1)
    amount.grid(row=2, column=0)
    Amount.grid(row=2, column=1)
    price.grid(row=3,column=0)
    Price.grid(row=3, column=1)

    window.mainloop()