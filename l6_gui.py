import json
from tkinter import *

def file_to_read():
    entered_name = 'file1.json'
    return entered_name

def save_app_data():
    #file1 = crypto_chosen.get()
    total_amount = 0
    buying_price = 0

    cryptocurr = variable.get()
    type1 = variable_1.get()
    amount = float(Text_2.get())
    price = float(Text_1.get())
    print(cryptocurr,type1,amount,price)

    if type1 == "Buy":
        file = open(file_name, 'r')
        json_data = json.load(file)
        file.close()

        json_data[cryptocurr].append([amount, price])
        file = open(file_name, 'w')
        json.dump(json_data, file)
        file.close()

    elif type1 == "Sell":
        file = open(file_name, 'r')
        json_data = json.load(file)
        file.close()
        crypto_amount = json_data[cryptocurr]

        for i in range(len(crypto_amount)):
            total_amount += crypto_amount[i][0]

        if amount > total_amount:
            print(f'You do not have enough this crypto to sell it.')
        else:
            counter = 0
            j = 0
            while counter < amount:
                if crypto_amount[j][0] >= amount:
                    buying_price += crypto_amount[j][1]*amount
                    crypto_amount[j][0] -=  amount
                    counter += amount
                elif (crypto_amount[j][0]+counter < amount) and crypto_amount[j][0] > 0:
                    buying_price += crypto_amount[j][1] * crypto_amount[j][0]
                    counter += crypto_amount[j][0]
                    crypto_amount[j][0] = 0
                elif (crypto_amount[j][0] + counter > amount) and crypto_amount[j][0] > 0:
                    temp = amount-counter
                    buying_price += crypto_amount[j][1] * temp
                    counter += temp
                    crypto_amount[j][0] -= temp
                elif crypto_amount[j][0] == 0:
                    j = j + 1

            seling_price = (amount * price)
            profit = seling_price - buying_price

            for i in range(0, len(crypto_amount)):
                if crypto_amount[0][0] == 0:
                    del crypto_amount[0]

            json_data[cryptocurr] = crypto_amount
            file = open(file_name, 'w')
            json.dump(json_data, file)
            file.close()

            file_profit = open('sell_values_json.json', 'r')
            profit_data = json.load(file_profit)
            file_profit.close()
            profit_data[cryptocurr].append(profit)

            file_profit = open('sell_values_json.json', 'w')
            json.dump(profit_data, file_profit)
            file_profit.close()

def clearing_json_file():
    with open(file_name, 'w') as file:
        json_data = {}
        json_data["ETH"] = []
        json_data["LTC"] = []
        json_data["DASH"] = []
        json.dump(json_data, file)
        file.close()

def clearing_profit_file():
    with open('sell_values_json.json', 'w') as file:
        json_data = {}
        json_data["ETH"] = []
        json_data["LTC"] = []
        json_data["DASH"] = []
        json.dump(json_data, file)
        file.close()
def buying_window():
    global variable,variable_1,Text_2,Text_1

    root =Tk()
    img = PhotoImage(file='btc_logo.png')
    root.iconphoto(False, img)
    root.title("Crypto buying window")
    root.geometry("300x300")
    #Canvas(root, width = 1000, height = 800)
    crytpo_list = ["ETH","LTC","DASH"]
    crytpo_to_chose= Label(root,text = "Which crypto?",font=('Montserrat',10))
    crytpo_to_chose.pack()

    variable = StringVar(root)
    variable.set("ETH") # default value
    crypto_chosen = OptionMenu(root, variable, *crytpo_list)
    crypto_chosen.pack()

    crytpo_buy_sell= Label(root,text = "Do you want to buy or sell crypto?",font=('Montserrat',10))
    crytpo_buy_sell.pack()

    variable_1 = StringVar(root)
    variable_1.set("Buy") # default value
    crypto_buy_sell = OptionMenu(root, variable_1, "Buy","Sell")
    crypto_buy_sell.pack()

    crytpo_to_amout= Label(root,text = "Enter the amount of selected crypto:",font=('Montserrat',10))
    crytpo_to_amout.pack()
    Text_2 = Entry(root)
    Text_2.pack()

    crytpo_to_price= Label(root,text = "Enter the price of selected crypto:",font=('Montserrat',10))
    crytpo_to_price.pack()
    Text_1 = Entry(root)
    Text_1.pack()

    button_confirm = Button(root, text='Confirm',command= save_app_data,font=('Montserrat',10))
    button_confirm.configure(background='royalblue', width=10)
    button_confirm.pack(expand=True)

    clearing = Button(root, text='Clear json file', font=('Montserrat',10), command=clearing_json_file)
    clearing.pack(expand=True)
    clearing.configure(background='red')

    clearing = Button(root, text='Clear profit file', font=('Montserrat',10), command=clearing_profit_file)
    clearing.pack(expand=True)
    clearing.configure(background='red')

    root.mainloop()
file_name = file_to_read()
buying_window()

