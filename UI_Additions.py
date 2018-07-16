from PyQt5 import QtCore, QtGui, QtWidgets
from HelperClasses import Translator
import Helper
import Indicator_Manager

class ChartPlotter(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(QtWidgets.QGraphicsView,self).__init__(*args,**kwargs)
        self.candleItems = []
        self.currentCandle = []
        self.indicatorItems = []
        self.currentIndicator = []
        self.chartsize = 0.6
        self.indicatorsize = 0.25
        self.space = (1-(self.chartsize+self.indicatorsize))/4
        self.widthspace = 0.09
        self.candleWidth = 0.65
        self.chart_x_trans = None
        self.chart_y_trans = None
        self.indi_x_trans = None
        self.indi_y_trans = None
        self.green = QtGui.QColor(46, 204, 113)
        self.red = QtGui.QColor(231, 76, 60)
        self.lastprint = ''

    def init_plotter(self):
        self.set_newscene()
        self.plot_frame()

    def set_newscene(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        self.currentCandle.clear()
        self.candleItems.clear()
        self.currentIndicator.clear()
        self.indicatorItems.clear()

    def plot_frame(self):
        width = self.width()-8
        height = self.height()-8
        y_trans = Translator(0, 1, 0, self.height())
        x_trans = Translator(0,1,0,width)

        textItems = []
        x = x_trans.t(1- self.widthspace) + 10
        y1 = y_trans.t(self.space)
        self.scene.addLine(0,y1,x,y1,QtGui.QPen(QtCore.Qt.DashLine))  
        self.top_text = TextPairWidget()
        self.top_text.setup_Widget(x)
        self.top_text.set_Widget(posY = y1)
        textItems += self.top_text.get_TextItems()

        y2 = y_trans.t(self.space + self.chartsize)
        self.scene.addLine(0,y2,x,y2,QtGui.QPen(QtCore.Qt.DashLine))
        self.bot_text = TextPairWidget()
        self.bot_text.setup_Widget(x)
        self.bot_text.set_Widget(posY = y2)
        textItems += self.bot_text.get_TextItems()
        
        self.current_text = TextPairWidget()
        self.current_text.setup_Widget(x,maxY=[y1,y2])
        self.current_text.set_Widget(posY=200)
        textItems += self.current_text.get_TextItems()

        self.indi_y_trans = Translator(150, -150, 
                            self.height() * (self.chartsize + (self.space*2)), 
                            self.height() - (self.height() * self.space))

        y = self.indi_y_trans.t(100)
        inditop_text = QtWidgets.QGraphicsTextItem('100')
        inditop_text.setPos(x,y-10)
        inditop_line = QtWidgets.QGraphicsLineItem(0,y,x,y)
        #self.scene.addItem(inditop_text)
        self.scene.addItem(inditop_line)

        y = self.indi_y_trans.t(-100)
        indibot_text = QtWidgets.QGraphicsTextItem('-100')
        indibot_text.setPos(x,y-10)
        indibot_line = QtWidgets.QGraphicsLineItem(0,y,x,y)
        #self.scene.addItem(indibot_text)
        self.scene.addItem(indibot_line)

        for item in textItems:
            self.scene.addItem(item)

        self.scene.addLine(0,0,width,0)
        self.scene.addLine(0,height,width,height)
        self.scene.addLine(0,0,0,height)
        self.scene.addLine(width,0,width,height)
        
    def plot_currentCandle(self,candles):
        candleswidth = self.width()/len(candles) * self.candleWidth
        self.__calculate_chart_translations(candles)
        for candle in self.currentCandle:
            self.scene.removeItem(candle)
        self.currentCandle.clear()
        candle = candles[0]
        graphic = self.__get_candleGraphic(candle,candleswidth,0)
        graphic[2].setWidth(1)
        graphic[2].setStyle(QtCore.Qt.DashLine)
        y = self.chart_y_trans.t(candle.close)
        newline2 = QtWidgets.QGraphicsLineItem(0, int(y),
                            self.width() - (self.width() * self.widthspace), int(y),)
        newline2.setPen(graphic[2])
        change = ((candle.close - candle.open) / candle.open)*100
        self.current_text.set_Widget(price=candle.close,precentage=change,posY=y)
        self.currentCandle.append(newline2)
        self.currentCandle.append(graphic[0])
        self.currentCandle.append(graphic[1])
        self.scene.addItem(newline2)
        self.scene.addItem(graphic[0])
        self.scene.addItem(graphic[1])

    def plot_chart(self, candles):
        candleswidth = self.width()/len(candles)* self.candleWidth
        self.__calculate_chart_translations(candles)
        for candle in self.candleItems:
            self.scene.removeItem(candle)
        self.candleItems.clear()
        for i in range(len(candles)-1):
            if i is not 0:
                candle = candles[i]
                graphic = self.__get_candleGraphic(candle, candleswidth,i)
                self.candleItems.append(graphic[0])
                self.candleItems.append(graphic[1])
                self.scene.addItem(graphic[0])
                self.scene.addItem(graphic[1])

    def __get_candleGraphic(self, candle, candleswidth, i):
        dif = candle.close - candle.open 
        if dif >= 0:
            color = self.green
        else:
            color = self.red
        pen = QtGui.QPen(color)
        brush = QtGui.QBrush(color)    
        newrect = QtWidgets.QGraphicsRectItem(int(self.chart_x_trans.t(i)-candleswidth),
                    int(self.chart_y_trans.t(candle.open)),
                    int(candleswidth),
                    int(self.chart_y_trans.t(candle.close) - 
                    self.chart_y_trans.t(candle.open)))
        newrect.setBrush(brush)
        newrect.setPen(pen)
        x = int(self.chart_x_trans.t(i)-(candleswidth/2))
        newline = QtWidgets.QGraphicsLineItem(x, int(self.chart_y_trans.t(candle.high)),
                            x, int(self.chart_y_trans.t(candle.low)))
        newline.setPen(pen)     
        return [newrect,newline,pen]        
    
    def __calculate_chart_translations(self, candles):
        extremes = Helper.get_extremes(candles)
        maxP = extremes['max']
        minP = extremes['min']
        currentCandle = candles[0]
        topprecentage = ((maxP / currentCandle.close) - 1) * 100
        botprecentage = ((minP - currentCandle.close) / currentCandle.close) * 100
        self.top_text.set_Widget(price=maxP,precentage=topprecentage)
        self.bot_text.set_Widget(price=minP,precentage=botprecentage)
        self.chart_y_trans = Translator(maxP, minP,
                            self.height() * self.space,
                            self.height() * (self.chartsize + self.space))
        self.chart_x_trans = Translator(0, len(candles),
                            self.width() - (self.width()*self.widthspace),0)

    def __calculate_indicator_translations(self, indicatordata):
        self.indi_y_trans = Translator(150, -150, 
                            self.height() * (self.chartsize + (self.space*2)), 
                            self.height() - (self.height() * self.space))
        self.indi_x_trans = Translator(0, len(indicatordata), 
                            self.width()- self.width()*self.widthspace,0 )
          
    def plot_indicator(self, indicatordata):      
        self.lastprint = ''
        pen = QtGui.QPen(QtCore.Qt.black,2)      
        self.__calculate_indicator_translations(indicatordata)
        for indicator in self.indicatorItems:
            self.scene.removeItem(indicator)
        self.indicatorItems.clear()
        for j in range(len(indicatordata)):
            i = len(indicatordata) - j - 2
            if i > 0:
                newline = QtWidgets.QGraphicsLineItem(self.indi_x_trans.t(i),self.indi_y_trans.t(indicatordata[i]),
                                                    self.indi_x_trans.t(i-1),self.indi_y_trans.t(indicatordata[i-1]))
                newline.setPen(pen)
                currentindi = indicatordata[i]
                actionline = False
                if currentindi <= 100 and indicatordata[i+1] > 100:
                    if self.lastprint is not 'short':
                        self.lastprint = 'short'
                        actionline = True
                        pen2 = QtGui.QPen(self.red, 2, QtCore.Qt.DashLine)
                if currentindi >= -100 and indicatordata[i+1] < -100:
                    if self.lastprint is not 'long':
                        self.lastprint = 'long'
                        actionline = True
                        pen2 = QtGui.QPen(self.green, 2, QtCore.Qt.DashLine)

                if actionline is True:
                    x = self.indi_x_trans.t(i)
                    y1 = self.height() * self.space
                    y2 = self.height() - (self.height() * self.space)
                    newline2 = QtWidgets.QGraphicsLineItem(x,y1,x,y2)
                    newline2.setPen(pen2)
                    self.scene.addItem(newline2)
                    self.indicatorItems.append(newline2)  

                self.scene.addItem(newline)
                self.indicatorItems.append(newline)

    def plot_currentIndicator(self, indicatordata):
        pen = QtGui.QPen(QtCore.Qt.black,2)
        for indicator in self.currentIndicator:
            self.scene.removeItem(indicator)
        self.currentIndicator.clear()
        newline = QtWidgets.QGraphicsLineItem(self.indi_x_trans.t(1),self.indi_y_trans.t(indicatordata[1]),
                                            self.indi_x_trans.t(0),self.indi_y_trans.t(indicatordata[0]))
        newline.setPen(pen)
        actionline = False
        currentindi = indicatordata[0]
        if currentindi <= 100 and indicatordata[1] > 100:         
            actionline = True
            pen2 = QtGui.QPen(self.red, 2, QtCore.Qt.DashLine)
        if currentindi >= -100 and indicatordata[1] < -100:
            actionline = True
            pen2 = QtGui.QPen(self.green, 2, QtCore.Qt.DashLine)

        if actionline is True:
            x = self.indi_x_trans.t(0)
            y1 = self.height() * self.space
            y2 = self.height() - (self.height() * self.space)
            newline2 = QtWidgets.QGraphicsLineItem(x,y1,x,y2)
            newline2.setPen(pen2)
            self.scene.addItem(newline2)
            self.indicatorItems.append(newline2)  

        self.scene.addItem(newline)
        self.currentIndicator.append(newline)


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
        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.stateChanged.connect(self.on_checkbox_checked)
        button = QtWidgets.QPushButton(name)
        button.pressed.connect(self.on_indicator_pressed)
        layout.addWidget(self.checkbox)
        layout.addWidget(button)
        self.setLayout(layout)

    def on_indicator_pressed(self):
        currentobject = self
        for i in range(7):
            currentobject = currentobject.parentWidget()
        currentobject.on_indicatorbutton_pressed(self.name)

    def on_checkbox_checked(self):
        state = self.checkbox.isChecked()
        if state is True:
            Indicator_Manager.add_to_active(self.name)
        else:
            Indicator_Manager.remove_from_active(self.name)

class IndicatorSettingsLister(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(QtWidgets.QListView,self).__init__(*args,**kwargs)
        self.settings = []

    
    def add_items(self, indicatorname ,values):
        self.currentindicator = indicatorname
        for key in values:
            newitem = QtWidgets.QListWidgetItem()
            widget = IndicatorSettingsItem()
            widget.setup_Widget(key,values[key])
            newitem.setSizeHint(widget.sizeHint())
            self.addItem(newitem)
            self.setItemWidget(newitem,widget)
            self.settings.append(widget)
    
    def save_settings(self):
        for widget in self.settings:
            widget.save_setting(self.currentindicator)
        self.clear()
        self.settings.clear()

class IndicatorSettingsItem(QtWidgets.QListWidget):
    def setup_Widget(self,key,value):
        self.key = key
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(str(key))
        self.value = QtWidgets.QLineEdit(str(value))
        layout.addWidget(label)
        layout.addWidget(self.value)
        self.setLayout(layout)

    def save_setting(self,name):
        try:
            Indicator_Manager.set_indicator(name,self.key,float(self.value.text()))
        except:
            print('No valid Input')

class TextPairWidget():
    def setup_Widget(self, posX, maxY=None):
        self.price_text = QtWidgets.QGraphicsTextItem()
        self.precentage_text = QtWidgets.QGraphicsTextItem()
        self.posX = posX
        if maxY != None:
            self.maxY = maxY[0] + 40
            self.minY = maxY[1] - 40
        else: 
            self.maxY = -99999
            self.minY =  99999
    
    def set_Widget(self, price=None, precentage=None, posY=None):
        if price != None:
            self.price_text.setPlainText(str(price))
        if precentage != None:
            self.precentage_text.setPlainText(str('%.3f'%(precentage)) + '%')
        if posY != None:
            if posY < self.maxY:
                self.__set_pos(self.maxY)
            elif posY > self.minY:
                self.__set_pos(self.minY)
            else:
                self.__set_pos(posY)

    def get_TextItems(self):
        return [self.price_text, self.precentage_text]

    def __set_pos(self, posY):
        self.price_text.setPos(self.posX,posY - 17)
        self.precentage_text.setPos(self.posX,posY)
