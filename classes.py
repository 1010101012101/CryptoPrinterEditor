class Candle:
    def __init__(self,opentime,open,high,low,close,volume,closetime,tradenumber):
        self.opentime = float(opentime)
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = float(volume)
        self.closetime = float(closetime)
        self.tradenumber = float(tradenumber)
    
    def printCandle(self):
        print("Opentime: {}, open: {}, close:{}, volume:{}".format(self.opentime,self.open,self.close,self.volume))