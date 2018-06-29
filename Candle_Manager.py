import APIs._Binance_API
from classes import Candle

__currentCandles = []

def load_candles(symbol):
    candles = APIs._Binance_API.getKlines('BTCUSDT',limit=500,interval='1m')
    __currentCandles.clear()
    for candle in candles:
        __currentCandles.append(Candle(candle[0],candle[1],candle[2],candle[3],candle[4],candle[5],candle[6],candle[8]))

def print_candles():
    for candle in __currentCandles:
        candle.printCandle()

def get_candles(length=len(__currentCandles)):
    return __currentCandles[:length]