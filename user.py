import json
import os
import pprint
import subprocess
import time

import sender
import helper
import archives


def run():
    check_if_files_exist()
    run_file = open("data/run.txt", "w")
    run_file.write("True")
    run_file.close()
    subprocess.Popen(["python", "visualize.py"])
    time.sleep(3)


def stop():
    check_if_files_exist()
    run_file = open("data/run.txt", "w")
    run_file.write("False")
    run_file.close()


def reset():
    confirmation = input("Are you sure? [y/N]: ")
    if confirmation == "y":
        if os.path.exists("data/buy.json"):
            os.remove("data/buy.json")
        if os.path.exists("data/profits_and_prices.json"):
            os.remove("data/profits_and_prices.json")
        if os.path.exists("data/archives.json"):
            os.remove("data/archives.json")
        # generate empty files
        check_if_files_exist()
        print("Done")
    else:
        print("Not removed")


def current_profit_price(currency, to_return, printing=False):
    profit_file = open("data/profits_and_prices.json", "r")
    profit_data = json.load(profit_file)
    profit_file.close()
    # get profit
    if to_return == 0:
        if currency not in profit_data.keys():
            return False
        if printing:
            print(f"Your current profit: {profit_data[currency][0]}")
        else:
            return profit_data[currency][0]
    # get price
    if to_return == 1:
        if currency not in profit_data.keys():
            return False
        if printing:
            print(f"Your current buy price: {profit_data[currency][1]}")
        else:
            return profit_data[currency][1]
    # get both
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


def get_property(currency=None):
    buy_file = open("data/buy.json", "r")
    buy_data = json.load(buy_file)
    buy_file.close()

    if currency is None:
        return buy_data
    elif currency in buy_data.keys():
        return buy_data[currency]
    else:
        print("There is nothing to show")
        return {}


def buy(currency, quantity, price):
    buy_file = open("data/buy.json", "r")
    buy_data = json.load(buy_file)
    buy_file.close()
    if currency not in buy_data.keys():
        archive_file = open("data/archives.json", "r")
        archive_data = json.load(archive_file)
        archive_file.close()
        if currency not in archive_data.keys():
            confirmation = input("This is new currency in your wallet. \nAre you sure that it is typed correctly? "
                                 "[y/N]: ")
        else:
            confirmation = "y"

        if confirmation == "y":
            buy_data[currency] = list()
            buy_data[currency].append([quantity, price])
        else:
            print("Not added")
            return
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
    to_archive = list()
    while quantity:
        try:
            temp = buy_data[currency].pop(0)
        except IndexError:
            print("You cannot sell more currency than you own! Try again...")
            return
        except KeyError:
            print(f"You do not have currency: {currency}")
            return

        if quantity < temp[0]:
            buy_data[currency].insert(0, [temp[0]-quantity, temp[1]])
            profit -= (quantity * temp[1])
            to_archive.append([quantity, temp[1]])
            break
        elif quantity == temp[0]:
            profit -= (quantity * temp[1])
            to_archive.append(temp)
            break
        else:
            profit -= (temp[0] * temp[1])
            quantity -= temp[0]
            to_archive.append(temp)

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
    archives.archive(currency, to_archive)


def check_if_files_exist():
    to_write = dict()
    try:
        buy_file = open("data/buy.json", "r")
    except FileNotFoundError:
        buy_file = open("data/buy.json", "a+")
        json.dump(to_write, buy_file)
    buy_file.close()

    try:
        profit_file = open("data/profits_and_prices.json", "r")
    except FileNotFoundError:
        profit_file = open("data/profits_and_prices.json", "a+")
        json.dump(to_write, profit_file)
    profit_file.close()

    try:
        archive_file = open("data/archives.json", "r")
    except FileNotFoundError:
        archive_file = open("data/archives.json", "a+")
        json.dump(to_write, archive_file)
    archive_file.close()

    try:
        run_file = open("data/run.txt", "r")
    except FileNotFoundError:
        run_file = open("data/run.txt", "a+")
        run_file.write("True")
    run_file.close()


def main():
    check_if_files_exist()
    while True:
        user_command = input(">> ").split()
        if not user_command:
            continue

        """additional commands"""
        if len(user_command) == 1 and user_command[0] == "help":
            print("Enter the command according to the template:")
            print("<buy/sell> <currency pair> <quantity> <price>")
            print("\nAdditionally: exit, reset, profit, price, archive, property, send, run, stop")
            print("Type 'help <command name>' to get more information about specific command")
            continue

        elif len(user_command) == 2 and user_command[0] == "help":
            helper.helps(user_command[1])
            continue

        elif len(user_command) == 1 and user_command[0] == "exit":
            print("Bye!")
            stop()
            break

        elif len(user_command) == 1 and user_command[0] == "reset":
            reset()
            continue

        elif len(user_command) == 1 and user_command[0] == "run":
            run()
            continue

        elif len(user_command) == 1 and user_command[0] == "stop":
            stop()
            continue

        elif len(user_command) == 2 and user_command[0] == "profit":
            res = current_profit_price(user_command[1].upper(), 0)
            if res:
                print(f"Your current profit from {user_command[1].upper()}: {res}")
            else:
                print(f"There is no information about '{user_command[1]}'")
            continue

        elif len(user_command) == 2 and user_command[0] == "price":
            res = current_profit_price(user_command[1].upper(), 1)
            if res:
                print(f"Your current buy price of {user_command[1].upper()}: {res}")
            else:
                print(f"There is no information about '{user_command[1]}'")
            continue

        elif len(user_command) in list(range(1, 3)) and user_command[0] == "archive":
            if len(user_command) == 1:
                pprint.pprint(archives.get_archive())
            else:
                pprint.pprint(archives.get_archive(user_command[1].upper()))
            continue

        elif len(user_command) in list(range(1, 3)) and user_command[0] == "property":
            if len(user_command) == 1:
                pprint.pprint(get_property())
            else:
                pprint.pprint(get_property(user_command[1].upper()))
            continue

        elif len(user_command) in list(range(3, 5)) and user_command[0] == "send":
            if len(user_command) == 3:
                sender.send(user_command[1], user_command[2])
            else:
                sender.send(user_command[1], user_command[2], user_command[3])
            continue

        """buy/sell commands"""
        if len(user_command) != 4:
            print("Wrong command! Type 'help' for more information.")
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
