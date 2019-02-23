from ui_mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
import driveutils
from PyQt5.QtCore import pyqtSlot, QItemSelection


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.__loadUsbDrivesIntoView()
        self.__ui.driveList.selectionModel().selectionChanged.connect(MainWindow.__driveListSelectionChanged)

    def __loadUsbDrivesIntoView(self):
        model = QStandardItemModel(self.__ui.driveList)
        for drive_info in driveutils.get_fat_usb_mounts():
            item = QStandardItem(QIcon(':/images/usbFlash'), drive_info.label)
            item.setData(drive_info.mount_point)
            model.appendRow(item)

        self.__ui.driveList.setModel(model)

    @pyqtSlot()
    def refreshActionTriggered(self):
        self.__loadUsbDrivesIntoView()

    @pyqtSlot(QItemSelection)
    def __driveListSelectionChanged(self, selected: QItemSelection):
        print(selected.count())
        print('selection changed')
