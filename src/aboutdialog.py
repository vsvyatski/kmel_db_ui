import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QWidget

import info
from ui_aboutdialog import Ui_AboutDialog


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
