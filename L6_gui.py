import tkinter as tk
import json
from datetime import datetime, timedelta
import time

root = tk.Tk()
root.title("Adding data- Crypto Currencies")

cur_var = tk.StringVar()
amount_var = tk.StringVar()
price_var = tk.StringVar()

title = tk.Label(root, text="Buy- information", font=('Helvetica', 14, 'bold'))
title.grid(row=0, column=3, columnspan=4)

curr_label = tk.Label ( root, text="Currency: " )
curr_label.grid ( row=2, column=0, columnspan=4 )

currency = tk.Entry ( root, textvariable=cur_var )
currency.grid ( row=2, column=7, columnspan=2 )

amt_label = tk.Label ( root, text="Amount of currency bought: " )
amt_label.grid ( row=3, column=0, columnspan=4 )

amount = tk.Entry ( root, textvariable=amount_var )
amount.grid ( row=3, column=7, columnspan=2 )

price_label = tk.Label ( root, text="Price of bought asset: " )
price_label.grid ( row=4, column=0, columnspan=4 )

price = tk.Entry ( root, textvariable=price_var )
price.grid ( row=4, column=7, columnspan=2 )


def submit_buy():
    crypto = cur_var.get ()
    amt = int ( amount_var.get () )
    price = int ( price_var.get () )

    small_cryptos = ['btc', 'ltc', 'eth']

    lower = crypto.lower ()

    input_data = {}

    for i in small_cryptos:
        if lower == i:
            upper = lower.upper ()
            input_data["currency"] = upper
            input_data["amount"] = amt
            input_data["price"] = price
            input_data['time'] = time.strftime ( "%H:%M:%S", time.localtime () )

        else:
            continue

    with open ( "buy.json", "a" ) as file_object:
        file_object.write ( json.dumps ( input_data ) + '\n' )

    cur_var.set ( "" )
    amount_var.set ( "" )
    price_var.set ( "" )


sub_btn = tk.Button ( root, text='Submit', command=submit_buy )
sub_btn.grid ( row=5, column=5 )

cur_var_sell = tk.StringVar ()
amount_var_sell = tk.StringVar ()
price_var_sell = tk.StringVar ()

title_sell = tk.Label ( root, text="Sell- information", font=('Helvetica', 14, 'bold') )
title_sell.grid ( row=6, column=3, columnspan=4 )

curr_label_sell = tk.Label ( root, text="Currency: " )
curr_label_sell.grid ( row=7, column=0, columnspan=4 )

currency_sell = tk.Entry ( root, textvariable=cur_var_sell )
currency_sell.grid ( row=7, column=7, columnspan=2 )

amt_label_sell = tk.Label ( root, text="Amount of currency bought: " )
amt_label_sell.grid ( row=8, column=0, columnspan=4 )

amount_sell = tk.Entry ( root, textvariable=amount_var_sell )
amount_sell.grid ( row=8, column=7, columnspan=2 )

price_label_sell = tk.Label ( root, text="Price of bought asset: " )
price_label_sell.grid ( row=9, column=0, columnspan=4 )

price_sell = tk.Entry ( root, textvariable=price_var_sell )
price_sell.grid ( row=9, column=7, columnspan=2 )


def submit_sell():
    crypto_sell = cur_var_sell.get ()
    amt_sell = int ( amount_var_sell.get () )
    price_sell = int ( price_var_sell.get () )

    input_data = {}
    small_cryptos = ['btc', 'ltc', 'eth']

    lower = crypto_sell.lower ()

    for i in small_cryptos:
        if lower == i:
            input_data["amount"] = amt_sell
            upper = lower.upper ()
            input_data["currency"] = upper
            input_data["price"] = price_sell
            input_data['time'] = time.strftime ( "%H:%M:%S", time.localtime () )

        else:
            continue

    with open ( "sell.json", "a" ) as file_object:
        file_object.write ( json.dumps ( input_data ) + '\n' )

    cur_var_sell.set ( "" )
    amount_var_sell.set ( "" )
    price_var_sell.set ( "" )


sub_btn_sell = tk.Button ( root, text='Submit', command=submit_sell )
sub_btn_sell.grid ( row=10, column=5 )

root.mainloop ()
