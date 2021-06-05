def user_info():
    curr = input('Waluta: ')
    ask = input('Kurs: ')
    vol = input('Ilość: ')

    return curr, int(ask), int(vol)


currencies = ['BTC']
n = len(currencies)

buy_rate = {}
buy_volume = {}
sell_rate = {}
sell_volume = {}

for currency in currencies:
    buy_rate[currency] = []
    buy_volume[currency] = []
    sell_rate[currency] = []
    sell_volume[currency] = []


t = 0
while True:
    t += 1
    if t % 10 == 0:
        czy = ''
        while czy != 'n':
            czy = input('Czy chcesz dodać tranzakcję?[t/n]: ')
            if czy == 't':
                czy2 = input('Kupno czy sprzedaż?[k/s]: ')
                if czy2 == 'k':
                    curre, asks, volu = user_info()
                    buy_rate[curre].append(asks)
                    buy_volume[curre].append(volu)

                elif czy2 == 's':
                    curre, asks, volu = user_info()

                    available_volume = 0
                    for voulm in buy_volume[curre]:
                        available_volume += voulm

                    if volu > available_volume:
                        print('Nie masz wystarczająco dużo waluty!')

                    else:

                        balance = 0
                        temp_volume = volu
                        while temp_volume > 0:

                            if buy_volume[curre][0] < temp_volume:
                                temp_volume -= buy_volume[curre][0]

                                balance += buy_volume[curre][0] * buy_rate[curre][0]

                                del buy_volume[curre][0]
                                del buy_rate[curre][0]

                            else:
                                buy_volume[curre][0] -= temp_volume

                                balance += temp_volume * buy_rate[curre][0]

                                if buy_volume[curre][0] == 0:
                                    del buy_volume[curre][0]
                                    del buy_rate[curre][0]

                                sell_rate[curre].append(asks)
                                sell_volume[curre].append(volu)
                                break

                        final_balance = sell_rate[curre][-1] * sell_volume[curre][-1] - balance
