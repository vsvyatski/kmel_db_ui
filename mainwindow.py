from ui_mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
import driveutils
from PyQt5.QtCore import pyqtSlot, QItemSelection, Qt
import subprocess
import os


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

    @pyqtSlot()
    def viewActionTriggered(self):
        selection_model = self.__ui.driveList.selectionModel()
        if not selection_model.hasSelection():
            return

        model_index = selection_model.selectedIndexes()[0]
        drive_mount_point = model_index.data(Qt.UserRole + 1)

        # We are going to try several known file managers if they are available. If any of them cannot be found,
        # then we'll just use xdg-open (but this will not select the file).
        cmd_list = None
        for file_manager in ['dolphin', 'nemo', 'nautilus']:
            path_to_file_manager = os.path.join('/usr/bin', file_manager)
            if os.access(path_to_file_manager, os.X_OK):
                args = [path_to_file_manager, os.path.join(drive_mount_point, 'kenwood.dap')]
                if file_manager == 'dolphin':
                    args.insert(1, '--select')
                cmd_list = args
                break

        if cmd_list is None:
            cmd_list = ['xdg-open', drive_mount_point]

        subprocess.Popen(cmd_list)
