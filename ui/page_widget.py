from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class PageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("res/page_window.ui", self)

        self.pressedPageStyleSheet = (
            "background-color: rgb(58, 59, 61);"
            + "color: white;"
            + "border-radius: 0px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 20px;"
            + "font-weight: bold;"
            + "text-align: center;"
        )
        self.defaultPageStyleSheet = (
            "QPushButton { "
            + "background-color: rgb(58, 59, 61);"
            + "color: rgb(119, 133, 133);"
            + "border-radius: 0px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 20px;"
            + "font-weight: bold;"
            + "}"
            + "QPushButton:hover { "
            + "color: white;"
            + "}"
        )


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    pw = PageWidget()
    pw.show()
    exit(app.exec_())
