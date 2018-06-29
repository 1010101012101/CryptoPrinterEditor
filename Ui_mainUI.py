# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/manuel/projects/CryptoPrinter/mainUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Plotter import IndicatorPlotter,ChartPlotter

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.chart_plotter = ChartPlotter(self.centralwidget)
        self.chart_plotter.setGeometry(QtCore.QRect(0, 40, 791, 301))
        self.chart_plotter.setObjectName("chart_plotter")
        self.indicator_plotter = IndicatorPlotter(self.centralwidget)
        self.indicator_plotter.setGeometry(QtCore.QRect(0, 350, 791, 241))
        self.indicator_plotter.setObjectName("indicator_plotter")
        self.symbol_input = QtWidgets.QLineEdit(self.centralwidget)
        self.symbol_input.setGeometry(QtCore.QRect(0, 0, 113, 32))
        self.symbol_input.setObjectName("symbol_input")
        self.load_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_button.setGeometry(QtCore.QRect(120, 0, 88, 34))
        self.load_button.setObjectName("load_button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load_button.setText(_translate("MainWindow", "LoadAnPlot"))

