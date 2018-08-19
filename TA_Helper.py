def get_sma(candles, length):
    sma = 0
    for i in range(length):
        sma += candles[i].close
    sma /= length
    return sma

def get_ema(candles, length, lastema):
    weigth = 2 / (length + 1)
    ema = candles[0].close * weigth + lastema * (1-weigth)
    return ema