from tkinter import *
import json
from tkinter.filedialog import asksaveasfile
import tkinter.ttk as ttk
import tkinter.messagebox as msb

window = Tk()
window.geometry('640x300')
window.title('Market')

CURRENCIES = ['ETH-PLN', 'BTC-PLN', 'LTC-PLN']
box_value = StringVar()
combobox = ttk.Combobox(window)
combobox['values'] = CURRENCIES
combobox.current(0)

# box_value = StringVar()
# locationBox = ttk.Combobox(master, textvariable=box_value)
# locationBox.bind("<<ComboboxSelected>>", self.justamethod())
# locationBox['values'] = CURRENCIES
# locationBox.current(0)



action = IntVar()
buy_button = Radiobutton(window, text="Buy", variable=action, value=1)
sell_button = Radiobutton(window, text="Sell", variable=action, value=2)

amount = Label(window, text="Amount:")
Amount = Entry(window)

price = Label(window, text="Price:")
Price = Entry(window)
test = 1



def check():
    amount_value = float(Amount.get())
    price_value = float(Price.get())
    action_value = float(action.get())
    currency_= combobox.get()
    print(amount_value)
    print(price_value)
    data = {'Currency': currency_, 'Amount': amount_value, 'Price': price_value, 'Action': action_value}
    print(data)
    with open('file.json', 'a') as file:
        file.write(json.dumps(data) + '\n')

submit_button = Button(window, text='Accept', command=check).grid(row=4, column=1)

buy_button.grid(row=1, column=0)
sell_button.grid(row=1, column=1)
combobox.grid(row=0, column=0)
amount.grid(row=2, column=0)
Amount.grid(row=2, column=1)
price.grid(row=3,column=0)
Price.grid(row=3, column=1)

window.mainloop()

