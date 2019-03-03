from ui_aboutdialog import Ui_AboutDialog
from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
import sys
import info
import os


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        if sys.platform == 'darwin':
            window_flags = Qt.Sheet
        else:
            window_flags = Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint
        super().__init__(parent, window_flags)

        self.__ui = Ui_AboutDialog()
        self.__ui.setupUi(self)

        self.__ui.labelVersion.setText(self.__ui.labelVersion.text() + info.APP_VERSION)
        self.__loadLicense()

    def __loadLicense(self):
        with open(os.path.join(info.APP_DIR, 'LICENSE'), 'r') as f:
            license_text = f.read()

        if len(license_text) > 0:
            self.__ui.licenseTextEdit.appendPlainText(license_text)
        else:
            self.__ui.licenseTextEdit.appendPlainText('No license file found, perhaps the distribution is damaged.')
