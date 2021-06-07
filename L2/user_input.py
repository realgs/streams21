import csv
import pandas as pd


def write_csv(curren, amount, ask, current_time, mode):
    fieldnames = ['curr', 'amount', 'ask_cur', 'time']

    with open(path_file, mode) as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if mode == 'w':
            csv_writer.writeheader()

        info = {
            'curr': curren,
            'amount': amount,
            'ask_cur': ask,
            'time': current_time,
        }

        csv_writer.writerow(info)


def choose_currency():
    t = '1, 2 or 3'
    print(f'Choose cryptocurrency({t}): ')
    while True:
        try:
            number = int(input("Type number: "))
            if number in [1, 2, 3]:
                return number
            else:
                print('\nInvalid number')
                print(t)
        except Exception as err:
            print(err)
            print(t)


def amount():
    print(f'Choose amount: ')
    while True:
        try:
            number = int(input("Type number: "))
            if number > 0:
                return number
            else:
                print('\nInvalid number')
                print('Type positive number')
        except Exception as err:
            print(err)
            print('Type positive number')


def ask(curr):
    data = pd.read_csv('data.csv')
    ask = 0
    if curr == 1:
        ask = data['ask_cur1']
    elif curr == 2:
        ask = data['ask_cur2']
    elif curr == 3:
        ask = data['ask_cur3']
    min_ask = min(ask)
    min_final = min_ask  # - 0.1*min_ask

    max_ask = max(ask)
    max_final = max_ask  # + 0.1*max_ask
    message = f'Type ask price beetwen {min_final} and {max_final}: '
    print(message)
    while True:
        try:
            number = float(input("Type number: "))
            if min_final <= number <= max_final:
                return number
            else:
                print('\nInvalid number')
                print(message)
        except Exception as err:
            print(err)
            print(message)


def decision():
    while True:
        try:
            decision = input("Y\\N? :")
            decision = decision.upper()
            if decision == 'Y':
                return True
            elif decision == 'N':
                return False
            else:
                print('Wrong input')

        except Exception as err:
            print(err)


def input_data(current_time, mode):
    cur = choose_currency()
    quan = amount()
    ask_val = ask(cur)

    write_csv(cur, quan, ask_val, current_time, mode)


def get_time():
    data = pd.read_csv('data.csv')
    val = list(data['x_val'])
    time = list(data['time'])
    return val[-1], time[-1]


def delete_row(element):
    lines = list()
    with open(path_file, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)

    sold_row = lines[element]
    try:
        lines.pop(element)
    except Exception as err:
        print('Cant pop that element')
        print(err)

    with open(path_file, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    return sold_row


def choose_row_for_sale():
    lines = dict()
    with open(path_file, 'r') as readFile:
        reader = csv.reader(readFile)
        count = 0
        for row in reader:
            lines[count] = row
            count += 1
    lines.pop(0)
    for id, row in lines.items():
        print(id, row)
    print('Type transaction number to be sold: ')
    while True:
        try:
            number = int(input("Type number: "))
            if number in [number + 1 for number in range(len(lines))]:
                return number
            else:
                print('\nInvalid number')
        except Exception as err:
            print(err)


def bid_price(curr):
    data = pd.read_csv('data.csv')
    ask = [0, 2]
    if curr == 1:
        ask = data['bid_cur1']
    elif curr == 2:
        ask = data['bid_cur2']
    elif curr == 3:
        ask = data['bid_cur3']
    min_ask = min(ask)
    min_final = min_ask  # - 0.1*min_ask

    max_ask = max(ask)
    max_final = max_ask  # + 0.1*max_ask
    message = f'Type bid price beetwen {min_final} and {max_final}: '
    print(message)
    while True:
        try:
            number = float(input("Type number: "))
            if min_final <= number <= max_final:
                return number
            else:
                print('\nInvalid number')
                print(message)
        except Exception as err:
            print(err)
            print(message)


def count_profit(row, profit):
    total_ask = float(row[1]) * float(row[2])
    price = bid_price(int(row[0]))
    total_bid = float(row[1]) * price
    profit[int(row[0])-1] += total_bid - total_ask



def write_profit(profit):
    fieldnames = ['prof1', 'prof2', 'prof3']

    with open('profit.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        csv_writer.writeheader()

        info = {
            'prof1': profit[0],
            'prof2': profit[1],
            'prof3': profit[2]
        }

        csv_writer.writerow(info)


if __name__ == '__main__':


    path_file = 'user_input.csv'
    print('Use historic input data?')
    if decision():
        mode = 'a+'
        data_profit = pd.read_csv('profit.csv')
        profit = [data_profit['prof1'], data_profit['prof2'], data_profit['prof3']]
    else:
        mode = 'w'
        profit = [0, 0, 0]
    while True:
        current_time = get_time()
        print(f'Pass data in current time? \n{current_time[1]}')
        if decision():
            input_data(current_time[0]-1, mode)
        mode = 'a+'
        print('\nDo you want to sell something?')
        if decision():
            row_for_sale = choose_row_for_sale()
            sold_row = delete_row(row_for_sale)
            count_profit(sold_row, profit)
            write_profit(profit)
