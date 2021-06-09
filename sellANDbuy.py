import json

while True:

    valueBuy = 0
    valueSell = 0

    while True:
        print("Witaj, życzysz sobie kupić czy sprzedać? (Kolejno: 0 lub 1)")
        sellbuy = int(input())
        if sellbuy == 0 or sellbuy == 1:
            break
        else:
            print("wartość z poza zakresu")

    if sellbuy == 0:

        while True:
            print("Jaką kryptowalutę życzysz sobie zakupić? : 0 - BTC ; 1 - ETH ; 2 - LSK \n")
            value = int(input())
            if value == 0 or value == 1 or value == 2:
                break
            else:
                print("wartość z poza zakresu")

        currency = ""

        while True:
            print("Ile jednostek tej krypto? \n")
            quant = int(input())
            print("W jakiej cenie ta jednostka krypto? \n")
            price = int(input())
            if quant > 0 and price > 0:
                break
            else:
                print("wartość z poza zakresu")


        if value == 0:
            valueBuy = price

            with open("CurrentBuySellData/dataBuy.json", 'r') as fp:
                data = json.load(fp)
                fp.close()

            data["BTC"] = price

            file = open("CurrentBuySellData/dataBuy.json", "w")
            json.dump(data, file)
            file.close()

            currency = "BTC"

            output = round(valueBuy * quant, 3)

            y = {"currency": currency,
                 "count": quant,
                 "value": output,
                 "single": valueBuy
                 }

            f = open('Buys/buysBTC.json')

            data = json.load(f)
            data["data"].append(y)

            with open('Buys/buysBTC.json', 'w') as f:
                json.dump(data, f)

        elif value == 1:
            valueBuy = price

            with open("CurrentBuySellData/dataBuy.json", 'r') as fp:
                data = json.load(fp)
                fp.close()

            data["ETH"] = price

            file = open("CurrentBuySellData/dataBuy.json", "w")
            json.dump(data, file)
            file.close()

            currency = "ETH"

            output = round(valueBuy * quant, 3)

            y = {"currency": currency,
                 "count": quant,
                 "value": output,
                 "single": valueBuy
                 }

            f = open('Buys/buysETH.json')

            data = json.load(f)
            data["data"].append(y)

            with open('Buys/buysETH.json', 'w') as f:
                json.dump(data, f)

        else:
            valueBuy = price

            with open("CurrentBuySellData/dataBuy.json", 'r') as fp:
                data = json.load(fp)
                fp.close()

            data["LSK"] = price

            file = open("CurrentBuySellData/dataBuy.json", "w")
            json.dump(data, file)
            file.close()

            currency = "LSK"

            output = round(valueBuy * quant, 3)

            y = {"currency": currency,
                 "count": quant,
                 "value": output,
                 "single": valueBuy
                 }

            f = open('Buys/buysLSK.json')

            data = json.load(f)
            data["data"].append(y)

            with open('Buys/buysLSK.json', 'w') as f:
                json.dump(data, f)

        print(f"Kupiłeś - {quant} {currency} (za jednostkę: {price}), suma: {output} \n")

    else:   # SELL

        while True:
            print("Jaką kryptowalutę życzysz sobie zakupić? : 0 - BTC ; 1 - ETH ; 2 - LSK \n")
            value = int(input())
            if value == 0 or value == 1 or value == 2:
                break
            else:
                print("wartość z poza zakresu")
        currency = ""

        while True:
            print("Ile jednostek tej krypto? \n")
            quant = int(input())
            print("W jakiej cenie ta jednostka krypto? \n")
            price = int(input())
            if quant > 0 and price > 0:
                break
            else:
                print("wartość z poza zakresu")

        if value == 0:
            valueSell = price

            with open("CurrentBuySellData/dataSell.json", 'r') as fp:
                data = json.load(fp)
                fp.close()

            data["BTC"] = price

            file = open("CurrentBuySellData/dataSell.json", "w")
            json.dump(data, file)
            file.close()

            currency = "BTC"
            f = open('Buys/buysBTC.json')
        elif value == 1:
            valueSell = price

            with open("CurrentBuySellData/dataSell.json", 'r') as fp:
                data = json.load(fp)
                fp.close()

            data["ETH"] = price

            file = open("CurrentBuySellData/dataSell.json", "w")
            json.dump(data, file)
            file.close()

            currency = "ETH"
            f = open('Buys/buysETH.json')
        elif value == 2:
            valueSell = price

            with open("CurrentBuySellData/dataSell.json", 'r') as fp:
                data = json.load(fp)
                fp.close()

            data["LSK"] = price

            file = open("CurrentBuySellData/dataSell.json", "w")
            json.dump(data, file)
            file.close()

            currency = "LSK"
            f = open('Buys/buysLSK.json')

        data = json.load(f)

        count = 0
        number = 0
        toIndex = 0
        money = 0

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
                    money += output - data['data'][toIndex-1]['value']
                    del data['data'][toIndex - 1]
                elif toIndex == 1 and count > quant:
                    w = ((data['data'][toIndex-1]['value']/data['data'][toIndex-1]['count']) * quant)
                    money += output - w
                    data['data'][toIndex - 1]['count'] -= quant
                else:
                    soldTotal = 0
                    boughtSold = quant
                    items = 0
                    while boughtSold != 0:
                        if boughtSold - data['data'][items]['count'] >= 0:
                            # usuwam
                            boughtSold -= data['data'][items]['count']
                            soldTotal += data['data'][items]['value']
                            del data['data'][items]
                            toIndex -= 1
                        else:
                            cur = float(quant - boughtSold)
                            boughtSold -= (quant - boughtSold)
                            soldTotal += (data['data'][items]['value']/data['data'][items]['count']) * (cur)
                            data['data'][items]['count'] -= cur  # odejmuje
                    money += quant - soldTotal

            print(f"Sprzedałeś - {money} {currency} (za jednostkę: {price}), suma: {quant} \n")
            if value == 0:
                with open('Buys/buysBTC.json', 'w') as f:
                    json.dump(data, f)

                f = open('Sells/sellsBTC.json')
                data = json.load(f)
                y = {"currency": currency,
                     "count": quant,
                     "value": output,
                     "single": price
                     }
                data['data'].append(y)
                with open('Sells/sellsBTC.json', 'w') as f:
                    json.dump(data, f)

                # adding to total revenue
                f = open('Revenue/revenueBTC.json')
                data = json.load(f)
                data["data"][0]['revenue'] += money
                with open('Revenue/revenueBTC.json', 'w') as f:
                    json.dump(data, f)

            elif value == 1:
                with open('Buys/buysETH.json', 'w') as f:
                    json.dump(data, f)

                    f = open('Sells/sellsETH.json')
                    data = json.load(f)
                    y = {"currency": currency,
                         "count": quant,
                         "value": output,
                         "single": price
                         }
                    data['data'].append(y)
                    with open('Sells/sellsETH.json', 'w') as f:
                        json.dump(data, f)

                    # adding to total revenue
                    f = open('Revenue/revenueETH.json')
                    data = json.load(f)
                    data["data"][0]['revenue'] += money
                    with open('Revenue/revenueETH.json', 'w') as f:
                        json.dump(data, f)

            elif value == 2:
                with open('Buys/buysLSK.json', 'w') as f:
                    json.dump(data, f)

                    f = open('Sells/sellsLSK.json')
                    data = json.load(f)
                    y = {"currency": currency,
                         "count": quant,
                         "value": output,
                         "single": price
                         }
                    data['data'].append(y)
                    with open('Sells/sellsLSK.json', 'w') as f:
                        json.dump(data, f)

                    # adding to total revenue
                    f = open('Revenue/revenueLSK.json')
                    data = json.load(f)
                    data["data"][0]['revenue'] += money
                    with open('Revenue/revenueLSK.json', 'w') as f:
                        json.dump(data, f)

        else:
            print("Brak wartości zakupionych danej kryptowaluty")
