import json

while True:

    with open("data.json", 'r') as fp:
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

        if value == 0:
            valueSell = valueSellBTC
            currency = "BTC"

            with open('buysBTC.txt', 'a') as outfile:
                outfile.write(f'{str(valueSell)} \n')
                outfile.close()

        elif value == 1:
            valueSell = valueSellETH
            currency = "ETH"

            with open('buysETH.txt', 'a') as outfile:
                outfile.write(f'{str(valueSell)} \n')
                outfile.close()

        else:
            valueSell = valueSellLSK
            currency = "LSK"

            with open('buysLSK.txt', 'a') as outfile:
                outfile.write(f'{str(valueSell)} \n')
                outfile.close()

        print("Ile jednostek tej krypto? \n")
        quant = int(input())
        output = round(valueSell*quant, 3)

        print(f"Kupiłeś - {output} \n")

    else:
        None