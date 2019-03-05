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
import sys

import asyncqt
from PyQt5.QtWidgets import QApplication

import settings
from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = asyncqt.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Loading settings
    settings = settings.ApplicationSettings()
    settings.read()

    main_window = MainWindow()
    main_window.useSettingsObject(settings)
    main_window.show()

    with loop:
        status = loop.run_forever()

    # Saving settings
    settings.write()

    sys.exit(status)
