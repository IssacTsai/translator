import UI4
import sys
import time
import keyboard
import win32clipboard

from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from googletrans import Translator

# 建立翻譯器
tr = Translator()
language = 'zh-tw'
pause = 0

# 介面功能
class MyWindow(QtWidgets.QWidget, UI4.Ui_Form):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_1.setEnabled(False)
        self.t_replace = trans()
        self.t_replace.start()
        self.t_replace.signal.connect(self.upgrade)

    def upgrade(self, txt):
        self.plainTextEdit.setPlainText(txt)

    def click(self):
        if self.plainTextEdit.toPlainText() != '':
            try:
                txt_tr = tr.translate(self.plainTextEdit.toPlainText(), dest=language).text
            except:
                txt_tr = 'Not text'
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, str(txt_tr))
            win32clipboard.CloseClipboard()
            self.plainTextEdit.setPlainText(str(txt_tr))

    def zh_tw(self):
        self.enable()
        self.pushButton_1.setEnabled(False)
        global language
        language = 'zh-tw'
        self.click()

    def en(self):
        self.enable()
        self.pushButton_2.setEnabled(False)
        global language
        language = 'en'
        self.click()

    def jp(self):
        self.enable()
        self.pushButton_3.setEnabled(False)
        global language
        language = 'ja'
        self.click()

    def zh_cn(self):
        self.enable()
        self.pushButton_4.setEnabled(False)
        global language
        language = 'zh-cn'
        self.click()

    def pause(self):
        global pause
        pause = 1 - pause
        if pause:
            self.pushButton_5.setStyleSheet("background-color : red")
            self.t_replace.pause = True
        else:
            self.pushButton_5.setStyleSheet("background-color : green")
            self.t_replace.pause = False
        self.clear()

    def clear(self):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
        self.plainTextEdit.setPlainText('')

    def enable(self):
        self.pushButton_1.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)

class trans(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super(trans, self).__init__()
        self.running = True
        self.pause = False

    def stop(self):
        self.running = False
        self.pause = True

    def run(self):
        data = ''
        while self.running:
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('c') and not self.pause:
                global language
                time.sleep(0.1)
                try:
                    win32clipboard.OpenClipboard()
                    data = win32clipboard.GetClipboardData()
                    win32clipboard.CloseClipboard()
                    txt_tr = tr.translate(data, dest=language).text
                except:
                    txt_tr = 'Not text'
                try:
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, str(txt_tr))
                    win32clipboard.CloseClipboard()
                except:
                    pass
                self.signal.emit(txt_tr)
            time.sleep(0.01)  # reduce CPU usage

# 主程式
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWindow()
    Form.setWindowTitle("Translator")
    Form.setWindowFlags(Qt.WindowMinimizeButtonHint |
                        Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
    Form.show()
    sys.exit(app.exec_())
