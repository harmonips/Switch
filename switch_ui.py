# -*- coding: utf-8 -*-

import sys, os, pickle
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGroupBox, QVBoxLayout, QMessageBox, QHBoxLayout, QPushButton, QCheckBox, QStyleFactory, QGridLayout, QFrame, QLabel, QTabWidget, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap

from functools import partial

from modules import relay

class UI (QMainWindow):

    def __init__(self, parent = None):
        QMainWindow .__init__(self, parent)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

        file = open('settings.txt', 'r')
        self.settings = {}
        for l in file:
            splitter = l.split(':')
            if '\n' in splitter[1]:
                splitter[1] = splitter[1][:-1]
            self.settings[splitter[0]] = splitter[1]
            print (splitter)
        self.settings['vid'] = int(self.settings['vid'], 16)
        self.settings['pid'] = int(self.settings['pid'], 16)
        self.settings['number_of_relay'] = int(self.settings['number_of_relay'])

        # print (self.settings)

        self.pictures = {}
        self.pictures['on'] = QPixmap('pictures/SWITCHON.png')
        self.pictures['off'] = QPixmap('pictures/SWITCHOFF.png')

        self.rb = relay.FT245R(self.settings['vid'], self.settings['pid'])
        self.dev = self.rb.list_dev()[0]
        print (self.dev)
        self.rb.connect(self.dev)
        self.setOFFRelais()

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Switch')
        self.setWindowIcon(QIcon(QPixmap('pictures/LOGO.png')))

        widget = QWidget()
        hbox = QHBoxLayout()
        self.relais = []
        self.bouton = []
        for n in range(self.settings['number_of_relay']):
            vbox = QVBoxLayout()
            self.relais.append(False)
            gb = QGroupBox('- %s -' %(n+1))
            gb.setLayout(vbox)
            but = QPushButton()
            but.setIcon(QIcon(self.pictures['off']))
            but.setIconSize(QSize(64,64))
            vbox.addWidget(but)
            hbox.addWidget(gb)
            self.bouton.append(but)
            but.clicked.connect(partial(self.reverse, n))
        widget.setLayout(hbox)
        self.setCentralWidget(widget)
    
    def reverse(self,n):
        self.relais[n] = not self.relais[n]
        
        if self.relais[n] == True:
            self.bouton[n].setIcon(QIcon(self.pictures['on']))
            self.rb.switchon(n+1)
        else:
            self.bouton[n].setIcon(QIcon(self.pictures['off']))
            self.rb.switchoff(n+1)
        
    
    def setOFFRelais(self):
        for i in range(4):
            self.rb.switchoff(i+1)

    def closeEvent(self, evt):
        self.setOFFRelais()
        self.rb.disconnect()


if __name__ == '__main__':
    app = QApplication([ ])

    w = UI()
    w.show()
    sys.exit(app.exec_())
