import time
import json

FILE_NAME = 'customer_transaction'

f = open(f"C:\\Users\\Lenovo\\PycharmProjects\\L6\\{FILE_NAME}.json", "r")
data = json.load(f)
f.close()

# to co klient kupił
cust_LSK_for_how_much_buy = data['cust_LSK_for_how_much_buy']
cust_LSK_number_buy = data['cust_LSK_number_buy_help']

cust_ETH_for_how_much_buy = data['cust_ETH_for_how_much_buy']
cust_ETH_number_buy = data['cust_ETH_number_buy_help']

cust_LTC_for_how_much_buy = data['cust_LTC_for_how_much_buy']
cust_LTC_number_buy = data['cust_LTC_number_buy_help']

average_LSK_buy = []
average_ETH_buy = []
average_LTC_buy = []

# to co klient sprzedał
cust_LSK_for_how_much_sold = []
cust_LSK_number_sold = []

cust_ETH_for_how_much_sold = []
cust_ETH_number_sold = []

cust_LTC_for_how_much_sold = []
cust_LTC_number_sold = []

# average_LSK_sold = []
# average_ETH_sold = []
# average_LTC_sold = []


def average(cust_for_how_much, cust_number):
    suma_kosztow = 0
    if sum(cust_number) == 0:
        return 0
    if cust_for_how_much == [] or cust_number == [] :
        if cust_for_how_much == data['cust_LSK_for_how_much_buy']  and cust_number == data['cust_LSK_number_buy_help']:
            return data['average_LSK_buy'][-1]
        if cust_for_how_much == data['cust_ETH_for_how_much_buy']  and cust_number == data['cust_ETH_number_buy_help']:
            return data['average_ETH_buy'][-1]
        if cust_for_how_much == data['cust_LTC_for_how_much_buy']  and cust_number == data['cust_LTC_number_buy_help']:
            return data['average_LTC_buy'][-1]
        else:
            return
    else:
        for i in range(len(cust_for_how_much)):
            for j in range(len(cust_number)):
                if i == j:
                    suma_kosztow += cust_for_how_much[i]*cust_number[j]
        suma_ilosci = sum(cust_number)
        average1 = suma_kosztow / suma_ilosci
        return average1


