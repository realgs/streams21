import json

while True:

    while True:
        print("Czy chcesz załadować dane kupna, używając danych z wybranego pliku? 0: Tak, 1: Nie")
        decide = int(input())
        if decide == 0 or decide == 1:
            break
        else:
            print("wartość z poza zakresu")

    while True:
        print("Którą walutę chcesz załadowac danymi? 0: BTC, 1: ETH, 2: LSK")
        currency = int(input())
        if currency == 0 or currency == 1 or currency == 2:
            break
        else:
            print("wartość z poza zakresu")

    if decide == 0:
        print("Podaj nazwę pliku wraz z rozszerzeniem")
        path = str(input())

        if currency == 0:
            source = open(path)
            dataSource = json.load(source)

            f = open('Buys/buysBTC.json')
            data = json.load(f)

            for line in range(len(dataSource["data"])):
                data["data"].append(dataSource["data"][line])

            with open('Buys/buysBTC.json', 'w') as f:
                json.dump(data, f)

        elif currency == 1:
            source = open(path)
            dataSource = json.load(source)

            f = open('Buys/buysETH.json')
            data = json.load(f)

            for line in range(len(dataSource["data"])):
                data["data"].append(dataSource["data"][line])

            with open('Buys/buysETH.json', 'w') as f:
                json.dump(data, f)

        else:
            source = open(path)
            dataSource = json.load(source)

            f = open('Buys/buysLSK.json')
            data = json.load(f)

            for line in range(len(dataSource["data"])):
                data["data"].append(dataSource["data"][line])

            with open('Buys/buysLSK.json', 'w') as f:
                json.dump(data, f)
        print("DATA LOADED!")
        