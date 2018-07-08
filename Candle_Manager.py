import APIs._Binance_API
from classes import Candle
import _thread as thread
import Candle_Manager
import InstanceHolder
import queue

__currentCandles = []
__mainWindow = None

def setup(main):
    Candle_Manager.__mainWindow = main

def load_candles(symbol, interval='1m'):
    candles = APIs._Binance_API.getKlines(symbol,limit=1000,interval=interval)
    if(candles != None):
        __currentCandles.clear()
        for candle in reversed(candles):
            __currentCandles.append(Candle(candle[0],candle[1],candle[2],candle[3],candle[4],candle[5],candle[6],candle[8]))
    else:
        print('Symbol was not found')

def print_candles():
    for candle in __currentCandles:
        candle.printCandle()

def get_candles(length=len(__currentCandles)):
    return __currentCandles[:length]

def initiate_pricestream(symbol, interval='1m'):
    thread.start_new_thread(APIs._Binance_API.open_klinesstream, (symbol.lower(), interval))

def close_pricestream():
    APIs._Binance_API.close_klinestream()

def pricesteam_message(data):
    cd = data['k']
    newcandle = Candle(cd['t'], cd['o'],cd['h'],cd['l'],cd['c'],cd['v'],cd['T'],1)
    __currentCandles[0] = newcandle
    mainWindow = InstanceHolder.get_instance('MainWindow')
    if cd['x'] is True:
        __currentCandles.insert(0,Candle(newcandle.closetime,newcandle.close,newcandle.close,newcandle.close,newcandle.close,0,0,0))  
        if len(__currentCandles) > 1000:
            del __currentCandles[-1]
        mainWindow.add_queueitem('plot_chart')
    else:
        mainWindow.add_queueitem('plot_currentCandle')
