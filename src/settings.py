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

    def read(self):
        self.__settings.beginGroup('Geometry')
        self.__main_window_geometry = self.__settings.value('MainWindow', type=QByteArray)
        self.__main_window_splitter_state = self.__settings.value('SplitterState', type=QByteArray)
        self.__settings.endGroup()

    def write(self):
        self.__settings.beginGroup('Geometry')
        self.__settings.setValue('MainWindow', self.__main_window_geometry)
        self.__settings.setValue('SplitterState', self.__main_window_splitter_state)
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
