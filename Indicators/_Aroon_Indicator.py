import Helper
import math
import Value_Smoother

name = 'Aroon'
__values = {'multiplier': 0.7, 'length': 20}

def set_values(key, value):
    __values[key] = float(value)

def get_values():
    return __values

def get_points(candles):
    length = int(__values['length'])
    diff = __get_aroon_value(candles,length)
    diff2 = Value_Smoother.linear_changer(diff)
    if diff2 > 100:
        diff2 = 100
    if diff < 0:
        diff2 *= -1
    return diff2 * __values['multiplier']

def __get_aroon_value(candles, length):
    extremes = Helper.get_extremes(candles[:length])
    highs = [x.high for x in candles[:length]]
    lows = [x.low for x in candles[:length]]
    sincehigh = highs.index(extremes['max'])
    sincelow = lows.index(extremes['min'])
    aroonup = 100 * (length - sincehigh) / length
    aroondown = 100 * (length - sincelow) / length
    return aroonup - aroondown


    