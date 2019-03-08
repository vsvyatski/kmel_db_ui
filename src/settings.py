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
from PyQt5.QtCore import QSettings, QByteArray, QObject

import info


class ApplicationSettings(QObject):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.__settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'Vladimir Svyatski', info.APP_NAME, self)

        self.__main_window_geometry: QByteArray = None
        self.__main_window_splitter_state: QByteArray = None

        self.__select_first_available_drive = False

        self.__show_toolbar = True
        self.__language: str = None

    def read(self):
        self.__settings.beginGroup('Geometry')
        self.__main_window_geometry = self.__settings.value('MainWindow', type=QByteArray)
        self.__main_window_splitter_state = self.__settings.value('SplitterState', type=QByteArray)
        self.__settings.endGroup()

        self.__settings.beginGroup('Drives')
        self.__select_first_available_drive = self.__settings.value('SelectFirst', defaultValue=False, type=bool)
        self.__settings.endGroup()

        self.__settings.beginGroup('Interface')
        self.__show_toolbar = self.__settings.value('ShowToolbar', defaultValue=True, type=bool)
        self.__language = self.__settings.value('Language')
        self.__settings.endGroup()

    def write(self):
        self.__settings.beginGroup('Geometry')
        self.__settings.setValue('MainWindow', self.__main_window_geometry)
        self.__settings.setValue('SplitterState', self.__main_window_splitter_state)
        self.__settings.endGroup()

        self.__settings.beginGroup('Drives')
        self.__settings.setValue('SelectFirst', self.__select_first_available_drive)
        self.__settings.endGroup()

        self.__settings.beginGroup('Interface')
        self.__settings.setValue('ShowToolbar', self.__show_toolbar)
        if self.__language is not None:
            self.__settings.setValue('Language', self.__language)
        else:
            self.__settings.remove('Language')
        self.__settings.endGroup()

        self.__settings.sync()

    @property
    def main_window_geometry(self) -> QByteArray:
        return self.__main_window_geometry

    @main_window_geometry.setter
    def main_window_geometry(self, value: QByteArray):
        self.__main_window_geometry = value

    @property
    def main_window_splitter_state(self) -> QByteArray:
        return self.__main_window_splitter_state

    @main_window_splitter_state.setter
    def main_window_splitter_state(self, value: QByteArray):
        self.__main_window_splitter_state = value

    @property
    def select_first_available_drive(self) -> bool:
        return self.__select_first_available_drive

    @select_first_available_drive.setter
    def select_first_available_drive(self, value: bool):
        self.__select_first_available_drive = value

    @property
    def show_toolbar(self) -> bool:
        return self.__show_toolbar

    @show_toolbar.setter
    def show_toolbar(self, value: bool):
        self.__show_toolbar = value

    @property
    def language(self) -> str:
        return self.__language

    @language.setter
    def language(self, value: str):
        self.__language = value
