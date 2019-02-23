from ui_mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
