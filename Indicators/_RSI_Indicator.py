from _Basic_Indicator import BasicIndicator

class RSI(BasicIndicator):

    name = 'RSI'
    defaultlength = 14

    def __init__(self, multiplier, lenght=defaultlength):
        super().__init__(multiplier)
        self.length = lenght

    def get_points(self, candles):
        averages = self.__get_averages(candles[:self.length])
        for i in range(1,self.length):
            newaverages = self.__get_averages(candles[i:self.length+i])
            averages['gain'] = (averages['gain'] * (self.length-1) + newaverages['gain']) / self.length
            averages['loss'] = (averages['loss'] * (self.length-1) + newaverages['loss']) / self.length
        RS = averages['gain'] / averages['loss']
        RSI = 100 - (100/(1+RS))
        return RSI * self.multiplier
      
    def __get_averages(self, candles):
        gain = 0
        loss = 0
        for candle in candles:
            dif = candle.close - candle.open
            if dif >= 0:
                gain += dif
            else:
                loss -= dif
        return {'gain': gain, 'loss': loss}