# -*- coding: utf-8 -*-
import sys
import pandas as pd
from ui import MainWindow
from random import randint, sample
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

GREY = (225, 225, 225)
GREEN = (119, 195, 107)
RED = (233, 95, 67)


class MemerizerGUI(QMainWindow):
    def __init__(self, excel_file):
        super().__init__()
        # ui init
        self.MainWindowUI = MainWindow.Ui_MainWindow()
        self.MainWindowUI.setupUi(self)
        self.colorList = [GREY for _ in range(4)]
        self.setButtonColor()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setProgressBar)

        # data init
        self.data = pd.read_excel(excel_file)
        self.num = len(self.data)
        self.idx = list(range(self.num))
        self.answer = 0
        self.update()

        # fixed window size
        self.setFixedSize(self.width(), self.height())

        self.MainWindowUI.pushButton0.clicked.connect(self.pushButton0Clicked)
        self.MainWindowUI.pushButton1.clicked.connect(self.pushButton1Clicked)
        self.MainWindowUI.pushButton2.clicked.connect(self.pushButton2Clicked)
        self.MainWindowUI.pushButton3.clicked.connect(self.pushButton3Clicked)
        self.MainWindowUI.pushButtonNext.clicked.connect(self.pushButtonNextClicked)

    def update(self):
        self.answer, word, pos, meaning = self.sample()
        self.MainWindowUI.labelText.setText(word)
        self.MainWindowUI.pushButton0.setText("{} {}".format(pos[0], meaning[0]))
        self.MainWindowUI.pushButton1.setText("{} {}".format(pos[1], meaning[1]))
        self.MainWindowUI.pushButton2.setText("{} {}".format(pos[2], meaning[2]))
        self.MainWindowUI.pushButton3.setText("{} {}".format(pos[3], meaning[3]))

    def sample(self):
        wordIdxList = sample(self.idx, 4)
        wordIdx = randint(0, 3)
        word = self.data.iloc[wordIdxList[wordIdx]]["word"]
        pos = [self.data.iloc[i]["pos"] for i in wordIdxList]
        meaning = [self.data.iloc[i]["meaning"] for i in wordIdxList]
        return wordIdx, word, pos, meaning

    def setButtonColor(self):
        # fmt: off
        self.MainWindowUI.pushButton0.setStyleSheet("background-color: rgb{}".format(self.colorList[0]))
        self.MainWindowUI.pushButton1.setStyleSheet("background-color: rgb{}".format(self.colorList[1]))
        self.MainWindowUI.pushButton2.setStyleSheet("background-color: rgb{}".format(self.colorList[2]))
        self.MainWindowUI.pushButton3.setStyleSheet("background-color: rgb{}".format(self.colorList[3]))
        # fmt: on

    def answerEvent(self, choice):
        self.colorList = [GREY for _ in range(4)]
        self.colorList[self.answer] = GREEN
        if choice != self.answer:
            self.colorList[choice] = RED
        self.setButtonColor()
        self.timer.start(1000)

    def pushButton0Clicked(self):
        self.answerEvent(0)

    def pushButton1Clicked(self):
        self.answerEvent(1)

    def pushButton2Clicked(self):
        self.answerEvent(2)

    def pushButton3Clicked(self):
        self.answerEvent(3)

    def pushButtonNextClicked(self):
        self.timer.stop()
        self.MainWindowUI.progressBar.setValue(0)
        self.update()
        self.colorList = [GREY for _ in range(4)]
        self.setButtonColor()

    def setProgressBar(self):
        value = self.MainWindowUI.progressBar.value()
        if value != 100:
            value += 25
        else:
            value = 0
            self.timer.stop()
            self.pushButtonNextClicked()
        self.MainWindowUI.progressBar.setValue(value)

    def closeEvent(self, e):
        r = QMessageBox.question(self, "提示", "确认退出?", QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            e.accept()
        else:
            e.ignore()


if __name__ == "__main__":
    excel_file = "./gre.xlsx"
    app = QApplication(sys.argv)
    gui = MemerizerGUI(excel_file)
    gui.show()
    sys.exit(app.exec_())
