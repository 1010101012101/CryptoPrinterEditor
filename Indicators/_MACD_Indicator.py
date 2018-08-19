import TA_Helper
name = 'MACD'
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
        #RSI = Value_Smoother.exponential_smoother(RSI)
        return RSI * __values['multiplier']
    except:
        return None
    
def __get_ema(candles, length):
    candles = candles.reverse()
    #for i in range(length):
    #    if i is 0:
    #        TA_Helper.get_sma(candles, length)
        
    #return {'gain': gain, 'loss': loss}