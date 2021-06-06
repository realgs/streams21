def defineCandidate(BTCTrend, ETHTrend, LSKTrend, BTCVolume, ETHVolume, LSKVolume):
    BTC = False
    ETH = False
    LSK = False

    TFArray = [BTC, ETH, LSK]

    BTCLastVolume = float(BTCVolume[len(BTCVolume) - 1])
    ETHLastVolume = float(ETHVolume[len(BTCVolume) - 1])
    LSKLastVolume = float(LSKVolume[len(BTCVolume) - 1])

    LastVolumeArray = [BTCLastVolume, ETHLastVolume, LSKLastVolume]
    max = ""

    if BTCTrend[len(BTCTrend) - 1] != "Downward trend":
        BTC = True
    if ETHTrend[len(ETHTrend) - 1] != "Downward trend":
        ETH = True
    if LSKTrend[len(LSKTrend) - 1] != "Downward trend":
        LSK = True

    maxArray = []
    for items in range(len(TFArray)):
        if TFArray[items] == True:
            maxArray.append(LastVolumeArray[items])
        else:
            maxArray.append(0)
    out = maxArray.index(np.max(maxArray))

    if out == 0:
        max = "BTC"
    elif out == 1:
        max = "ETH"
    else:
        max = "LSK"
    return max
