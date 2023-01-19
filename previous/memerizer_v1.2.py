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

        self.page = 0               # current page
        self.history = []           # word history for recurrence
        self.pause_flag = False     # progress bar is paused
        self.answer_flag = False    # this page has been answered
        self.page_iterval = 4000    # page iterval, msec
        self.timer_iterval = 500    # timer iterval, msec

        # button color, green for right and red for wrong
        self.colorList = [GREY for _ in range(4)]

        # UI init
        self.MainWindowUI = MainWindow.Ui_MainWindow()
        self.MainWindowUI.setupUi(self)
        self.MainWindowUI.pushButtonPause.setVisible(False)
        self.MainWindowUI.pushButtonPrevious.setVisible(False)
        self.setButtonColor()
        self.setFixedSize(self.width(), self.height())

        # function connect
        self.MainWindowUI.pushButton0.clicked.connect(self.pushButton0Clicked)
        self.MainWindowUI.pushButton1.clicked.connect(self.pushButton1Clicked)
        self.MainWindowUI.pushButton2.clicked.connect(self.pushButton2Clicked)
        self.MainWindowUI.pushButton3.clicked.connect(self.pushButton3Clicked)
        self.MainWindowUI.pushButtonNext.clicked.connect(self.pushButtonNextClicked)
        self.MainWindowUI.pushButtonPause.clicked.connect(self.pushButtonPauseClicked)
        self.MainWindowUI.pushButtonPrevious.clicked.connect(self.pushButtonPreviousClicked)

        # timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setProgressBar)

        # data init
        self.excel_file = excel_file
        self.data = pd.read_excel(self.excel_file)
        self.idx = list(range(len(self.data)))
        self.answer = -1
        self.wordIdxInFile = -1

        # update data on this page
        self.update()

    def update(self):
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
        wordIdxList = sample(self.idx, 4)
        wordIdx = randint(0, 3)
        self.wordIdxInFile = wordIdxList[wordIdx]
        word = self.data.loc[self.wordIdxInFile, "word"]
        pos = [self.data.loc[i, "pos"] for i in wordIdxList]
        meaning = [self.data.loc[i, "meaning"] for i in wordIdxList]
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
            self.data.loc[self.wordIdxInFile, "forget"] += 1

        self.setButtonColor()
        self.timer.start(self.timer_iterval)
        self.MainWindowUI.pushButtonPause.setVisible(True)

    def pushButton0Clicked(self):
        if not self.answer_flag:
            self.answer_flag = True
            self.answerEvent(0)

    def pushButton1Clicked(self):
        if not self.answer_flag:
            self.answer_flag = True
            self.answerEvent(1)

    def pushButton2Clicked(self):
        if not self.answer_flag:
            self.answer_flag = True
            self.answerEvent(2)

    def pushButton3Clicked(self):
        if not self.answer_flag:
            self.answer_flag = True
            self.answerEvent(3)

    def pushButtonNextClicked(self):
        self.timer.stop()
        self.MainWindowUI.progressBar.setValue(0)
        self.MainWindowUI.pushButtonPause.setVisible(False)
        self.MainWindowUI.pushButtonPrevious.setVisible(True)

        self.page += 1
        self.answer_flag = False

        self.update()
        self.colorList = [GREY for _ in range(4)]
        self.setButtonColor()

    def pushButtonPauseClicked(self):
        if self.pause_flag:
            self.pause_flag = False
            self.timer.start(self.timer_iterval)
            self.MainWindowUI.pushButtonPause.setText("Pause")
        else:
            self.pause_flag = True
            self.timer.stop()
            self.MainWindowUI.pushButtonPause.setText("Continue")

    def pushButtonPreviousClicked(self):
        self.timer.stop()
        self.MainWindowUI.progressBar.setValue(0)
        self.MainWindowUI.pushButtonPause.setVisible(False)
        if self.page == 0:
            self.MainWindowUI.pushButtonPrevious.setVisible(False)

        self.page -= 1
        self.answer_flag = False

        self.update()
        self.colorList = [GREY for _ in range(4)]
        self.setButtonColor()

    def setProgressBar(self):
        value = self.MainWindowUI.progressBar.value()
        value += int(self.timer_iterval / self.page_iterval * 100)
        if value >= 100:
            value = 0
            self.timer.stop()
            self.pushButtonNextClicked()
        self.MainWindowUI.progressBar.setValue(value)

    def closeEvent(self, e):
        r = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            try:
                self.data.to_excel(self.excel_file, index=False)
            except:
                w = QMessageBox.critical(self, "Message", "Error: xlsx occupation.")
                e.ignore()
            else:
                e.accept()
        else:
            e.ignore()


if __name__ == "__main__":
    excel_file = "./gre.xlsx"
    app = QApplication(sys.argv)
    gui = MemerizerGUI(excel_file)
    gui.show()
    sys.exit(app.exec_())
