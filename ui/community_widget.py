from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class CommunityWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("res/community_buttons.ui", self)

        self.pressedFMStyleSheet = (
            "background-color: rgb(78, 120, 208);"
            + "color: white;"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
        )
        self.defaultFMStyleSheet = (
            "QPushButton { "
            + "background-color: rgb(89, 91, 94);"
            + "color: rgb(101,201,117);"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
            + "}"
            + "QPushButton:hover { "
            + "background-color: rgb(87, 137, 250);"
            + "color: white;"
            + "}"
        )

        self.pressedGlobalStyleSheet = (
            "background-color: rgb(59, 72, 144);"
            + "color: white;"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
        )
        self.defaultGlobalStyleSheet = (
            "QPushButton { "
            + "background-color: rgb(89, 91, 94);"
            + "color: rgb(101,201,117);"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
            + "}"
            + "QPushButton:hover { "
            + "background-color: rgb(64, 78, 156);"
            + "color: white;"
            + "}"
        )

        self.pressedRealStyleSheet = (
            "background-color: rgb(219, 81, 84);"
            + "color: white;"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
        )
        self.defaultRealStyleSheet = (
            "QPushButton { "
            + "background-color: rgb(89, 91, 94);"
            + "color: rgb(101,201,117);"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
            + "}"
            + "QPushButton:hover { "
            + "background-color: rgb(255, 97, 100);"
            + "color: white;"
            + "}"
        )

        self.pressedHitStyleSheet = (
            "background-color: rgb(181, 0, 0);"
            + "color: white;"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
        )
        self.defaultHitStyleSheet = (
            "QPushButton { "
            + "background-color: rgb(89, 91, 94);"
            + "color: rgb(101,201,117);"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
            + "}"
            + "QPushButton:hover { "
            + "background-color: rgb(224, 0, 0);"
            + "color: white;"
            + "}"
        )

        self.pressedDogStyleSheet = (
            "background-color: rgb(46, 67, 97);"
            + "color: white;"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
        )
        self.defaultDogStyleSheet = (
            "QPushButton { "
            + "background-color: rgb(89, 91, 94);"
            + "color: rgb(101,201,117);"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
            + "}"
            + "QPushButton:hover { "
            + "background-color: rgb(60, 87, 125);"
            + "color: white;"
            + "}"
        )

        self.pressedHumorStyleSheet = (
            "background-color: rgb(236, 24, 68);"
            + "color: white;"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
        )
        self.defaultHumorStyleSheet = (
            "QPushButton { "
            + "background-color: rgb(89, 91, 94);"
            + "color: rgb(101,201,117);"
            + "border-radius: 10px;"
            + 'font-family: -apple-system,BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;'
            + "font-size: 15px;"
            + "font-weight: bold;"
            + "}"
            + "QPushButton:hover { "
            + "background-color: rgb(252, 25, 72);"
            + "color: white;"
            + "}"
        )


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    sw = CommunityWidget()
    sw.show()
    exit(app.exec_())
