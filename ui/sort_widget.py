from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget


class SortWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("res/sort_buttons.ui", self)

        self.custom_widget = CustomWidget()
        self.condition_widget = CustomWidget()
        self.sort_layout.addWidget(self.custom_widget)
        self.sort_layout.addWidget(self.condition_widget)
        self.custom_widget.hide()
        self.condition_widget.hide()

        self.sort_list = SortList()
        self.sort_show = 0
        self.sort_layout.addWidget(self.sort_list)
        self.sort_list.hide()

        self.sort_btn.clicked.connect(self.sortClicked)
        self.sort_list.sort_condition.clicked.connect(self.conditionClicked)
        self.sort_list.sort_custom.clicked.connect(self.customClicked)
        self.custom_mode = 1

        self.date_show = 0
        self.cal_option_widget.start_dateEdit.setDate(QDate.currentDate())
        self.cal_option_widget.end_dateEdit.setDate(QDate.currentDate())
        self.cal_option_widget.hide()

    def sortClicked(self):
        self.sort_btn.hide()
        self.sort_list.show()

    def conditionClicked(self):
        self.custom_mode = 0
        self.condition_widget.show()
        self.condition_widget.textEdit.setFocus()
        self.sort_btn.hide()
        self.sort_list.hide()

    def customClicked(self):
        self.custom_mode = 1
        self.custom_widget.show()
        self.custom_widget.textEdit.setFocus()
        self.sort_btn.hide()
        self.sort_list.hide()


class SortList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("res/sort_list.ui", self)


class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("res/custom_window.ui", self)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    sw = SortWidget()
    sw.show()
    exit(app.exec_())
