from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class CalOptionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("res/cal_option_window.ui", self)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    sw = CalOptionWidget()
    sw.show()
    exit(app.exec_())
