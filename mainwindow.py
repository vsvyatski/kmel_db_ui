from ui_mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
import driveutils
from PyQt5.QtCore import pyqtSlot, QItemSelection, Qt, QPoint
import subprocess
import os
import sys
import asyncqt
import asyncio


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

    def __get_selected_drive_mount_point(self):
        selection_model = self.__ui.driveList.selectionModel()
        if not selection_model.hasSelection():
            return None

        model_index = selection_model.selectedIndexes()[0]
        return model_index.data(Qt.UserRole + 1)

    @pyqtSlot()
    def viewActionTriggered(self):
        drive_mount_point = self.__get_selected_drive_mount_point()
        if drive_mount_point is None:
            return

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

    @pyqtSlot(QPoint)
    def terminalLogCustomContextMenuRequested(self, pos: QPoint):
        custom_menu = self.__ui.terminalLogWindow.createStandardContextMenu(pos)
        custom_menu.addSeparator()
        custom_menu.addAction(self.__ui.actionClearLog)

        custom_menu.exec(self.__ui.terminalLogWindow.mapToGlobal(pos))

    @pyqtSlot()
    def clearLogActionTriggered(self):
        self.__ui.terminalLogWindow.clear()

    @asyncqt.asyncSlot()
    async def generateActionTriggered(self):
        drive_mount_point = self.__get_selected_drive_mount_point()
        if drive_mount_point is None:
            return

        dapgen_path = os.path.join(os.path.dirname(__file__), 'kmeldb_cli/DapGen.py')

        kmeldb_cli_process = await asyncio.create_subprocess_exec(sys.executable, dapgen_path,
                                                                  stdout=asyncio.subprocess.PIPE,
                                                                  stderr=asyncio.subprocess.PIPE)

        stdout_stream = kmeldb_cli_process.stdout
        leftover_data = bytearray()
        while not stdout_stream.at_eof() or len(leftover_data) > 0:
            separator_encountered = False
            while not separator_encountered:
                leftover_data += await stdout_stream.read(64)
                separator_index = -1
                for index, b in enumerate(leftover_data):
                    if b == ord(b'\r') or b == ord(b'\n'):
                        separator_index = index
                        break
                if separator_index != -1:
                    separator_encountered = True
                    meaningful_data = leftover_data[0:separator_index]
                    leftover_data = leftover_data[separator_index + 1:]
                else:
                    leftover_data += leftover_data[separator_index + 1:]

            text = meaningful_data.decode()
            # TODO: insert or append text properly treating \r and \n and using void QPlainTextEdit::moveCursor
            self.__ui.terminalLogWindow.appendPlainText(text)

        await kmeldb_cli_process.wait()
