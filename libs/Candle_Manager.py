import _thread as thread
import queue
import numpy as np

from libs.classes import Candle
#import libs.Candle_Manager as Candle_Manager
import libs.InstanceHolder as InstanceHolder
import libs.API_Manager as API_Manager

__currentCandles = []
__currentOHLCV = {}

def load_candles(symbol, interval='1m'):
    global __currentCandles
    candles = API_Manager.get_Klines(symbol,interval)
    if(candles != None):
        __currentCandles.clear() 
        for candle in reversed(candles):
            __currentCandles.append(Candle(candle[0],candle[1],candle[2],candle[3],candle[4],candle[5]))
        print('Loaded {} candles'.format(len(candles)))
    else:
        print('Symbol was not found')
    _translate_OHLCV()

def print_candles():
    for candle in __currentCandles:
        candle.printCandle()

def get_candles(length=len(__currentCandles)):
    return __currentCandles[:length]

def get_OHLCVs():
    return __currentOHLCV

def on_newcandle(candle):
    global __currentCandles
    newcandle = Candle(candle[0],candle[1],candle[2],candle[3],candle[4],candle[5])
    mainWindow = InstanceHolder.get_instance('MainWindow')
    __currentCandles.insert(0,newcandle)  
    if len(__currentCandles) > 1000:
        del __currentCandles[-1]
    mainWindow.add_queueitem('new_candle')

def _translate_OHLCV():
    global __currentOHLCV
    candles = {
        'open': [],
        'high': [],
        'low': [],
        'close': [],
        'volume': []
    }
    for c in __currentCandles:
        candles['open'].append(c.open)
        candles['high'].append(c.high)
        candles['low'].append(c.low)
        candles['close'].append(c.close)
        candles['volume'].append(c.volume)
    __currentOHLCV['open'] = np.array(candles['open'])
    __currentOHLCV['high'] = np.array(candles['high'])
    __currentOHLCV['low'] = np.array(candles['low'])
    __currentOHLCV['close'] = np.array(candles['close'])
    __currentOHLCV['volume'] = np.array(candles['volume'])

