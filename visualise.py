from tkinter import *
import json
from tkinter.filedialog import asksaveasfile
import tkinter.ttk as ttk
import tkinter.messagebox as msb

# def read_new_lines_from_json(current_data):
#     new_data = []
#     with open('file.json', 'r') as file:
#         all_data = [json.loads(line) for line in file]
#         # print(all_data)
#     for i in range (len(current_data), len(all_data)):
#         new_data.append(all_data[i])
#     return new_data

def check():
    amount_value = float(Amount.get())
    price_value = float(Price.get())
    action_value = float(action.get())
    action_ = 'buy' if action_value == 1.0 else 'sell'
    currency_= combobox.get()
    print(amount_value)
    print(price_value)
    data = {'Currency': currency_, 'Amount': amount_value, 'Price': price_value, 'Action': action_}
    print(data)
    with open('file.json', 'a') as file:
        file.write(json.dumps(data) + '\n')

if __name__ == '__main__':

    window = Tk()
    window.geometry('340x200')
    window.title('Market')

    CURRENCIES = ['ETH-PLN', 'BTC-PLN', 'LTC-PLN']
    box_value = StringVar()
    currency = Label(window, text="Currency:")
    combobox = ttk.Combobox(window)
    combobox['values'] = CURRENCIES

    action = IntVar()
    buy_button = Radiobutton(window, text="Buy", variable=action, value=1)
    sell_button = Radiobutton(window, text="Sell", variable=action, value=2)

    amount = Label(window, text="Amount:")
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
    # a = []
    # read_new_lines_from_json(a)
    window.mainloop()