flag = True
while flag:
    f = open(f"C:\\Users\\Lenovo\\PycharmProjects\\L6\\{FILE_NAME}.json", "r")
    data = json.load(f)
    f.close()

    LSK_profit_loss = "nie ma ani zysku ani straty"
    ETH_profit_loss = "nie ma ani zysku ani straty"
    LTC_profit_loss = "nie ma ani zysku ani straty"

    buying = input('czy kupiles cos t/n: ')

    if buying == 't':
        what_buy = (input('Co kupiles: '))
        for_how_much_buy = int(input('Za ile kupiles: '))
        number_buy = int(input('W jakiej ilosci kupiles: '))

        if what_buy == 'LSK':
            # cust_LSK_for_how_much_buy.append(for_how_much_buy)
            # cust_LSK_number_buy.append(number_buy)

            data['cust_LSK_for_how_much_buy'].append(for_how_much_buy)
            data['cust_LSK_number_buy'].append(number_buy)

            data['cust_LSK_number_buy_help'].append(number_buy)

        if what_buy == 'ETH':
            # cust_ETH_for_how_much_buy.append(for_how_much_buy)
            # cust_ETH_number_buy.append(number_buy)

            data['cust_ETH_for_how_much_buy'].append(for_how_much_buy)
            data['cust_ETH_number_buy'].append(number_buy)

            data['cust_ETH_number_buy_help'].append(number_buy)

        if what_buy == 'LTC':
            # cust_LTC_for_how_much_buy.append(for_how_much_buy)
            # cust_LTC_number_buy.append(number_buy)

            data['cust_LTC_for_how_much_buy'].append(for_how_much_buy)
            data['cust_LTC_number_buy'].append(number_buy)

            data['cust_LTC_number_buy_help'].append(number_buy)

    solding = input('czy sprzedales cos t/n: ')
    if solding == 't':
        what_sold = (input('Co sprzedales: '))
        for_how_much_sold = int(input('Za ile sprzedales: '))
        number_sold = int(input('W jakiej ilosci sprzedales: '))


        if what_sold == 'LSK':
            cust_LSK_for_how_much_sold.append(for_how_much_sold) # 3 000
            cust_LSK_number_sold.append(number_sold) # 1

            data['cust_LSK_for_how_much_sold'].append(for_how_much_sold)
            data['cust_LSK_number_sold'].append(number_sold)

            counter1 = 0
            i1 = 0
            profit_loss1 = 0
            flag1 = True
            while flag1:
                counter1 += data['cust_LSK_number_buy_help'][i1] # 2
                profit_loss1 += data['cust_LSK_for_how_much_buy'][i1] * data['cust_LSK_number_buy_help'][i1] #  30 000* 2
                # cust_LSK_number_buy[i1] = 0
                data['cust_LSK_number_buy_help'][i1] = 0
                if counter1 > number_sold or counter1 == number_sold: # True
                    data['cust_LSK_number_buy_help'][i1] = counter1 - number_sold # 1) 17 -12  -> 2)  2 - 1 = 1
                    help_main_profit_loss1 = profit_loss1 - data['cust_LSK_number_buy_help'][i1] * data['cust_LSK_for_how_much_buy'][i1]  #  1) 5 * 20 -> 2) 60 000 - 1 * 30 000 = 30 000
                    main_profit_loss1 = for_how_much_sold * number_sold - help_main_profit_loss1 # 3 000 * 1 - 30  000
                    if main_profit_loss1 > 0:
                        LSK_profit_loss = "zysk"
                    if main_profit_loss1 < 0:
                        LSK_profit_loss = "strata"
                    if main_profit_loss1 == 0:
                        LSK_profit_loss = "nie ma ani zysku ani straty"
                    data['LSK_profit_loss1'].append(LSK_profit_loss)
                    #
                    flag1 = False
                i1 += 1


        if what_sold == 'ETH':
            cust_ETH_for_how_much_sold.append(for_how_much_sold)
            cust_ETH_number_sold.append(number_sold)

            data['cust_ETH_for_how_much_sold'].append(for_how_much_sold)
            data['cust_ETH_number_sold'].append(number_sold)

            counter2 = 0
            i2 = 0
            profit_loss2 = 0
            flag2 = True
            while flag2:
                counter2 += data['cust_ETH_number_buy'][i2]
                profit_loss2 += data['cust_ETH_for_how_much_buy'][i2] * data['cust_ETH_number_buy_help'][i2]
                data['cust_ETH_number_buy_help'][i2] = 0
                if counter2 > number_sold or counter2 == number_sold:
                    data['cust_ETH_number_buy_help'][i2] = counter2 - number_sold
                    # main_profit_loss2 = profit_loss2 - cust_ETH_number_buy[i2] * cust_ETH_for_how_much_buy[i2]  # 5 * 20
                    help_main_profit_loss2 = profit_loss2 - data['cust_ETH_number_buy_help'][i2] * data['cust_ETH_for_how_much_buy'][i2]
                    main_profit_loss2 = for_how_much_sold * number_sold - help_main_profit_loss2
                    if main_profit_loss2 > 0:
                        ETh_profit_loss = "zysk"
                    if main_profit_loss2 < 0:
                        ETH_profit_loss = "strata"
                    if main_profit_loss2 == 0:
                        ETH_profit_loss = "nie ma ani zysku ani straty"
                    data['ETH_profit_loss1'].append(ETH_profit_loss)
                    #
                    flag2 = False
                i2 += 1


        if what_sold == 'LTC':
            cust_LTC_for_how_much_sold.append(for_how_much_sold)
            cust_LTC_number_sold.append(number_sold)

            data['cust_LTC_for_how_much_sold'].append(for_how_much_sold)
            data['cust_LTC_number_sold'].append(number_sold)

            counter3 = 0
            i3 = 0
            profit_loss3 = 0
            flag3 = True
            while flag3:
                counter3 += data['cust_LTC_number_buy_help'][i3]
                profit_loss3 += data['cust_LTC_for_how_much_buy'][i3] * data['cust_LTC_number_buy_help'][i3]
                data['cust_LTC_number_buy_help'][i3] = 0
                if counter3 > number_sold or counter3 == number_sold:
                    data['cust_LTC_number_buy_help'][i3] = counter3 - number_sold
                    # main_profit_loss3 = profit_loss3 - cust_LTC_number_buy[i3] * cust_LTC_for_how_much_buy[i3]  # 5 * 20
                    help_main_profit_loss3 = profit_loss3 - data['cust_LTC_number_buy_help'][i3] * data['cust_LTC_for_how_much_buy'][i3]
                    main_profit_loss3 = for_how_much_sold * number_sold - help_main_profit_loss3
                    if main_profit_loss3 > 0:
                        LTC_profit_loss = "zysk"
                    if main_profit_loss3 < 0:
                        LTC_profit_loss = "strata"
                    if main_profit_loss3 == 0:
                        LTC_profit_loss = "nie ma ani zysku ani straty"
                    data['LTC_profit_loss1'].append(LTC_profit_loss)
                    #
                    flag3 = False
                i3 += 1


    # average_LSK_sold.append(average(data['cust_LSK_for_how_much_sold'], data['cust_LSK_number_sold']))
    # average_ETH_sold.append(average(data['cust_ETH_for_how_much_sold'], data['cust_ETH_number_sold']))
    # average_LTC_sold.append(average(data['cust_LTC_for_how_much_sold'], data['cust_LTC_number_sold']))
    #
    # data['average_LSK_sold'].append(average(data['cust_LSK_for_how_much_sold'], data['cust_LSK_number_sold']))
    # data['average_ETH_sold'].append(average(data['cust_ETH_for_how_much_sold'], data['cust_ETH_number_sold']))
    # data['average_LTC_sold'].append(average(data['cust_LTC_for_how_much_sold'], data['cust_LTC_number_sold']))

    average_LSK_buy.append(average(data['cust_LSK_for_how_much_buy'], data['cust_LSK_number_buy_help']))
    average_ETH_buy.append(average(data['cust_ETH_for_how_much_buy'], data['cust_ETH_number_buy_help']))
    average_LTC_buy.append(average(data['cust_LTC_for_how_much_buy'], data['cust_LTC_number_buy_help']))

    data['average_LSK_buy'].append(average(data['cust_LSK_for_how_much_buy'], data['cust_LSK_number_buy_help']))
    data['average_ETH_buy'].append(average(data['cust_ETH_for_how_much_buy'], data['cust_ETH_number_buy_help']))
    data['average_LTC_buy'].append(average(data['cust_LTC_for_how_much_buy'], data['cust_LTC_number_buy_help']))

    g = open(f"C:\\Users\\Lenovo\\PycharmProjects\\L6\\{FILE_NAME}.json", "w")
    json.dump(data, g)
    g.close()

    answer1 = input('Czy chcesz zakonczyc: t/n: ')

    print('LSK')
    print(data['cust_LSK_for_how_much_buy'])
    print(data['cust_LSK_number_buy'])
    print('srednia za kupione akcje', data['average_LSK_buy'][-1])
    # print('srednia za sprzedane akcje', data['average_LSK_sold'][-1])
    print(LSK_profit_loss)

    print('ETH')
    print(data['cust_ETH_for_how_much_buy'])
    print(data['cust_ETH_number_buy'])
    print('srednia za kupione akcje', data['average_ETH_buy'][-1])
    # print('srednia za sprzedane akcje', data['average_ETH_sold'][-1])
    print(ETH_profit_loss)

    print('LTC')
    print(data['cust_LTC_for_how_much_buy'])
    print(data['cust_LTC_number_buy'])
    print('srednia za kupione akcje', data['average_LTC_buy'][-1])
    # print('srednia za sprzedane akcje', data['average_LTC_sold'][-1])
    print(LTC_profit_loss)

    time.sleep(3)

    if answer1 == 't':
        flag = False
