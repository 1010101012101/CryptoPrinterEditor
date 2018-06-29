from PyQt5 import QtCore, QtGui, QtWidgets
from HelperClasses import Translator
import Helper

class ChartPlotter(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(QtWidgets.QGraphicsView,self).__init__(*args,**kwargs)

    def plot_chart(self, candles):
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        extremes = Helper.get_extremes(candles)
        candleswidth = self.width()/len(candles)
        y_trans = Translator(extremes['min'],
                            extremes['max'],
                            0, self.height())
        x_trans = Translator(0, len(candles),
                            self.width(),0 )
        for i in range(len(candles)-1):
            candle = candles[i]
            dif = candle.close - candle.open 
            if dif >= 0:
                pen = QtGui.QPen(QtCore.Qt.green)
                brush = QtGui.QBrush(QtCore.Qt.green)
            else:
                pen = QtGui.QPen(QtCore.Qt.red)
                brush = QtGui.QBrush(QtCore.Qt.red)

            self.scene.addRect(int(x_trans.t(i)-candleswidth),
                                int(y_trans.t(candle.open)),
                                int(candleswidth),
                                int(y_trans.t(candle.close) - 
                                y_trans.t(candle.open)),pen, brush)
            x = int(x_trans.t(i)-(candleswidth/2))
            self.scene.addLine(x, int(y_trans.t(candle.high)),
                                x, int(y_trans.t(candle.low)),pen)
            
class IndicatorPlotter(QtWidgets.QGraphicsView):

    def plot_indicator(self, indicatordata):
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        y_trans = Translator(0, 100, 0, self.height())
        x_trans = Translator(0, len(indicatordata), 
                                self.width(),0 )
        for i in range(len(indicatordata)-1):
            self.scene.addLine(x_trans.t(i),y_trans.t(indicatordata[i]),
                                x_trans.t(i-1),y_trans.t(indicatordata[i-1]))
        
