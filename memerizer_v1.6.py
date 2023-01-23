# -*- coding: utf-8 -*-
import sys
import pandas as pd

from ui import MainWindow
from random import random, randint, sample

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

GREY    = (225, 225, 225)
GREEN   = (119, 195, 107)
RED     = (233, 95,  67)
BLACK   = (0,   0,   0)


class MemerizerGUI(QMainWindow):
    def __init__(self, excelFile):
        super().__init__()

        self.page = 0               # current page
        self.saveIterval = 10       # auto save interval, page
        self.pageIterval = 4000     # page iterval, msec
        self.timerIterval = 1000    # timer iterval, msec
        self.reviewRate = 0.2       # the probablity of reviewing
        self.history = []           # word history for recurrence
        self.answerFlag = False     # this page has been answered
        self.pauseFlag = False      # progress bar is paused

        # button color, green for right and red for wrong
        self.colorList = [GREY for _ in range(4)]

        # MainWindow UI init
        self.MainWindowUI = MainWindow.Ui_MainWindow()
        self.MainWindowUI.setupUi(self)
        self.MainWindowUI.pushButtonPause.setVisible(False)
        self.MainWindowUI.pushButtonPrevious.setVisible(False)
        self.setButtonColor()
        self.setFixedSize(self.width(), self.height())

        # MainWindow function
        self.MainWindowUI.pushButton0.clicked.connect(self.pushButton0Clicked)
        self.MainWindowUI.pushButton1.clicked.connect(self.pushButton1Clicked)
        self.MainWindowUI.pushButton2.clicked.connect(self.pushButton2Clicked)
        self.MainWindowUI.pushButton3.clicked.connect(self.pushButton3Clicked)
        self.MainWindowUI.pushButtonNext.clicked.connect(self.pushButtonNextClicked)
        self.MainWindowUI.pushButtonPause.clicked.connect(self.pushButtonPauseClicked)
        self.MainWindowUI.pushButtonPrevious.clicked.connect(self.pushButtonPreviousClicked)
        self.MainWindowUI.spinBox.valueChanged.connect(self.spinBoxValueChanged)

        # timer init
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setProgressBar)

        # data init
        self.excelFile = excelFile
        self.data = pd.read_excel(self.excelFile)
        self.idxIter = range(len(self.data))
        self.answer = -1
        self.wordIdx = -1

        # update data on this page
        self.update()

    def update(self):
        # check if a new page
        if self.page >= len(self.history):
            self.answer, word, pos, meaning = self.sample()
            self.history.append((self.answer, word, pos, meaning))
        else:
            self.answer, word, pos, meaning = self.history[self.page]

        self.MainWindowUI.labelText.setText(word)
        self.MainWindowUI.pushButton0.setText("{} {}".format(pos[0], meaning[0]))
        self.MainWindowUI.pushButton1.setText("{} {}".format(pos[1], meaning[1]))
        self.MainWindowUI.pushButton2.setText("{} {}".format(pos[2], meaning[2]))
        self.MainWindowUI.pushButton3.setText("{} {}".format(pos[3], meaning[3]))

    def sample(self):
        wordIdxList = sample(self.idxIter, 4)
        answer = randint(0, 3)

        self.MainWindowUI.labelText.setStyleSheet("color: rgb{}".format(BLACK))
        if random() < self.reviewRate:
            wrongData = self.data[self.data["forget"] > 0]
            wrongDataNum = len(wrongData)
            if wrongDataNum != 0:
                self.MainWindowUI.labelText.setStyleSheet("color: rgb{}".format(GREEN))
                if wrongDataNum > 3:
                    wrongDataSample = wrongData.sample(n=4)
                    wordIdxList = list(map(int, wrongDataSample.index))
                else:
                    wrongDataSample = wrongData.sample(n=1)
                    wordIdxList[answer] = int(wrongDataSample.index[0])
        self.wordIdx = wordIdxList[answer]

        word = self.data.loc[self.wordIdx, "word"]
        pos = [self.data.loc[i, "pos"] for i in wordIdxList]
        meaning = [self.data.loc[i, "meaning"] for i in wordIdxList]
        return answer, word, pos, meaning

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
            self.data.loc[self.wordIdx, "forget"] += 1

        self.setButtonColor()
        self.timer.start(self.timerIterval)
        self.MainWindowUI.pushButtonPause.setVisible(True)

        if (self.page + 1) % self.saveIterval == 0:
            self.saveFile()

    def pushButton0Clicked(self):
        if not self.answerFlag:
            self.answerFlag = True
            self.answerEvent(0)

    def pushButton1Clicked(self):
        if not self.answerFlag:
            self.answerFlag = True
            self.answerEvent(1)

    def pushButton2Clicked(self):
        if not self.answerFlag:
            self.answerFlag = True
            self.answerEvent(2)

    def pushButton3Clicked(self):
        if not self.answerFlag:
            self.answerFlag = True
            self.answerEvent(3)

    def pushButtonNextClicked(self):
        self.timer.stop()
        self.MainWindowUI.progressBar.setValue(0)
        self.MainWindowUI.pushButtonPause.setVisible(False)
        self.MainWindowUI.pushButtonPrevious.setVisible(True)
        self.MainWindowUI.pushButtonPause.setText("| |")
        self.pauseFlag = False

        self.page += 1
        self.answerFlag = False

        self.update()
        self.colorList = [GREY for _ in range(4)]
        self.setButtonColor()

    def pushButtonPauseClicked(self):
        if self.pauseFlag:
            self.pauseFlag = False
            self.timer.start(self.timerIterval)
            self.MainWindowUI.pushButtonPause.setText("| |")
        else:
            self.pauseFlag = True
            self.timer.stop()
            self.MainWindowUI.pushButtonPause.setText("▶")

    def pushButtonPreviousClicked(self):
        self.timer.stop()
        self.MainWindowUI.progressBar.setValue(0)
        self.MainWindowUI.pushButtonPause.setVisible(False)
        if self.page == 0:
            self.MainWindowUI.pushButtonPrevious.setVisible(False)
        self.MainWindowUI.pushButtonPause.setText("| |")
        self.pauseFlag = False

        self.page -= 1
        self.answerFlag = False

        self.update()
        self.colorList = [GREY for _ in range(4)]
        self.setButtonColor()

    def spinBoxValueChanged(self):
        self.pageIterval = self.MainWindowUI.spinBox.value() * 1000

    def setProgressBar(self):
        maxValue = self.MainWindowUI.progressBar.maximum()
        value = self.MainWindowUI.progressBar.value()
        value += int(self.timerIterval / self.pageIterval * maxValue)
        if value >= maxValue:
            value = 0
            self.timer.stop()
            self.pushButtonNextClicked()
        self.MainWindowUI.progressBar.setValue(value)

    def saveFile(self):
        try:
            self.data.to_excel(self.excelFile, index=False)
        except Exception as ex:
            w = QMessageBox.critical(self, "Message", "{}\r\n[Hint] Maybe the xlsx is occupied.".format(ex))
            return False
        else:
            return True

    def closeEvent(self, e):
        r = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            if self.saveFile():
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()


if __name__ == "__main__":
    excelFile = "./gre.xlsx"
    app = QApplication(sys.argv)
    gui = MemerizerGUI(excelFile)
    gui.show()
    sys.exit(app.exec_())
