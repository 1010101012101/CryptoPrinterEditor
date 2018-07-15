
name = 'RSI'
__values = {'multiplier': 1, 'length': 14, }

def set_values(key, value):
    __values[key] = int(value)

def get_values():
    return __values

def get_points(candles):
    length = __values['length']
    averages = __get_averages(candles[:length+1])
    try:
        RS = averages['gain'] / averages['loss']
        RSI = 100 - (100/(1+RS))
        RSI = (RSI - 50) * 2
        return RSI * __values['multiplier']
    except:
        return None
    
def __get_averages(candles):
    gain = 0
    loss = 0
    for i in range(__values['length']):
        ccandle = candles[i]
        lcandle = candles[i+1]
        dif = ccandle.close - lcandle.close
        if dif >= 0:
            gain += dif
        else:
            loss -= dif
    return {'gain': gain, 'loss': loss}