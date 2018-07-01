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
        Indicator_Manager.load_indicators()
        self.plot_button.pressed.connect(self.plot_chart)
        self.length_slider.valueChanged.connect(self.on_value_changed)
        self.interval_comboBox.addItems(['1m','3m','5m','15m','30m','1h','12h','1d','1w','1M'])
        self.indicator_comboBox.addItems(Indicator_Manager.get_indicator_names())
        self.indicator_comboBox.currentTextChanged.connect(self.on_indicator_changed)
        self.key_comboBox.currentTextChanged.connect(self.on_key_changed)
        self.indicatorsave_button.pressed.connect(self.on_save_indicator)
        self.on_indicator_changed()
        self.on_key_changed()
        self.show()

    def plot_chart(self):
        length = self.length_slider.value()
        Candle_Manager.load_candles(self.symbol_input.text(),self.interval_comboBox.currentText())
        candles = Candle_Manager.get_candles(length=length)
        self.chart_plotter.plot_chart(candles)
        indicatordata = Indicator_Manager.get_indicatordata(self.indicator_comboBox.currentText(),length)
        self.indicator_plotter.plot_indicator(indicatordata)
    
    def on_value_changed(self):
        self.length_label.setText(str(self.length_slider.value()))

    def on_indicator_changed(self):
        values = Indicator_Manager.get_indicator_values(self.indicator_comboBox.currentText())
        self.key_comboBox.clear()
        for key in values:
            self.key_comboBox.addItem(key)
    
    def on_key_changed(self):
        values = Indicator_Manager.get_indicator_values(self.indicator_comboBox.currentText())
        self.value_input.setText(str(values[self.key_comboBox.currentText()]))

    def on_save_indicator(self):
        Indicator_Manager.set_indicator(self.indicator_comboBox.currentText(), 
                                        self.key_comboBox.currentText(),
                                        self.value_input.text())
        length = self.length_slider.value()
        indicatordata = Indicator_Manager.get_indicatordata(self.indicator_comboBox.currentText(),length)
        self.indicator_plotter.plot_indicator(indicatordata)
    
if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("CryptoPrinter") 
    window = MainWindow()
    app.exec_()
    