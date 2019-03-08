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
import sys

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QDialog, QWidget

from ui_preferencesdialog import Ui_PreferencesDialog

_translate = QCoreApplication.translate


# noinspection PyPep8Naming
class PreferencesDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        if sys.platform == 'darwin':
            window_flags = Qt.Sheet
        else:
            window_flags = Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint
        super().__init__(parent, window_flags)

        self.__ui = Ui_PreferencesDialog()
        self.__ui.setupUi(self)

        self.__loadLanguagesList()

    def __loadLanguagesList(self):
        self.__ui.comboBoxLanguage.addItem(_translate('PreferencesDialog', 'System default'))

        language_list = [('en', _translate('PreferencesDialog', 'English')),
                         ('ru', _translate('PreferencesDialog', 'Russian')),
                         ('es', _translate('PreferencesDialog', 'Spanish'))]
        language_list.sort(key=lambda item: item[1])
        for language_tuple in language_list:
            self.__ui.comboBoxLanguage.addItem(language_tuple[1], language_tuple[0])
