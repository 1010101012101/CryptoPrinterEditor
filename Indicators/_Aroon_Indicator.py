import Helper

name = 'Aroon'
__values = {'multiplier': 1, 'length': 14, }

def set_values(key, value):
    __values[key] = float(value)

def get_values():
    return __values

def get_points(candles):
    length = __values['length']
    extremes = Helper.get_extremes(candles[:length])
    highs = [x.high for x in candles[:length]]
    lows = [x.low for x in candles[:length]]
    sincehigh = highs.index(extremes['max'])
    sincelow = lows.index(extremes['min'])
    aroonup = 100 * (length - sincehigh) / length
    aroondown = 100 * (length - sincelow) / length
    diff = aroonup - aroondown
    returnvalue = 0
    if diff is 0:
        returnvalue = 100
    return diff * __values['multiplier']

    