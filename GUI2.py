from tkinter import *
import tkinter.ttk
import json

window = Tk()
window.geometry('390x200')
choose = IntVar()
action_value = StringVar()

window.title('Crypto to visualize')

introduce_label = Label(window, text='Choose currency and input values', font=('Helvetica', 15, 'bold'))
button_BTC = Radiobutton(window, text='BTC', font=('Helvetica', 7, 'bold'), variable=choose, value=0)
button_LTC = Radiobutton(window, text='LTC', font=('Helvetica', 7, 'bold'), variable=choose, value=1)
button_TRX = Radiobutton(window, text='TRX', font=('Helvetica', 7, 'bold'), variable=choose, value=2)

combobox_label = Label(window, text='Choose action: ', font=('Helvetica', 10, 'normal'))
combobox_action = tkinter.ttk.Combobox(window, values=['buy', 'sell'])


label_amount = Label(window, text='Input the amount:', font=('Helvetica', 10, 'normal'))
entry_amount = Entry(window)
label_price = Label(window, text='Input the price:', font=('Helvetica', 10, 'normal'))
entry_price = Entry(window)


def check():
    amount = int(entry_amount.get())
    price = float(entry_price.get())
    currency = float(choose.get())

    def choose_value():
        if currency == 0:
            value_currency = 'BTC-PLN'
            return value_currency
        elif currency == 1:
            value_currency = 'LTC-PLN'
            return value_currency
        elif currency == 2:
            value_currency = 'TRX-PLN'
            return value_currency

    value_currency = choose_value()
    action = combobox_action.get()
    user_data = {'currency': value_currency, 'action': action,'amount': amount, 'price': price}

    f = open('user_value.json',)
    data = json.load(f)
    f.close()
    f = open('user_value.json', 'w')
    data.append(user_data)
    f.write(json.dumps(data))
    f.close()


submit = Button(window, text='Submit', command=check).grid(row=5, column=1)

introduce_label.grid(row=0, column=0, columnspan=2)
button_LTC.grid(row=1, column=0)
button_BTC.grid(row=1, column=1)
button_TRX.grid(row=1, column=2)
combobox_label.grid(row=2, column=0)
combobox_action.grid(row=2, column=1)
label_amount.grid(row=3, column=0)
entry_amount.grid(row=3, column=1)
label_price.grid(row=4, column=0)
entry_price.grid(row=4, column=1)

window.mainloop()