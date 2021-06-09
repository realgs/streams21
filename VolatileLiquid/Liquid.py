def defineAsLiquid(buy, sell, S):
    if buy > sell:
        max = buy
        min = sell
    else:
        max = sell
        min = sell

    out = min * 100/max
    percent = 100 - out

    if percent < S:
        return True
    else:
        return False
