import requests
import json
import websocket
import time
import Candle_Manager

__baseURL = "https://api.binance.com"
__endpoints = {'ping': '/api/v1/ping',
            'servertime': '/api/v1/time',
            'klines': '/api/v1/klines'}

__websocket = None

def __request_data(endpoint, printResult=False, params=None):
    response = requests.get(__baseURL + __endpoints[endpoint],params=params)
    if response.ok is True:
        jData = json.loads(response.content)
        if printResult is True:
            if type(response.content) is type(dict()):               
                if printResult is True:
                    for key in jData:
                        print("{} is {}".format(key,jData[key]))
            else:           
                if printResult is True:
                    print(jData)
        else:
            return jData
    else:
        print("Error while requesting: " + endpoint)
        #print("Errormessage: " + response.raise_for_status())

def printPing():
    __request_data('servertime',printResult=True)

def getKlines(symbol,interval='1m',limit=1000):
    params = {'symbol': symbol,'interval': interval,'limit': limit}
    return(__request_data('klines',params=params))

def __on_message(ws, message):
    jData = json.loads(message)
    Candle_Manager.pricesteam_message(jData)

def __on_error(ws, error):
    print(error)

def __on_close(ws):
    print("### closed ###")

def open_klinesstream(symbol, interval='1m'):
    websocket.enableTrace(True)
    url = "wss://stream.binance.com:9443/ws/" + symbol + "@kline_" + interval
    global __websocket
    __websocket = websocket.WebSocketApp(url,
                              on_message = __on_message,
                              on_error = __on_error,
                              on_close = __on_close)
    __websocket.run_forever()

def close_klinestream():
    global __websocket
    if __websocket is not None:
        __websocket.close()


    

