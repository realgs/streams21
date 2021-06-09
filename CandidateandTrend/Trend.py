def checkWhatTrend(RSIArray):

    downHillsPoints = []
    upHillsPoints = []

    for items in range(1, len(RSIArray) - 1):
        if (RSIArray[items - 1] > RSIArray[items]) and (RSIArray[items] < RSIArray[items + 1]):  # sprawdzam czy to dołek
            downHillsPoints.append(items)
        else:
            downHillsPoints.append(0)  # wyrównuję indeksy

        if (RSIArray[items - 1] < RSIArray[items]) and (RSIArray[items] > RSIArray[items + 1]):  # sprawdzam czy to wierzchołek
            upHillsPoints.append(items)
        else:
            upHillsPoints.append(0) # wyrównuję indeksy

    # Sprawdzam czy nastapił spadek
    if (downHillsPoints[len(downHillsPoints) - 1] < downHillsPoints[len(downHillsPoints) - 2]) and \
            (downHillsPoints[len(downHillsPoints) - 1] != 0 and downHillsPoints[len(downHillsPoints) - 2] != 0):
        print("down")
        return "Downward trend"
    # Sprawdzam czy nastapił wzrost
    elif (upHillsPoints[len(upHillsPoints) - 1] > upHillsPoints[len(upHillsPoints) - 2]) and \
            (upHillsPoints[len(upHillsPoints) - 1] != 0 and upHillsPoints[len(upHillsPoints) - 2] != 0):
        print("up")
        return "Rising trend"
    # Sprawdzam czy osięgnęliśmy trend boczny
    elif ((upHillsPoints[len(upHillsPoints) - 1] == upHillsPoints[len(upHillsPoints) - 2]) or (downHillsPoints[len(downHillsPoints) - 1] == downHillsPoints[len(downHillsPoints) - 2])) \
            and (upHillsPoints[len(upHillsPoints) - 1] != 0 and upHillsPoints[len(upHillsPoints) - 2] != 0) \
            and (downHillsPoints[len(downHillsPoints) - 1] != 0 and downHillsPoints[len(downHillsPoints) - 2] != 0):
        print("side")
        return "Sideways trend"
    else:
        print("Small amount of data")
        return "Small amount of data"