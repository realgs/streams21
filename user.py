import json
import os
import time


def reset():
    confirmation = input("Are you sure? [y/N]: ")
    if confirmation == "y":
        if os.path.exists("data/buy.json"):
            os.remove("data/buy.json")
        if os.path.exists("data/profits_and_prices.json"):
            os.remove("data/profits_and_prices.json")
        # generate empty files
        check_if_files_exist()
        print("Done")
    else:
        print("Not removed")


def current_profit_price(currency, to_return, printing=False):
    profit_file = open("data/profits_and_prices.json", "r")
    profit_data = json.load(profit_file)
    profit_file.close()
    if to_return == 0:
        if printing:
            print(f"Your current profit: {profit_data[currency][0]}")
        else:
            return profit_data[currency][0]
    if to_return == 1:
        if printing:
            print(f"Your current buy price: {profit_data[currency][1]}")
        else:
            return profit_data[currency][1]
    if to_return == 2:
        try:
            return profit_data[currency]
        except KeyError:
            # if there is no information about this currency
            return [0, 0]


def average_price(currency):
    buy_file = open("data/buy.json", "r")
    buy_data = json.load(buy_file)
    buy_file.close()
    quantity = 0
    price = 0
    for transaction in buy_data[currency]:
        quantity += transaction[0]
        price += transaction[0] * transaction[1]
    try:
        average = price / quantity
    except ZeroDivisionError:
        average = 0

    profit_file = open("data/profits_and_prices.json", "r")
    profit_data = json.load(profit_file)
    profit_file.close()
    if currency not in profit_data.keys():
        profit_data[currency] = [0, average]
    else:
        profit_data[currency][1] = average
    profit_file = open("data/profits_and_prices.json", "w")
    json.dump(profit_data, profit_file)
    profit_file.close()


def buy(currency, quantity, price):
    buy_file = open("data/buy.json", "r")
    buy_data = json.load(buy_file)
    buy_file.close()
    if currency not in buy_data.keys():
        buy_data[currency] = list()
        buy_data[currency].append([quantity, price])
    else:
        buy_data[currency].append([quantity, price])
    buy_file = open("data/buy.json", "w")
    json.dump(buy_data, buy_file)
    buy_file.close()
    average_price(currency)


def sell(currency, quantity, price):
    buy_file = open("data/buy.json", "r")
    buy_data = json.load(buy_file)
    buy_file.close()
    profit = quantity * price
    while quantity:
        try:
            temp = buy_data[currency].pop(0)
        except IndexError:
            print("You cannot sell more currency than you own! Try again...")
            return

        if quantity < temp[0]:
            buy_data[currency].insert(0, [temp[0]-quantity, temp[1]])
            profit -= (quantity * temp[1])
            break
        elif quantity == temp[0]:
            profit -= (quantity * temp[1])
            break
        else:
            profit -= (temp[0] * temp[1])
            quantity -= temp[0]

    buy_file = open("data/buy.json", "w")
    json.dump(buy_data, buy_file)
    buy_file.close()

    profit_file = open("data/profits_and_prices.json", "r")
    profit_data = json.load(profit_file)
    profit_file.close()
    if currency not in profit_data.keys():
        profit_data[currency] = [profit, 0]
    else:
        profit_data[currency][0] = profit_data[currency][0] + profit
    profit_file = open("data/profits_and_prices.json", "w")
    json.dump(profit_data, profit_file)
    profit_file.close()
    average_price(currency)


def check_if_files_exist():
    try:
        buy_file = open("data/buy.json", "r")
    except FileNotFoundError:
        to_write = dict()
        buy_file = open("data/buy.json", "a+")
        json.dump(to_write, buy_file)
    buy_file.close()

    try:
        profit_file = open("data/profits_and_prices.json", "r")
    except FileNotFoundError:
        to_write = dict()
        profit_file = open("data/profits_and_prices.json", "a+")
        json.dump(to_write, profit_file)
    profit_file.close()


def main():
    check_if_files_exist()
    while True:
        user_command = input(">> ").split()
        if len(user_command) == 1 and user_command[0] == "help":
            print("Enter the command according to the template:")
            print("<buy/sell> <currency pair> <quantity> <price>")
            continue

        elif len(user_command) == 1 and user_command[0] == "exit":
            print("Bye!")
            time.sleep(2)
            break

        elif len(user_command) == 1 and user_command[0] == "reset":
            reset()
            continue

        if len(user_command) != 4:
            print("Wrong command structure! Try again...")
            continue

        try:
            user_command[2] = float(user_command[2])
        except ValueError:
            print("Quantity must be a number! Try again...")
            continue

        try:
            user_command[3] = float(user_command[3])
        except ValueError:
            print("Price must be a number! Try again...")
            continue

        if user_command[0] == "buy":
            buy(user_command[1].upper(), user_command[2], user_command[3])
        elif user_command[0] == "sell":
            sell(user_command[1].upper(), user_command[2], user_command[3])
        else:
            print("Unknown command")
            print("Please use buy/sell command:")


if __name__ == "__main__":
    print("Type 'help' for more information")
    main()
