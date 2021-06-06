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

    else:

        print("Jaką kryptowalutę życzysz sobie zakupić? : 0 - BTC ; 1 - ETH ; 2 - XLM \n")
        value = int(input())
        currency = ""

        print("Ile jednostek tej krypto? \n")
        quant = int(input())
        output = round(valueSell * quant, 3)

        if value == 0:
            valueSell = valueSellBTC
            currency = "BTC"

            y = {"currency": currency,
                 "count": quant,
                 "value": output
                 }

            f = open('Sells/sellsBTC.json')

            data = json.load(f)
            data["data"].append(y)

            with open('Sells/sellsBTC.json', 'w') as f:
                json.dump(data, f)

        elif value == 1:
            valueSell = valueSellETH
            currency = "ETH"

            y = {"currency": currency,
                 "count": quant,
                 "value": output
                 }

            f = open('Sells/sellsETH.json')

            data = json.load(f)
            data["data"].append(y)

            with open('Sells/sellsETH.json', 'w') as f:
                json.dump(data, f)

        else:
            valueSell = valueSellLSK
            currency = "LSK"

            y = {"currency": currency,
                 "count": quant,
                 "value": output
                 }

            f = open('Sells/sellsLSK.json')

            data = json.load(f)
            data["data"].append(y)

            with open('Sells/sellsLSK.json', 'w') as f:
                json.dump(data, f)

        print(f"Kupiłeś - {output} \n")