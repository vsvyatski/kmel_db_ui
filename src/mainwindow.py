"""
Copyright (C) 2019  Vladimir Svyatski

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import asyncio
import html
import logging
import os
import subprocess
import sys

import asyncqt
from PyQt5.QtCore import pyqtSlot, QItemSelection, Qt, QPoint, QCoreApplication, QUrl, QItemSelectionModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QTextCursor, QCloseEvent, QDesktopServices
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QDialog

import aboutdialog
import driveutils
import info
import preferencesdialog
import settings
from ui_mainwindow import Ui_MainWindow

_translate = QCoreApplication.translate


# noinspection PyPep8Naming
class MainWindow(QMainWindow):
    def __init__(self, settings_obj: settings.ApplicationSettings, parent: QWidget = None):
        super().__init__(parent)

        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.__app_settings = settings_obj
        self.__initUiFromSettings()

        model = QStandardItemModel(self.__ui.driveList)
        self.__ui.driveList.setModel(model)
        self.__ui.driveList.selectionModel().selectionChanged.connect(self.__driveListSelectionChanged)

        self.__loadUsbDrivesIntoView()

    def __loadUsbDrivesIntoView(self):
        model: QStandardItemModel = self.__ui.driveList.model()
        model.clear()
        for drive_info in driveutils.get_fat_usb_mounts():
            item = QStandardItem(QIcon(':/images/usbFlash'), drive_info.label)
            item.setData(drive_info)
            model.appendRow(item)

        drive_selected = False
        if self.__app_settings.select_first_available_drive:
            drive_index = model.index(0, 0)
            if drive_index.isValid():
                self.__ui.driveList.selectionModel().select(drive_index, QItemSelectionModel.Select)
                drive_selected = True

        self.__changeActionAvailabilityBasedOnDriveSelection(drive_selected)

    def __changeActionAvailabilityBasedOnDriveSelection(self, drive_selected: bool):
        self.__ui.actionWriteDatabase.setEnabled(drive_selected)
        self.__ui.actionViewDatabase.setEnabled(drive_selected)
        self.__ui.actionUnmount.setEnabled(drive_selected)

    @pyqtSlot()
    def refreshActionTriggered(self):
        self.__loadUsbDrivesIntoView()

    # noinspection PyUnusedLocal
    @pyqtSlot(QItemSelection, QItemSelection)
    def __driveListSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        self.__changeActionAvailabilityBasedOnDriveSelection(not selected.isEmpty())

    def __getSelectedDriveMountPoint(self):
        data = self.__getSelectedDriveData()
        return data.mount_point if data is not None else None

    def __getSelectedDriveDevice(self):
        data = self.__getSelectedDriveData()
        return data.device if data is not None else None

    def __getSelectedDriveData(self):
        selection_model = self.__ui.driveList.selectionModel()
        if not selection_model.hasSelection():
            return None

        model_index = selection_model.selectedIndexes()[0]
        return model_index.data(Qt.UserRole + 1)

    @pyqtSlot()
    def viewDatabaseActionTriggered(self):
        drive_mount_point = self.__getSelectedDriveMountPoint()
        if drive_mount_point is None:
            return

        # We are going to try several known file managers if they are available. If any of them cannot be found,
        # then we'll just use xdg-open (but this will not select the file).
        cmd_list = None
        for file_manager in ['dolphin', 'nautilus', 'nemo', 'thunar']:
            path_to_file_manager = os.path.join('/usr/bin', file_manager)
            if os.access(path_to_file_manager, os.X_OK):
                args = [path_to_file_manager, os.path.join(drive_mount_point, 'kenwood.dap')]
                if file_manager == 'dolphin' or file_manager == 'nautilus':
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

    async def __readAndPrintStream(self, sr: asyncio.StreamReader, text_cursor: QTextCursor):
        leftover_data = bytearray()
        while not sr.at_eof() or len(leftover_data) > 0:
            separator_encountered = False
            meaningful_data = None
            cr_found = False
            lf_found = False
            while not separator_encountered:
                leftover_data += await sr.read(64)
                separator_index = -1
                for index, b in enumerate(leftover_data):
                    if b == ord(b'\r'):
                        separator_index = index
                        cr_found = True
                        break
                    elif b == ord(b'\n'):
                        separator_index = index
                        lf_found = True
                        break
                if separator_index != -1:
                    separator_encountered = True
                    meaningful_data = leftover_data[0:separator_index]
                    leftover_data = leftover_data[separator_index + 1:]
                else:
                    leftover_data += leftover_data[separator_index + 1:]

            text = meaningful_data.decode() if meaningful_data is not None else ''

            text_cursor.beginEditBlock()

            if cr_found:
                text_cursor.movePosition(QTextCursor.StartOfLine)
                text_cursor.insertText(text)
                i = 1
                count = len(text)
                while i <= count:
                    text_cursor.deleteChar()
                    i += 1
            elif lf_found:
                text_cursor.insertText(text + '\n')
            else:
                text_cursor.insertText(text)

            text_cursor.endEditBlock()
            self.__ui.terminalLogWindow.ensureCursorVisible()

    @asyncqt.asyncSlot()
    async def writeDatabaseActionTriggered(self):
        self.__uiBeginGenerateOperation()

        drive_mount_point = self.__getSelectedDriveMountPoint()
        if drive_mount_point is None:
            self.__uiEndGenerateOperation()
            return

        text_cursor = self.__ui.terminalLogWindow.textCursor()

        dap_generator_path = os.path.join(info.APP_DIR, 'kmeldb_cli/DapGen.py')
        text_cursor.insertText('{} {} {}\n'.format(sys.executable, dap_generator_path, drive_mount_point))

        kmeldb_cli_process = await asyncio.create_subprocess_exec(sys.executable, dap_generator_path, drive_mount_point,
                                                                  stdout=asyncio.subprocess.PIPE,
                                                                  stderr=asyncio.subprocess.PIPE)

        await self.__readAndPrintStream(kmeldb_cli_process.stdout, text_cursor)
        text_cursor.insertText('\n')
        await self.__readAndPrintStream(kmeldb_cli_process.stderr, text_cursor)
        text_cursor.insertText('\n')

        exit_code = await kmeldb_cli_process.wait()
        text_cursor.insertText(_translate('MainWindow', 'Process finished with exit code %d\n\n') % exit_code)
        self.__ui.terminalLogWindow.ensureCursorVisible()

        self.__uiEndGenerateOperation()

    def __uiBeginGenerateOperation(self):
        self.__ui.actionWriteDatabase.setEnabled(False)
        self.__ui.actionUnmount.setEnabled(False)

    def __uiEndGenerateOperation(self):
        self.__ui.actionWriteDatabase.setEnabled(True)
        self.__ui.actionUnmount.setEnabled(True)

    @pyqtSlot()
    def aboutActionTriggered(self):
        about_box = aboutdialog.AboutDialog(self)
        about_box.exec()

    def __initUiFromSettings(self):
        self.__ui.toolBar.setVisible(self.__app_settings.show_toolbar)

        if self.__app_settings.main_window_geometry is not None:
            self.restoreGeometry(self.__app_settings.main_window_geometry)

        if self.__app_settings.main_window_splitter_state is not None:
            self.__ui.splitter.restoreState(self.__app_settings.main_window_splitter_state)

    def closeEvent(self, event: QCloseEvent):
        self.__app_settings.main_window_geometry = self.saveGeometry()
        self.__app_settings.main_window_splitter_state = self.__ui.splitter.saveState()
        super().closeEvent(event)

    @pyqtSlot()
    def visitWebsiteActionTriggered(self):
        if not QDesktopServices.openUrl(QUrl('https://vsvyatski.github.io/kmeldb-ui')):
            QMessageBox.critical(self, info.APP_NAME,
                                 _translate('MainWindow',
                                            'Unable to navigate to the Github repository with the default browser.'))

    @pyqtSlot()
    def preferencesActionTriggered(self):
        preferences_dialog = preferencesdialog.PreferencesDialog(self.__app_settings, self)
        if preferences_dialog.exec() == QDialog.Accepted:
            self.__ui.toolBar.setVisible(self.__app_settings.show_toolbar)

    @pyqtSlot()
    def unmountActionTriggered(self):
        drive_device = self.__getSelectedDriveDevice()
        try:
            driveutils.unmount_usb_device(drive_device)
            self.__loadUsbDrivesIntoView()
        except RuntimeError as err:
            QMessageBox.critical(self, info.APP_NAME,
                                 _translate('MainWindow',
                                            'Unable to unmount the device:<br/><br/><i>%s</i>') % html.escape(err))
        except (TypeError, ValueError) as err:
            logging.error(err)
            QMessageBox.critical(self, info.APP_NAME, _translate('MainWindow', 'Internal error occurred.'))
