import sys
from PyQt5.QtWidgets import (QApplication)
from windows.base_window import BaseWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        sys.excepthook = except_hook
        base_window = BaseWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
