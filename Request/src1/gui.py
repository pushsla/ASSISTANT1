#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys, subprocess
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QFrame
from PyQt5.QtGui import QIcon

#subprocess.Popen('python')

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Alt+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        toolbar = self.addToolBar('It`s ME')
        toolbar.addAction(exitAction)
        #toolbar.addAction(listenAction)

        self.setGeometry(250, 250, 300, 450)
        self.setFixedSize(300, 450)
        self.setWindowIcon(QIcon('me.png'))
        self.setWindowTitle('Smart Fluffy Brick')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())