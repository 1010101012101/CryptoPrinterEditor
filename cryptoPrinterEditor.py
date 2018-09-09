import os
import sys
import queue
import talib

import libs.Candle_Manager as Candle_Manager
import libs.Indicator_Manager as Indicator_Manager
import libs.File_Loader as File_Loader
import libs.InstanceHolder as InstanceHolder
import libs.API_Manager as API_Manager
import libs.XML_Writer as XML_Writer
from libs.Ui_mainUI import Ui_MainWindow

from PyQt5 import QtCore,QtWidgets,QtGui

class MainWindow(Ui_MainWindow,QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.setupUi(self)
        Indicator_Manager.load_indicators()
        InstanceHolder.add_instance(self, 'MainWindow')
        self.queueTimer = QtCore.QTimer()
        self.queueTimer.timeout.connect(self.on_timertick)
        self.queueTimer.start(100)
        self.workqueue = queue.Queue()
        self.plot_button.pressed.connect(self.plot_chart)
        self.interval_comboBox.addItems(['1m','5m','1h','12h','1d','1w','1M'])
        self.indicatoroverview_view.add_items(Indicator_Manager.get_indicator_names())
        self.saveindicator_button.pressed.connect(self.on_save_indicator)
        self.save_button.pressed.connect(self.save_data)
        self.path_input.setText(os.path.dirname(os.path.realpath(__file__)) + "/IndicatorTemplates/")
        self.indicators_combobox.addItems(talib.get_functions())
        self.currentStream = ''
        self.lastindicator = "Overview"
        self.add_queueitem('init_plotter')
        self.add_queueitem('plot_chart')
        API_Manager.set_newexchange("binance","","")
        self.show()

    def on_timertick(self):
        if self.workqueue.empty() is not True:
            task = self.workqueue.get()
            if task == 'plot_chart':
                self.plot_chart()
            if task == 'plot_currentCandle':
                self.plot_currentCandle()
            if task == 'init_plotter':
                self.chart_plotter.init_plotter()
    
    def add_queueitem(self, task):
        self.workqueue.put(task)

    def save_data(self):
        path = self.path_input.text()
        if path.find('.xml') is -1:
            path += ".xml"
        symbol = self.symbol_input.text()
        timeframe = self.interval_comboBox.currentText()
        XML_Writer.save_data(path,symbol, timeframe)

    def plot_currentCandle(self):
        requestlength = self.length_slider.value()
        #Candle_Manager.load_candles(self.symbol_input.text(),self.interval_comboBox.currentText())
        candles = Candle_Manager.get_candles(length=requestlength)
        self.chart_plotter.plot_currentCandle(candles)
        if self.lastindicator is 'Overview':
            indicatordata = Indicator_Manager.get_activeindicatordata(2)
        else:
            indicatordata = Indicator_Manager.get_indicatordata(self.lastindicator,2)
        self.chart_plotter.plot_currentIndicator(indicatordata)

    def plot_chart(self, indicatorname='Overview'):
        requestlength = self.length_slider.value()
        Candle_Manager.load_candles(self.symbol_input.text(),self.interval_comboBox.currentText())
        candles = Candle_Manager.get_candles(length=requestlength)
        self.chart_plotter.set_newscene()
        self.chart_plotter.plot_frame()
        self.chart_plotter.plot_chart(candles)
        if indicatorname is 'Overview':
            indicatordata = Indicator_Manager.get_activeindicatordata(requestlength)
        else:
            indicatordata = Indicator_Manager.get_indicatordata(indicatorname,requestlength)
        self.chart_plotter.plot_indicator(indicatordata)
        self.lastindicator = indicatorname
        self.reinitiate_pricestream(self.symbol_input.text())

    def reinitiate_pricestream(self, symbol):
        if symbol != self.currentStream:
            API_Manager.close_klinestream()        
            API_Manager.open_klinesstream(symbol)
            self.currentStream = symbol

    def on_addIndicatorbutton_pressed(self):
        pass
        

    def on_save_indicator(self):
        self.indicatorsettings_view.save_settings()
        self.indicator_stack.setCurrentIndex(0)
        self.plot_chart(indicatorname=self.currentindicator)

    def on_indicatorbutton_pressed(self, name):
        self.plot_chart(indicatorname=name)
        self.indicator_stack.setCurrentIndex(1)
        values = Indicator_Manager.get_indicator_values(name)
        self.indicatorsettings_view.add_items(name,values)
        self.currentindicator = name

if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("CryptoPrinter") 
    window = MainWindow()
    app.exec_()
    