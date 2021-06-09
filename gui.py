from tkinter import *
import json


def file_to_read():
    print("Podaj nazwe pliku do odczytu, lub wpisz 0 jesli chcesz skorzystac z domyslnego pliku:")
    entered_name = str(input())
    if entered_name == '0':
        entered_name = 'buyjson.json'

    text_file = open('name_of_file.txt', 'w')
    text_file.write(entered_name)
    text_file.close()
    return entered_name


def collecting_data():
    buying_price = 0
    total_amount = 0
    which_crypto = variable1.get()
    buy_sell = variable2.get()
    how_much = float(how_much_entry.get())
    price = float(price_entry.get())

    print(which_crypto, buy_sell, how_much, price)

    if buy_sell == "Buy":
        file = open(FILE_NAME, 'r')
        json_data = json.load(file)
        print(json_data)
        file.close()

        json_data[which_crypto].append([how_much, price])
        file = open(FILE_NAME, 'w')
        json.dump(json_data, file)
        file.close()

    if buy_sell == "Sell":
        file = open(FILE_NAME, 'r')
        json_data = json.load(file)
        file.close()
        crypto_amount = json_data[which_crypto]
        for i in range(len(crypto_amount)):
            total_amount += crypto_amount[i][0]

        if how_much > total_amount:
            print("Nie masz tylu dostepnych kryptowalut")

        else:
            profit = (how_much * price)
            while how_much:
                if how_much < crypto_amount[0][0]:
                    crypto_amount[0][0] -= how_much
                    profit -= how_much * crypto_amount[0][1]
                    how_much = 0
                elif how_much == crypto_amount[0][0]:
                    crypto_amount[0][0] -= how_much
                    profit -= how_much * crypto_amount[0][1]
                    how_much = 0
                    crypto_amount.pop(0)
                else:
                    how_much -= crypto_amount[0][0]
                    profit -= how_much * crypto_amount[0][1]
                    crypto_amount[0][0] = 0
                    crypto_amount.pop(0)

            json_data[which_crypto] = crypto_amount
            file = open(FILE_NAME, 'w')
            json.dump(json_data, file)
            file.close()

            file_profit = open('selljson.json', 'r')
            profit_data = json.load(file_profit)
            file_profit.close()
            profit_data[which_crypto].append(profit)

            file_profit = open('selljson.json', 'w')
            json.dump(profit_data, file_profit)
            file_profit.close()


def gui_window():
    global variable1, variable2, how_much_entry, price_entry
    window = Tk()

    window.configure(background='white')
    window.title('Gui')
    window.geometry("300x600")

    chose_crypto = Label(window, text='Chose crypto id:', font=('arialbold', 17))
    chose_crypto.pack(expand=True)
    chose_crypto.configure(background='white')

    variable1 = StringVar(window)
    options = OptionMenu(window, variable1, "LTC", 'ETH', "DASH")
    variable1.set("-----")
    options.config(width=32, background='#6B6969', font=('arialbold', 17))
    options.pack(expand=True)
    options.configure(background='gray', width=20)

    chose_sell_buy = Label(window, text='Do you want to sell or buy?:', font=('arialbold', 17))
    chose_sell_buy.pack(expand=True)
    chose_sell_buy.configure(background='white')

    variable2 = StringVar(window)
    options = OptionMenu(window, variable2, 'Sell', 'Buy')
    variable2.set("-----")
    options.config(width=32, background='#6B6969', font=('arialbold', 17))
    options.pack(expand=True)
    options.configure(background='gray', width=20)

    how_much = Label(window, text='How much of crypto?:', font=('arialbold', 17))
    how_much.pack(expand=True)
    how_much.configure(background='white')

    how_much_entry = Entry(window, font=('arialbold', 17))
    how_much_entry.configure(background='gray', width=20)
    how_much_entry.pack(expand=True)

    price = Label(window, text='What is the price?:', font=('arialbold', 17))
    price.pack(expand=True)
    price.configure(background='white')

    price_entry = Entry(window, font=('arialbold', 17))
    price_entry.configure(background='gray', width=20)
    price_entry.pack(expand=True)

    confirmation = Button(window, text='Confirm', font=('arialbold', 17), command=collecting_data)
    confirmation.pack(expand=True)
    confirmation.configure(background='green')

    window.mainloop()


FILE_NAME = file_to_read()
gui_window()
