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
