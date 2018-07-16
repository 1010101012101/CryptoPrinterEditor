
name = 'RSI'
__values = {'multiplier': 1, 'length': 10}

def set_values(key, value):
    __values[key] = float(value)

def get_values():
    return __values

def get_points(candles):
    length = int(__values['length'])
    averages = __get_averages(candles[:length+1],length)
    try:
        RS = averages['gain'] / averages['loss']
        RSI = 100 - (100/(1+RS))
        RSI = (RSI - 50) * 2
        return RSI * __values['multiplier']
    except:
        return None
    
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