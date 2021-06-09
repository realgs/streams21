def calculateAverage(arraySell, arrayBuy, samplesNumber):
    valueBuy = 0
    valueSell = 0
    if len(arrayBuy) > samplesNumber:
        for items in range(samplesNumber):
            valueBuy += arrayBuy[len(arrayBuy)-items-1]
        valueBuy /= samplesNumber
    else:
        for items in range(len(arrayBuy)):
            valueBuy += arrayBuy[items]
        valueBuy /= samplesNumber

    if len(arraySell) > samplesNumber:
        for items in range(samplesNumber):
            valueSell += arraySell[len(arraySell)-items-1]
        valueSell /= samplesNumber
    else:
        for items in range(len(arraySell)):
            valueSell += arraySell[items]
        valueSell /= samplesNumber
    return valueSell, valueBuy