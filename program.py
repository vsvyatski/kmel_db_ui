import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
import asyncqt
import asyncio

if __name__ == '__main__':
    a = QApplication(sys.argv)
    loop = asyncqt.QEventLoop(a)
    asyncio.set_event_loop(loop)

    w = MainWindow()
    w.show()

    with loop:
        sys.exit(loop.run_forever())
