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
        self.indicatoroverview_view.add_items(Indicator_Manager.get_indicator_names())
        self.show()

    def plot_chart(self, indicatorname='Overview'):
        self.chart_plotter.set_newscene()
        length = self.length_slider.value()
        Candle_Manager.load_candles(self.symbol_input.text(),self.interval_comboBox.currentText())
        candles = Candle_Manager.get_candles(length=length)
        self.chart_plotter.plot_chart(candles)
        if indicatorname is 'Overview':
            indicatordata = Indicator_Manager.get_activeindicatordata(length)
        else:
            indicatordata = Indicator_Manager.get_indicatordata(indicatorname,length)
        self.chart_plotter.plot_indicator(indicatordata)
    
    def on_value_changed(self):
        self.length_label.setText(str(self.length_slider.value()))

    def on_key_changed(self):
        values = Indicator_Manager.get_indicator_values(self.indicator_comboBox.currentText())
        self.value_input.setText(str(values[self.key_comboBox.currentText()]))

    def on_save_indicator(self):
        Indicator_Manager.set_indicator(self.indicator_comboBox.currentText(), 
                                        self.key_comboBox.currentText(),
                                        self.value_input.text())

    def on_indicatorbutton_pressed(self, name):
        self.plot_chart(indicatorname=name)
        self.indicator_stack.setCurrentIndex(1)
        values = Indicator_Manager.get_indicator_values(name)
        self.key_comboBox.clear()
        for key in values:
            self.key_comboBox.addItem(key)
    
if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("CryptoPrinter") 
    window = MainWindow()
    app.exec_()
    