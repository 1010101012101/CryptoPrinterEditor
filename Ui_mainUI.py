# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/manuel/projects/CryptoPrinter/mainUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from Plotter import ChartPlotter, IndicatorPlotter

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.chart_plotter = ChartPlotter(self.centralwidget)
        self.chart_plotter.setGeometry(QtCore.QRect(0, 40, 1000, 300))
        self.chart_plotter.setFrameShape(QtWidgets.QFrame.Box)
        self.chart_plotter.setFrameShadow(QtWidgets.QFrame.Plain)
        self.chart_plotter.setLineWidth(1)
        self.chart_plotter.setObjectName("chart_plotter")
        self.indicator_plotter = IndicatorPlotter(self.centralwidget)
        self.indicator_plotter.setGeometry(QtCore.QRect(0, 380, 1000, 220))
        self.indicator_plotter.setFrameShape(QtWidgets.QFrame.Box)
        self.indicator_plotter.setFrameShadow(QtWidgets.QFrame.Plain)
        self.indicator_plotter.setLineWidth(1)
        self.indicator_plotter.setObjectName("indicator_plotter")
        self.symbol_input = QtWidgets.QLineEdit(self.centralwidget)
        self.symbol_input.setGeometry(QtCore.QRect(0, 0, 150, 40))
        self.symbol_input.setObjectName("symbol_input")
        self.symbol_input.setText('BTCUSDT')
        self.plot_button = QtWidgets.QPushButton(self.centralwidget)
        self.plot_button.setGeometry(QtCore.QRect(900, 0, 100, 40))
        self.plot_button.setObjectName("plot_button")
        self.length_slider = QtWidgets.QSlider(self.centralwidget)
        self.length_slider.setGeometry(QtCore.QRect(150, 0, 600, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.length_slider.sizePolicy().hasHeightForWidth())
        self.length_slider.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.length_slider.setFont(font)
        self.length_slider.setMinimum(10)
        self.length_slider.setMaximum(500)
        self.length_slider.setSingleStep(10)
        self.length_slider.setProperty("value", 200)
        self.length_slider.setTracking(True)
        self.length_slider.setOrientation(QtCore.Qt.Horizontal)
        self.length_slider.setInvertedAppearance(False)
        self.length_slider.setInvertedControls(False)
        self.length_slider.setObjectName("length_slider")
        self.length_label = QtWidgets.QLabel(self.centralwidget)
        self.length_label.setGeometry(QtCore.QRect(750, 0, 50, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.length_label.sizePolicy().hasHeightForWidth())
        self.length_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.length_label.setFont(font)
        self.length_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.length_label.setLineWidth(5)
        self.length_label.setScaledContents(False)
        self.length_label.setAlignment(QtCore.Qt.AlignCenter)
        self.length_label.setWordWrap(False)
        self.length_label.setObjectName("length_label")
        self.interval_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.interval_comboBox.setGeometry(QtCore.QRect(800, 0, 100, 40))
        self.interval_comboBox.setObjectName("interval_comboBox")
        self.indicator_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.indicator_comboBox.setGeometry(QtCore.QRect(0, 340, 370, 40))
        self.indicator_comboBox.setObjectName("indicator_comboBox")
        self.key_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.key_comboBox.setGeometry(QtCore.QRect(370, 340, 300, 40))
        self.key_comboBox.setObjectName("key_comboBox")
        self.value_input = QtWidgets.QLineEdit(self.centralwidget)
        self.value_input.setGeometry(QtCore.QRect(670, 340, 230, 40))
        self.value_input.setObjectName("value_input")
        self.indicatorsave_button = QtWidgets.QPushButton(self.centralwidget)
        self.indicatorsave_button.setGeometry(QtCore.QRect(900,340,100,40))
        self.indicatorsave_button.setObjectName("indicatorsave_button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plot_button.setText(_translate("MainWindow", "Plot"))
        self.length_label.setText(_translate("MainWindow", "100"))

