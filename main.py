import os
import sys
import Candle_Manager
import Indicator_Manager
import File_Loader

from PyQt5 import QtCore,QtWidgets,QtGui
from Ui_mainUI import Ui_MainWindow

class MainWindow(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.setupUi(self)
        self.load_button.pressed.connect(self.plot_chart)
        self.show()

    def plot_chart(self):
        Candle_Manager.load_candles(self.symbol_input.text)
        candles = Candle_Manager.get_candles(length=200)
        self.chart_plotter.plot_chart(candles)
        indicatordata = Indicator_Manager.get_indicatordata('RSI',200)
        self.indicator_plotter.plot_indicator(indicatordata)
    

if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("CryptoPrinter")
    Indicator_Manager.load_indicators()
    window = MainWindow()
    app.exec_()
    