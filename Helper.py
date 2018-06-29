def get_extremes(candles):
    minlist = []
    maxlist = []
    for c in candles:
        minlist.append(c.low)
        maxlist.append(c.high)
    output = {'min': min(minlist), 'max': max(maxlist)}
    return output