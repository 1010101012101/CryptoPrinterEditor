import requests
import json

__baseURL = "https://api.whaleclub.co/v1/"
__endpoints = {'ping': '/api/v1/ping',
            'servertime': '/api/v1/time',
            'klines': '/api/v1/klines'}

def __request_data(endpoint, *args, printResult=False):
    response = requests.get(__baseURL + __endpoints[endpoint],*args)
    if response.ok is True:
        jData = json.loads(response.content)
        if type(response.content) is type(dict()):               
            if printResult is True:
                for key in jData:
                    print("{} is {}".format(key,jData[key]))
            else:
                return jData
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

def getKlines(symbol,interval='1m',limit=100):
    return(__request_data('klines',{'symbol': symbol,
                            'interval': interval,
                            'limit': limit}))


    

