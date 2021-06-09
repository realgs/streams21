def defineAsVolatile(samplesArray, Y, X):
    if len(samplesArray) > Y:
        Ysample = samplesArray[Y]
    else:
        Ysample = samplesArray[len(samplesArray) - 1]

    currentSample = samplesArray[0]

    if Ysample > currentSample:
        max = Ysample
        min = currentSample
    else:
        max = currentSample
        min = Ysample

    out = min * 100/max
    percent = 100 - out

    if percent > X:
        return True
    else:
        return False