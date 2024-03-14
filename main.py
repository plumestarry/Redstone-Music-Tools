import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox, QErrorMessage
import ui_design

def excepthook(exctype, value, traceback):
    error_dialog = QErrorMessage()
    error_dialog.showMessage('{}: {}'.format(exctype.__name__, value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    #调自定义的界面（即刚转换的.py对象）
    #这里也引用了一次helloworld.py文件的名字注意
    sys.excepthook = excepthook
    Ui = ui_design.Ui_stonemusic()
    Ui.setupUi(MainWindow)
    #显示窗口并释放资源
    MainWindow.show()
    sys.exit(app.exec_())

