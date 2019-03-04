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
