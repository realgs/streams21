from tkinter import *
import json


def read_file():
    file_name = 'buy_json.json'
    text_file = open('file_name.txt', 'w')
    text_file.write(file_name)
    text_file.close()

    return file_name


def read_other_file():
    print("Podaj nazwe pliku do odczytu:")
    file_name = str(input())

    text_file = open('file_name.txt', 'w')
    text_file.write(file_name)
    text_file.close()
    return file_name


def clean_buy():
    file = open(FILE_NAME, 'r')
    json_data = json.load(file)
    file.close()

    json_data["LSK"] = []
    json_data["BCP"] = []
    json_data["GNT"] = []

    file = open(FILE_NAME, 'w')
    json.dump(json_data, file)
    file.close()


def clean_sell():
    file = open('sell_json.json', 'r')
    json_data = json.load(file)
    file.close()

    json_data["LSK"] = []
    json_data["BCP"] = []
    json_data["GNT"] = []

    file = open('sell_json.json', 'w')
    json.dump(json_data, file)
    file.close()

def clean_all_date():
    clean_sell()
    clean_buy()


def window_tk():
    global currency, action, amount_value, price_value, file_name

    window = Tk()

    window.configure(background='snow4')
    window.title('Buy and Sell')
    window.geometry("600x600")

    currencies = ["LSK", "BCP", "GNT"]
    actions = ["BUY", "SELL"]

    chose_currency = Label(window, text='Chose currency', font=('Calibri', 17), fg='white')
    chose_currency.pack(expand=True)
    chose_currency.configure(background='snow4')

    currency = StringVar(window)
    which_option = OptionMenu(window, currency, *currencies)
    currency.set("-----")
    which_option.config(width=32, background='snow2', font=('Calibri', 17), fg='snow4')
    which_option.pack(expand=True)
    which_option.configure(background='snow4', width=20)

    b_or_s = Label(window, text='Buy or sell?', font=('Calibri', 17), fg='white')
    b_or_s.pack(expand=True)
    b_or_s.configure(background='snow4')

    action = StringVar(window)
    action.set("-----")
    which_action = OptionMenu(window, action, *actions)
    which_action.config(width=32, background='snow2', font=('Calibri', 17), fg='snow4')
    which_action.pack(expand=True)
    which_action.configure(background='snow4', width=20)

    price_label = Label(window, text='Price:', font=('Calibri', 17), fg='white')
    price_label.pack(expand=True)
    price_label.configure(background='snow4')

    price_value = Entry(window, font=('Calibri', 17), fg='snow4')
    price_value.configure(background='snow2', width=20)
    price_value.pack(expand=True)

    amount_label = Label(window, text='Amount:', font=('Calibri', 17), fg='white')
    amount_label.pack(expand=True)
    amount_label.configure(background='snow4')

    amount_value = Entry(window, font=('Calibri', 17), fg='snow4')
    amount_value.configure(background='snow2', width=20)
    amount_value.pack(expand=True)

    clean = Button(window, text='CLEAN BUY FILE', font=('Calibri', 17), fg='snow4', command=clean_buy)
    clean.pack(anchor="s", side=LEFT)
    clean.configure(background='snow4')

    clean1 = Button(window, text='CLEAN GAIN FILE', font=('Calibri', 17), fg='snow4', command=clean_sell)
    clean1.pack(anchor="s", side=RIGHT)
    clean1.configure(background='snow4')

    clean2 = Button(window, text='CLEAN ALL FILES', font=('Calibri', 17), fg='snow4', command=clean_all_date)
    clean2.pack(side=BOTTOM)
    clean2.configure(background='snow4')

    confirmation = Button(window, text='CONFIRM', font=('Calibri', 17), fg='snow4', command=save_data)
    confirmation.pack(expand=True)
    confirmation.configure(background='snow4')

    window.mainloop()


def save_data():

    total_amount = 0
    buying_price = 0
    which_currency = currency.get()
    buy_sell = action.get()
    how_much = float(amount_value.get())
    price = float(price_value.get())

    if buy_sell == "BUY":
        file = open(FILE_NAME, 'r')
        json_data = json.load(file)
        file.close()

        json_data[which_currency].append([how_much, price])
        file = open(FILE_NAME, 'w')
        json.dump(json_data, file)

        file.close()

    if buy_sell == "SELL":

        file = open(FILE_NAME, 'r')
        json_data = json.load(file)
        file.close()

        currency_amount = json_data[which_currency]
        for i in range(len(currency_amount)):
            total_amount += currency_amount[i][0]

        if how_much > total_amount:
            print("Nie masz tylu zakupionych walut")

        else:

            counter = 0
            j = 0
            while counter < how_much:
                if currency_amount[j][0] > 0:
                    buying_price += currency_amount[j][1]
                    currency_amount[j][0] = currency_amount[j][0] - 1
                    counter += 1

                elif currency_amount[j][0] == 0:
                    j = j + 1

            seling_price = (how_much * price)
            profit = seling_price - buying_price

            for i in range(0, len(currency_amount)):
                if currency_amount[0][0] == 0:
                    del currency_amount[0]

                else:
                    break

            json_data[which_currency] = currency_amount
            file = open(FILE_NAME, 'w')
            json.dump(json_data, file)
            file.close()

            file_gain = open('sell_json.json', 'r')
            profit_data = json.load(file_gain)
            file_gain.close()
            profit_data[which_currency].append(profit)

            file_gain = open('sell_json.json', 'w')
            json.dump(profit_data, file_gain)
            file_gain.close()

    amount_value.delete(0, 'end')
    price_value.delete(0, 'end')


if __name__ == "__main__":

    print("Jesli chcesz skorzystac z pliku istniejacymi z danymi nacisnij 1, jezeli nie wybierz 2")
    y_or_n = str(input())
    if y_or_n == '1':
        FILE_NAME = read_other_file()
    else:
        FILE_NAME = read_file()
    window_tk()
