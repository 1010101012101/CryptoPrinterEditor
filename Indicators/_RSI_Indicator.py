
name = 'RSI'
__values = {'multiplier': 1, 'length': 14, }

def set_values(**kwargs):
    for key in kwargs:
        for key2 in __values:
            if key is key2:
                __values[key] = kwargs[key]

def get_points(candles):
    length = __values['length']
    averages = __get_averages(candles[:length])
    for i in range(1,length):
        newaverages = __get_averages(candles[i:length+i])
        averages['gain'] = (averages['gain'] * (length-1) + newaverages['gain']) / length
        averages['loss'] = (averages['loss'] * (length-1) + newaverages['loss']) / length
    RS = averages['gain'] / averages['loss']
    RSI = 100 - (100/(1+RS))
    return RSI * __values['multiplier']
      
def __get_averages(candles):
    gain = 0
    loss = 0
    for candle in candles:
        dif = candle.close - candle.open
        if dif >= 0:
            gain += dif
        else:
            loss -= dif
    return {'gain': gain, 'loss': loss}