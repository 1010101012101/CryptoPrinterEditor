import Value_Smoother
import talib
import numpy as np
import pandas as pd

name = 'RSI'
__values = {'multiplier': 1, 'length': 10}

def set_values(key, value):
    __values[key] = float(value)

def get_values():
    return __values

def get_points(candles):
    length = int(__values['length'])
    RSIvalue = talib.RSI(candles['close'][:length+1], timeperiod=length)
    RSIvalue = (RSIvalue[10] - 50) * 2
    return RSIvalue * __values['multiplier']
    
def __get_averages(candles, length):
    gain = 0
    loss = 0
    for i in range(length):
        ccandle = candles[i]
        lcandle = candles[i+1]
        dif = ccandle.close - lcandle.close
        if dif >= 0:
            gain += dif
        else:
            loss -= dif
    return {'gain': gain, 'loss': loss}