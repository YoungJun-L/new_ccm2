from PyQt5 import uic
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QColor
from PyQt5.QtWidgets import (
    QWidget,
    QAbstractItemView,
    QHeaderView,
    QFrame,
    QStyle,
    QStyledItemDelegate,
)
from PyQt5.QtCore import Qt
from sort import s

sites = set()


class TableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("res/table_window.ui", self)
        self.model = QStandardItemModel()
        self.setItemModel()
        self.tableView.setModel(self.model)
        self.setupUI()

    def setupUI(self):
        self.header = self.tableView.horizontalHeader()
        self.tableView.verticalHeader().setVisible(False)
        self.header.setVisible(True)
        self.tableView.setColumnWidth(0, 55)
        self.tableView.setColumnWidth(1, 495)
        self.tableView.setColumnWidth(2, 180)
        self.tableView.setColumnWidth(3, 90)
        self.tableView.setColumnWidth(4, 90)
        self.tableView.setColumnWidth(5, 90)
        self.tableView.setColumnWidth(6, 0)
        self.tableView.setColumnWidth(7, 90)
        self.tableView.setColumnWidth(8, 90)

        self.header.setFixedHeight(30)
        self.header.setStretchLastSection(True)
        self.header.setSectionResizeMode(QHeaderView.Fixed)
        self.header.setSectionsClickable(True)
        self.header.setHighlightSections(True)

        self.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableView.setColumnHidden(6, True)

        self.tableView.setCurrentIndex(self.tableView.model().index(0, 0))

        self.tableView.setFrameShape(QFrame.NoFrame)

        self.tableView.setItemDelegate(NoFocusDelegate())

    def setItemModel(self):
        data = s.getData()
        sites.clear()

        if data is False:
            return False

        try:
            self.model = QStandardItemModel()
            self.model.setHorizontalHeaderLabels(
                ["", "제목", "시간", "조회수", "좋아요수", "댓글수", "url", "글자수", "사진수"]
            )

            urls = []
            f = open("./cache.txt", "r")
            for line in f.readlines():
                line = line.strip()
                urls.append(line)
            f.close()

            for i in range(24):
                items = [
                    setCommunityColor(data[i][0]),
                    QStandardItem(data[i][3]),
                    QStandardItem((data[i][7]).strftime("%Y-%m-%d %H:%M:%S")),
                    QStandardItem(str(data[i][5])),
                    QStandardItem(str(data[i][6])),
                    QStandardItem(str(data[i][4])),
                    QStandardItem(data[i][2]),
                    QStandardItem(str(data[i][8])),
                    QStandardItem(str(data[i][9])),
                ]

                items[1].setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                items[2].setTextAlignment(Qt.AlignCenter)
                for item in items[3:]:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                if data[i][2] in urls:
                    for item in items[1:]:
                        item.setForeground(QColor(37, 37, 38))

                self.model.appendRow(items)

            self.tableView.setModel(self.model)

            self.tableView.selectionModel().selectionChanged.connect(
                self.on_selectionChanged
            )
            self.tableView.clearFocus()
            self.tableView.selectRow(0)

            return True

        except IndexError:
            self.tableView.setModel(self.model)

            self.tableView.selectionModel().selectionChanged.connect(
                self.on_selectionChanged
            )
            self.tableView.clearFocus()
            self.tableView.selectRow(0)

            return True

    def nextSelectedRow(self):
        self.tableView.selectRow(self.tableView.currentIndex().row() + 1)

    def prevSelectedRow(self):
        self.tableView.selectRow(self.tableView.currentIndex().row() - 1)

    def on_selectionChanged(self, selection, deselection):
        try:
            for index in selection.indexes()[5::8]:
                select_item = self.model.itemFromIndex(index)
                select_site = select_item.text()
                sites.add(select_site)

            for index in deselection.indexes()[5::8]:
                deselect_item = self.model.itemFromIndex(index)
                deselect_site = deselect_item.text()
                sites.discard(deselect_site)

        except IndexError:
            pass


class NoFocusDelegate(QStyledItemDelegate):
    def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
        if QStyleOptionViewItem.state & QStyle.State_HasFocus:
            QStyleOptionViewItem.state = (
                QStyleOptionViewItem.state ^ QStyle.State_HasFocus
            )
        super().paint(QPainter, QStyleOptionViewItem, QModelIndex)


def setCommunityColor(name):
    item = QStandardItem("")
    item.setTextAlignment(Qt.AlignCenter)
    item.setData(QColor(255, 255, 255), Qt.ForegroundRole)

    if name == "FM":
        item.setText("펨코")
        item.setData(QColor(78, 120, 208), Qt.BackgroundRole)
    elif name == "GLOBAL":
        item.setText("싱벙")
        item.setData(QColor(59, 72, 144), Qt.BackgroundRole)
    elif name == "REAL":
        item.setText("실베")
        item.setData(QColor(219, 81, 84), Qt.BackgroundRole)
    elif name == "HIT":
        item.setText("힛갤")
        item.setData(QColor(181, 0, 0), Qt.BackgroundRole)
    elif name == "DOG":
        item.setText("개드립")
        item.setData(QColor(46, 67, 97), Qt.BackgroundRole)
    elif name == "HUMOR":
        item.setText("웃대")
        item.setData(QColor(236, 24, 68), Qt.BackgroundRole)

    item.setFlags(Qt.ItemIsSelectable)
    return item


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    tw = TableWidget()
    tw.show()
    exit(app.exec_())
