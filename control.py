from trends_analysis import Cryptos
import json


Answer = input("Use archival data? (y/n) : ")
assert Answer == 'y' or Answer == 'n'

if Answer == 'y':
    name = input("Name of archival file: ")

else:
    name = 'database.json'
    data = {'Rec': {}, 'Avr': {}, 'Bil': {}}
    for c in Cryptos:
        data['Rec'][c] = []
        data['Avr'][c] = None
        data['Bil'][c] = None
    with open(name, 'w') as f:
        json.dump(data, f, indent = 2)

while True:
    with open(name) as f:
        data = json.load(f)
    New_record = []
    stopper = input("Shut down program? (y/n) ")
    if stopper == 'y':
        break
    print()
    print("Insert new data")
    New_record.append(input('Crypto: '))
    New_record.append(input('Buy/sell (b/s): '))
    New_record.append(int(input('Quantity: ')))
    New_record.append(int(input('Value: ')))
    assert New_record[1] == 'b' or New_record[1] == 's'
    assert New_record[0] in Cryptos

    if New_record[1] == 'b':
        r = 'Bought'
        sv = New_record[3] / New_record[2]
        for x in range(New_record[2]):
            data['Rec'][New_record[0]].append(sv)
    else:
        r = 'Sold'
        assert New_record[2] <= len(data['Rec'][New_record[0]])
        bill = 0
        for x in range(New_record[2]):
            bill += data['Rec'][New_record[0]].pop(0)
        bill = New_record[3] - bill
        if data['Bil'][New_record[0]] == None:
            data['Bil'][New_record[0]] = 0
        data['Bil'][New_record[0]] += round(bill, 2)

    if len(data['Rec'][New_record[0]]) > 0:
        am = len(data['Rec'][New_record[0]])
    else:
        am = 1
    data['Avr'][New_record[0]] = round(sum(data['Rec'][New_record[0]]) / am, 2)
    if data['Avr'][New_record[0]] == 0:
        data['Avr'][New_record[0]] = None

    print(r, New_record[0], 'in amount', New_record[2], 'for', New_record[3], "zlotys.")
    print('New average for', New_record[0], 'is', data['Avr'][New_record[0]], "zlotys.")
    if New_record[1] == 's':
        print('Change in balance of', New_record[0], 'to', data['Bil'][New_record[0]], "zlotys.")

    with open(name, 'w') as f:
        json.dump(data, f, indent = 2)
