import ccxt
from threading import Thread, Event

__exchange = None
__thread = None

def set_newexchange(name, APIkey, secret):
    global __exchange
    exchange_class = getattr(ccxt, name)
    __exchange = exchange_class({
        'apiKey': APIkey,
        'secret': secret,
        'timeout': 30000,
        'enableRateLimit': True,
    })

def get_Klines(symbol,timeframe = '1m', since = None, limit=750):
    if since is None:
        since = __exchange.milliseconds() - parseInterval(interval=timeframe) * 60 * 1000 * limit
    candles = __exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    return candles

def open_klinesstream(symbol, interval='1m'):
    global __thread
    __thread = PriceStreamThread(Event(), 2, __exchange, symbol, interval)
    __thread.start()

def close_klinestream():
    global __thread
    if __thread != None:
        __thread.stopThread()

def create_order(side):
    __exchange.create_order("BTCUSD", "Market", side, 0.0001)  

def parseInterval(interval = '1m'):
    sInterval = str(interval)
    time = sInterval[len(sInterval)-1:]
    amount = int(sInterval[:len(sInterval)-1])
    multiplier = 0
    if time == 'm':
        multiplier = amount 
    if time == 'h':
        multiplier = amount * 60
    if time == 'd':
        multiplier = amount * 60 * 24
    if time == 'w':
        multiplier = amount  * 60 * 24 * 7
    if time == 'M':
        multiplier = amount * 60 * 24 * 7 * 31
    return multiplier

class PriceStreamThread(Thread):
    def __init__(self, event, time, exchange, symbol, interval):
        Thread.__init__(self)
        self.stopped = event
        self.exchange = exchange
        self.time = time
        self.symbol = symbol
        self.interval = interval
        self.multiplier = parseInterval(interval=interval)
        print('Started new pricestream thread for {}'.format(symbol))

    def run(self):
        while not self.stopped.wait(self.time):
            since = self.exchange.milliseconds() - self.multiplier * 60 * 1000
            try:
                candles = self.exchange.fetch_ohlcv(self.symbol, self.interval, since, 3)
                time = candles[0][0]
                if hasattr(self, 'lasttime'):
                    if self.lasttime != time:
                        print("New Candle", candles)
                        import libs.Candle_Manager as Candle_Manager
                        Candle_Manager.on_newcandle(candles[0])
                self.lasttime = time
            except:
                pass

    def stopThread(self):
        self.stopped.set()

    
        



    

