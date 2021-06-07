import json

while True:

    with open("CurrentBuySellData/dataBuy.json", 'r') as fp:
        data = json.load(fp)
        valueBuyBTC = data['BTC']
        valueBuyETH = data['ETH']
        valueBuyLSK = data['LSK']

    valueBuy = 0

    with open("CurrentBuySellData/dataSell.json", 'r') as fp:
        data = json.load(fp)
        valueSellBTC = data['BTC']
        valueSellETH = data['ETH']
        valueSellLSK = data['LSK']

    valueSell = 0

    print("Witaj, życzysz sobie kupić czy sprzedać? (Kolejno 0 lub 1)")
    sellbuy = int(input())

    if sellbuy == 0:

        print("Jaką kryptowalutę życzysz sobie zakupić? : 0 - BTC ; 1 - ETH ; 2 - XLM \n")
        value = int(input())
        currency = ""

        print("Ile jednostek tej krypto? \n")
        quant = int(input())

        if value == 0:
            valueBuy = valueBuyBTC
            currency = "BTC"

            output = round(valueBuy * quant, 3)

            y = {"currency": currency,
                 "count": quant,
                 "value": output
                 }

            f = open('Buys/buysBTC.json')

            data = json.load(f)
            data["data"].append(y)

            with open('Buys/buysBTC.json', 'w') as f:
                json.dump(data, f)

        elif value == 1:
            valueBuy = valueBuyETH
            currency = "ETH"

            output = round(valueBuy * quant, 3)

            y = {"currency": currency,
                 "count": quant,
                 "value": output
                 }

            f = open('Buys/buysETH.json')

            data = json.load(f)
            data["data"].append(y)

            with open('Buys/buysETH.json', 'w') as f:
                json.dump(data, f)

        else:
            valueBuy = valueBuyLSK
            currency = "LSK"

            output = round(valueBuy * quant, 3)

            y = {"currency": currency,
                 "count": quant,
                 "value": output
                 }

            f = open('Buys/buysLSK.json')

            data = json.load(f)
            data["data"].append(y)

            with open('Buys/buysLSK.json', 'w') as f:
                json.dump(data, f)

        print(f"Kupiłeś - {output} \n")

    else:   # SELL

        print("Jaką kryptowalutę życzysz sobie sprzedać? : 0 - BTC ; 1 - ETH ; 2 - XLM \n")
        value = int(input())
        currency = ""

        print("Ile jednostek tej krypto? \n")
        quant = int(input())

        if value == 0:
            valueSell = valueSellBTC
            currency = "BTC"

            f = open('Buys/buysBTC.json')
            data = json.load(f)

            count = 0
            number = 0
            toIndex = 0

            if len(data['data']) > 0:
                for line in range(len(data["data"])):
                    number += 1
                    count += data['data'][line]['count']
                    if count >= quant:
                        output = round(valueSell * quant, 3)
                        toIndex = number
                        break
                if toIndex == 0:
                    print("Ilość kupionych kryptowalut jest niższa od ilości którą chcesz sprzedać")
                else:
                    if toIndex == 1 and count == quant:
                        # usuwam
                        money = output - data['data'][toIndex-1]['value']
                        del data['data'][toIndex - 1]
                    elif toIndex == 1 and count > quant:
                        w = ((data['data'][toIndex-1]['value']/data['data'][toIndex-1]['count']) * quant)
                        money = output - w
                        data['data'][toIndex - 1]['count'] -= quant
                    else:
                        soldTotal = 0
                        buyedSold = quant
                        for items in range(toIndex):
                            if buyedSold - data['data'][items]['count'] >= 0:
                                # usuwam
                                buyedSold -= data['data'][items]['count']
                                soldTotal += data['data'][items]['value']
                                del data['data'][items]
                            else:
                                cur = (quant-buyedSold)
                                buyedSold -= (quant-buyedSold)
                                soldTotal += (data['data'][items]['value']/data['data'][items]['count']) * (cur)
                                data['data'][items]['count'] -= cur  # odejmuje
                        money = output - soldTotal
            else:
                print("Brak wartości zakupionych danej kryptowaluty")
