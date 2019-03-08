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
import os
import sys

import asyncqt
from PyQt5.QtCore import QLocale, QTranslator, QLibraryInfo
from PyQt5.QtWidgets import QApplication

import info
import settings
from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = asyncqt.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Loading settings
    settings = settings.ApplicationSettings()
    settings.read()

    locale = settings.language if settings.language is not None and len(
        settings.language) > 0 else QLocale.system().name()

    qt_translator = QTranslator()
    if qt_translator.load('qt_' + locale, QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
        app.installTranslator(qt_translator)

    my_app_translator = QTranslator()
    if my_app_translator.load('kenwood_db_gen_' + locale, os.path.join(info.APP_DIR, 'translations')):
        app.installTranslator(my_app_translator)

    main_window = MainWindow(settings)
    main_window.show()

    with loop:
        status = loop.run_forever()

    # Saving settings
    settings.write()

    sys.exit(status)
