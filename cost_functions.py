import json
# from Okienko_2 import calculator


# # if u choose BTC
# to_do = 'buy'
# current = 'btc'
# ile_jednostek = 1
# za_ile = 3000

def showSettings():
    f = open("/repozytorium/database.txt", "r")
    data = json.load(f)
    return data

def user_average( to_do, current, ile_jednostek, za_ile ):
    f = open("/repozytorium/database.txt", "r")
    data = json.load(f)

    cost = za_ile / ile_jednostek

    if current == 'btc':
        transactions_BTC = data['list_BTC_json'] # w jsonie to jest tablica
        if to_do == 'buy':
            for i in range(ile_jednostek):
                transactions_BTC.append(cost)
            data['saldo_BTC_json'] += -za_ile
        if to_do == 'sell':
            del transactions_BTC[:ile_jednostek]
            data['saldo_BTC_json'] += za_ile
        try:
            average_btc = sum(transactions_BTC) / len(transactions_BTC)
            data['average_BTC_json'] = average_btc
        except ZeroDivisionError:
            average_btc = 0
            data['average_BTC_json'] = average_btc

    elif current == 'bat':
        transactions_BAT = data['list_BAT_json']
        if to_do == 'buy':
            for i in range(ile_jednostek):
                transactions_BAT.append(cost)
            data['saldo_BAT_json'] += -za_ile
        if to_do == 'sell':
            del transactions_BAT[:ile_jednostek]
            data['saldo_BAT_json'] += za_ile

        try:
            average_bat = sum(transactions_BAT) / len(transactions_BAT)
            data['average_BAT_json'] = average_bat
        except ZeroDivisionError:
            average_bat = 0
            data['average_BAT_json'] = average_bat

    elif current == 'zrx':
        transactions_ZRX = data['list_ZRX_json']
        if to_do == 'buy':
            for i in range(ile_jednostek):
                transactions_ZRX.append(cost)
            data['saldo_ZRX_json'] += -za_ile
        if to_do == 'sell':
            del transactions_ZRX[:ile_jednostek]
            data['saldo_ZRX_json'] += za_ile

        try:
            average_zrx = sum(transactions_ZRX) / len(transactions_ZRX)
            data['average_ZRX_json'] = average_zrx
        except ZeroDivisionError:
            average_zrx = 0
            data['average_ZRX_json'] = average_zrx

    f.close()
    g = open("/repozytorium/database.txt", "w")
    json.dump(data, g)
    g.close()

print(showSettings())



# coś = showSettings()['average_BTC_json'] # i to chcemy dawać na wykres
# coś2 = showSettings()['saldo_BTC_json']