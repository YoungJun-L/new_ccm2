from PyQt5 import uic
from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget


class SearchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("res/search_window.ui", self)

        self.search_label.hide()
        self.search_gif = QMovie("res/search_pressed.gif", QByteArray(), self)
        self.search_gif.setCacheMode(QMovie.CacheAll)
        self.search_label.setMovie(self.search_gif)

        self.pressedLogoStyleSheet = (
            "QPushButton {"
            + "background-image: url(res/logo_pressed.png);"
            + "background-repeat: no-repeat;"
            + "border: 0px;"
            + "}"
            + "QPushButton:hover {"
            + "background-image: url(res/logo_hover2.png);"
            + "background-repeat: no-repeat;"
            + "}"
        )

        self.defaultLogoStyleSheet = (
            "QPushButton {"
            + "background-image: url(res/logo_default.png);"
            + "background-repeat: no-repeat;"
            + "border: 0px;"
            + "}"
            + "QPushButton:hover {"
            + "background-image: url(res/logo_hover.png);"
            + "background-repeat: no-repeat;"
            + "}"
        )


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    sw = SearchWidget()
    sw.show()
    exit(app.exec_())
