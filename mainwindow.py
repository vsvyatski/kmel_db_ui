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

        model = QStandardItemModel(self.__ui.driveList)
        self.__ui.driveList.setModel(model)
        self.__ui.driveList.selectionModel().selectionChanged.connect(self.__driveListSelectionChanged)

        self.__loadUsbDrivesIntoView()

    def __loadUsbDrivesIntoView(self):
        model: QStandardItemModel = self.__ui.driveList.model()
        model.clear()
        for drive_info in driveutils.get_fat_usb_mounts():
            item = QStandardItem(QIcon(':/images/usbFlash'), drive_info.label)
            item.setData(drive_info.mount_point)
            model.appendRow(item)

        self.__changeActionAvailabilityBasedOnDriveSelection(False)

    def __changeActionAvailabilityBasedOnDriveSelection(self, drive_selected: bool):
        self.__ui.actionGenerate.setEnabled(drive_selected)
        self.__ui.actionView.setEnabled(drive_selected)

    @pyqtSlot()
    def refreshActionTriggered(self):
        self.__loadUsbDrivesIntoView()

    @pyqtSlot(QItemSelection, QItemSelection)
    def __driveListSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        self.__changeActionAvailabilityBasedOnDriveSelection(not selected.isEmpty())
