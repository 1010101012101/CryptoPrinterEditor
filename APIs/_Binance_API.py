import requests
import json

__baseURL = "https://api.binance.com"
__endpoints = {'ping': '/api/v1/ping',
            'servertime': '/api/v1/time',
            'klines': '/api/v1/klines'}

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


    

