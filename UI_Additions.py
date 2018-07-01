from PyQt5 import QtCore, QtGui, QtWidgets
from HelperClasses import Translator
import Helper

class ChartPlotter(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(QtWidgets.QGraphicsView,self).__init__(*args,**kwargs)
        self.chartsize = 0.5
        self.indicatorsize = 0.4
        self.space = (1-(self.chartsize+self.indicatorsize))/3
        self.widthspace = 0.05

    def set_newscene(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        #self.scene.addLine()

    def plot_chart(self, candles):
        extremes = Helper.get_extremes(candles)
        candleswidth = self.width()/len(candles)
        y_trans = Translator(extremes['max'],
                            extremes['min'],
                            self.height() * self.space
                            , self.height() * self.chartsize)
        x_trans = Translator(len(candles), 0,
                            self.width()- self.width()*self.widthspace,0 )
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

    def plot_indicator(self, indicatordata):      
        pen = QtGui.QPen(QtCore.Qt.black,3)
        y_trans = Translator(-150, 150, self.height() * (self.chartsize + self.space), self.height() - (self.height() * self.space))
        x_trans = Translator(0, len(indicatordata), 
                                self.width()- self.width()*self.widthspace,0 )
        for i in range(len(indicatordata)-1):
            self.scene.addLine(x_trans.t(i),y_trans.t(indicatordata[i]),
                                x_trans.t(i-1),y_trans.t(indicatordata[i-1]),pen)

class IndicatorOverviewLister(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(QtWidgets.QListView,self).__init__(*args,**kwargs)
    
    def add_items(self, items):
        for item in items:
            newitem = QtWidgets.QListWidgetItem()
            widget = IndicatorOverviewItem()
            widget.setup_Widget(item)
            newitem.setSizeHint(widget.sizeHint())
            self.addItem(newitem)
            self.setItemWidget(newitem,widget)

class IndicatorOverviewItem(QtWidgets.QListWidget):
    def setup_Widget(self,name):
        self.name = name
        layout = QtWidgets.QHBoxLayout()
        checkbox = QtWidgets.QCheckBox()
        button = QtWidgets.QPushButton(name)
        button.pressed.connect(self.on_indicator_pressed)
        layout.addWidget(checkbox)
        layout.addWidget(button)
        self.setLayout(layout)

    def on_indicator_pressed(self):
        currentobject = self
        for i in range(7):
            currentobject = currentobject.parentWidget()
        currentobject.on_indicatorbutton_pressed(self.name)

class IndicatorSettingsLister(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(QtWidgets.QListView,self).__init__(*args,**kwargs)
    
    def add_items(self, values):
        for key in values:
            newitem = QtWidgets.QListWidgetItem()
            widget = IndicatorSettingsItem()
            widget.setup_Widget(key,values[key])
            newitem.setSizeHint(widget.sizeHint())
            self.addItem(newitem)
            self.setItemWidget(newitem,widget)

class IndicatorSettingsItem(QtWidgets.QListWidget):
    def setup_Widget(self,key,value):
        self.key = key
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(key)
        value = QtWidgets.QLineEdit(value)
        layout.addWidget(label)
        layout.addWidget(value)
        self.setLayout(layout)

