from PyQt5 import uic
from PyQt5.QtCore import QDate, QEvent, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QIcon

from res import images_rc

from sort_widget import SortWidget
from table_widget import TableWidget, sites
from search_widget import SearchWidget
from community_widget import CommunityWidget
from page_widget import PageWidget
from sort import s

from os import environ
import sys

import webbrowser
import platform


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
if platform.system() == "Darwin":
    browser = webbrowser.get(using="safari")
else:
    browser = webbrowser.get(chrome_path)

form_class = uic.loadUiType("res/main_window.ui")[0]


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.tableWidget = TableWidget(self.table_widget)
        self.sortWidget = SortWidget(self.sort_widget)
        self.searchWidget = SearchWidget(self.search_widget)
        self.communityWidget = CommunityWidget(self.community_widget)
        self.pageWidget = PageWidget(self.page_widget)

        self.installEventFilter(self)
        self.searchWidget.lineEdit.installEventFilter(self)
        self.searchWidget.logo_btn.clicked.connect(self.logoBtnSlot)

        self.sortWidget.custom_widget.textEdit.installEventFilter(self)
        self.sortWidget.sort_list.sort_latest.clicked.connect(self.latestSlot)
        self.sortWidget.sort_list.sort_like.clicked.connect(self.likeSlot)
        self.sortWidget.sort_list.sort_view.clicked.connect(self.viewSlot)
        self.sortWidget.sort_list.sort_popular.clicked.connect(self.popularSlot)
        self.sortWidget.condition_widget.custom_btn.clicked.connect(self.customSlot)
        self.sortWidget.custom_widget.custom_btn.clicked.connect(self.customSlot)
        self.sortWidget.date_btn.clicked.connect(self.dateSlot)
        self.sortWidget.default_btn.clicked.connect(self.defaultSlot)

        self.communityWidget.fm_btn.clicked.connect(self.fmBtnSlot)
        self.communityWidget.global_btn.clicked.connect(self.globalBtnSlot)
        self.communityWidget.real_btn.clicked.connect(self.realBtnSlot)
        self.communityWidget.hit_btn.clicked.connect(self.hitBtnSlot)
        self.communityWidget.dog_btn.clicked.connect(self.dogBtnSlot)
        self.communityWidget.humor_btn.clicked.connect(self.humorBtnSlot)

        self.pageWidget.page1_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page1_btn.setEnabled(False)
        self.pageWidget.prev_btn.setEnabled(False)
        self.pageWidget.first_btn.setEnabled(False)

        self.pageWidget.page1_btn.toggled.connect(self.page1BtnSlot)
        self.pageWidget.page2_btn.toggled.connect(self.page2BtnSlot)
        self.pageWidget.page3_btn.toggled.connect(self.page3BtnSlot)
        self.pageWidget.page4_btn.toggled.connect(self.page4BtnSlot)
        self.pageWidget.page5_btn.toggled.connect(self.page5BtnSlot)
        self.pageWidget.page6_btn.toggled.connect(self.page6BtnSlot)
        self.pageWidget.page7_btn.toggled.connect(self.page7BtnSlot)
        self.pageWidget.page8_btn.toggled.connect(self.page8BtnSlot)
        self.pageWidget.page9_btn.toggled.connect(self.page9BtnSlot)
        self.pageWidget.page10_btn.toggled.connect(self.page10BtnSlot)
        self.pageWidget.next_btn.toggled.connect(self.nextBtnSlot)
        self.pageWidget.prev_btn.toggled.connect(self.prevBtnSlot)
        self.pageWidget.first_btn.toggled.connect(self.firstBtnSlot)

        self.tableWidget.tableView.installEventFilter(self)
        self.tableWidget.header.sectionClicked.connect(self.headerSlot)
        self.tableWidget.tableView.clicked.connect(self.clickedSlot)
        self.tableWidget.tableView.doubleClicked.connect(self.connectSiteSlot)

    def initUI(self):
        self.setWindowIcon(QIcon("res/icon.png"))
        self.setupUi(self)

    def show(self):
        super().showMaximized()

    def eventFilter(self, obj, event):
        if obj == self.searchWidget.lineEdit and event.type() == QEvent.FocusIn:
            self.searchWidget.search_btn.hide()
            self.searchWidget.search_label.show()
            self.searchWidget.search_gif.start()

        elif obj == self.searchWidget.lineEdit and event.type() == QEvent.FocusOut:
            self.searchWidget.search_btn.show()
            self.searchWidget.search_label.hide()
            self.searchWidget.search_gif.stop()

        elif event.type() == QEvent.KeyPress and event.key() in (
            Qt.Key_Enter,
            Qt.Key_Return,
        ):
            if obj == self.searchWidget.lineEdit:
                obj.clearFocus()
                s.selectWord(self.searchWidget.lineEdit.text())
                self.firstBtnSlot()

            elif obj == self.sortWidget.custom_widget.textEdit:
                obj.clearFocus()
                self.customSlot()

            else:
                self.connectSite()
            return True

        elif (
            obj != self.sortWidget.custom_widget.textEdit
            and obj != self.searchWidget.lineEdit
        ):
            if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Left:
                self.moveToPrevPage()
                return True

            elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Right:
                self.moveToNextPage()
                return True

            elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Up:
                self.tableWidget.prevSelectedRow()
                return True

            elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Down:
                self.tableWidget.nextSelectedRow()
                return True

            elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
                self.searchWidget.lineEdit.setFocus()
                return True

        return super().eventFilter(obj, event)

    def logoBtnSlot(self, state):
        if state:
            browser.open_new_tab("https://killingtime.co.kr/")

    def clickedSlot(self, idx):
        self.tableWidget.tableView.selectRow(idx.row())
        self.tableWidget.tableView.selectRow(idx.row())

    def headerSlot(self, idx):
        if idx == 2:
            self.latestSlot()
        elif idx == 3:
            self.viewSlot()
        elif idx == 4:
            self.likeSlot()
        elif idx == 5:
            self.replySlot()
        elif idx == 7:
            self.lenSlot()
        elif idx == 8:
            self.imgSlot()

    def connectSite(self):
        for site in sites:
            browser.open_new_tab(site)
        s.updateIsChecked(sites)
        self.tableWidget.setItemModel()

    def connectSiteSlot(self, idx):
        self.tableWidget.tableView.selectRow(idx.row())
        self.connectSite()

    def latestSlot(self):
        self.sortWidget.sort_btn.setText("최신순")
        self.sortWidget.sort_btn.show()
        self.sortWidget.sort_list.hide()
        s.selectOrder("timeUpload")
        self.firstBtnSlot()

    def likeSlot(self):
        self.sortWidget.sort_btn.setText("좋아요순")
        self.sortWidget.sort_btn.show()
        self.sortWidget.sort_list.hide()
        s.selectOrder("voteNum")
        self.firstBtnSlot()

    def viewSlot(self):
        self.sortWidget.sort_btn.setText("조회순")
        self.sortWidget.sort_btn.show()
        self.sortWidget.sort_list.hide()
        s.selectOrder("viewNum")
        self.firstBtnSlot()

    def replySlot(self):
        self.sortWidget.sort_btn.setText("댓글순")
        s.selectOrder("replyNum")
        self.firstBtnSlot()

    def lenSlot(self):
        self.sortWidget.sort_btn.setText("길이순")
        s.selectOrder("len")
        self.firstBtnSlot()

    def imgSlot(self):
        self.sortWidget.sort_btn.setText("사진순")
        s.selectOrder("imgCount")
        self.firstBtnSlot()

    def popularSlot(self):
        self.sortWidget.sort_btn.setText("인기순")
        self.sortWidget.sort_btn.show()
        self.sortWidget.sort_list.hide()
        s.selectOrder("popular")
        self.firstBtnSlot()

    def customSlot(self):
        def exp_translate(exp):
            exp = exp.replace("\n", "")
            exp = exp.replace(" ", "")
            exp = exp.replace("댓글수", "replyNum")
            exp = exp.replace("조회수", "viewNum")
            exp = exp.replace("좋아요수", "voteNum")
            exp = exp.replace("글자수", "len")
            exp = exp.replace("사진수", "imgCount")
            return exp

        if self.sortWidget.custom_mode:
            exp = self.sortWidget.custom_widget.textEdit.toPlainText()
            exp = exp_translate(exp)
            if "&" in exp or "<" in exp or ">" in exp or "=" in exp:
                exp = ""
            self.sortWidget.custom_widget.hide()
            self.sortWidget.sort_btn.setText("커스텀")
            s.selectOrder("custom", exp)
            self.sortWidget.custom_widget.textEdit.clearFocus()
        else:
            exp = self.sortWidget.condition_widget.textEdit.toPlainText()
            exp = exp_translate(exp)
            for e in exp.split("&&"):
                if "&" in e or "<" not in e and ">" not in e and "=" not in e:
                    exp = ""
                    break
            self.sortWidget.condition_widget.hide()
            self.sortWidget.sort_btn.setText("조건식")
            s.selectCondition(exp)
            self.sortWidget.condition_widget.textEdit.clearFocus()
        self.sortWidget.sort_btn.show()
        self.firstBtnSlot()

    def dateSlot(self):
        if not self.sortWidget.date_show:
            self.sortWidget.date_show = 1
            self.sortWidget.date_btn.setText("조회하기")
            self.sortWidget.date_btn.setMinimumWidth(100)
            self.sortWidget.date_btn.setMaximumWidth(100)
            self.sortWidget.cal_option_widget.show()
            self.sortWidget.default_btn.hide()
        elif self.sortWidget.date_show:
            self.sortWidget.date_show = 0

            start_date = self.sortWidget.cal_option_widget.start_dateEdit.date()
            end_date = self.sortWidget.cal_option_widget.end_dateEdit.date()
            if start_date <= end_date and end_date <= QDate.currentDate():
                self.sortWidget.date_btn.setText(
                    start_date.toString("yy-MM-dd")
                    + " ~ "
                    + end_date.toString("yy-MM-dd")
                )
                s.selectDate(
                    start_date.toString("yyyy-MM-dd"),
                    end_date.toString("yyyy-MM-dd"),
                )
                self.firstBtnSlot()
            else:
                self.sortWidget.date_btn.setText("날짜 입력 오류")

            self.sortWidget.default_btn.show()
            self.sortWidget.cal_option_widget.hide()
            self.sortWidget.date_btn.setMinimumWidth(170)
            self.sortWidget.date_btn.setMaximumWidth(170)

    def defaultSlot(self):
        self.sortWidget.cal_option_widget.start_dateEdit.setDate(QDate.currentDate())
        self.sortWidget.cal_option_widget.end_dateEdit.setDate(QDate.currentDate())
        self.sortWidget.cal_option_widget.hide()
        self.sortWidget.sort_btn.setText("최신순")
        self.sortWidget.sort_btn.show()
        self.sortWidget.sort_list.hide()
        self.sortWidget.date_show = 0
        self.sortWidget.date_btn.setText("기간 선택")
        self.sortWidget.date_btn.setMinimumWidth(100)
        self.sortWidget.date_btn.setMaximumWidth(100)
        self.sortWidget.condition_widget.hide()
        self.sortWidget.condition_widget.textEdit.clear()
        self.sortWidget.custom_widget.hide()
        self.sortWidget.custom_widget.textEdit.clear()
        self.searchWidget.lineEdit.clear()
        self.communityWidget.fm_btn.setStyleSheet(
            self.communityWidget.defaultFMStyleSheet
        )
        self.communityWidget.global_btn.setStyleSheet(
            self.communityWidget.defaultGlobalStyleSheet
        )
        self.communityWidget.real_btn.setStyleSheet(
            self.communityWidget.defaultRealStyleSheet
        )
        self.communityWidget.hit_btn.setStyleSheet(
            self.communityWidget.defaultHitStyleSheet
        )
        self.communityWidget.dog_btn.setStyleSheet(
            self.communityWidget.defaultDogStyleSheet
        )
        self.communityWidget.humor_btn.setStyleSheet(
            self.communityWidget.defaultHumorStyleSheet
        )
        s.query = {
            "select": "SELECT * FROM post_table ",
            "site": [],
            "condition": "",
            "word": "",
            "date": "",
            "order": "ORDER BY timeUpload ",
            "limit": "DESC LIMIT 24 ",
            "offset": "OFFSET 0",
        }
        s.pageIndex = 0
        s.curPage = 1
        self.firstBtnSlot()

    def fmBtnSlot(self, state):
        if state:
            self.communityWidget.fm_btn.setStyleSheet(
                self.communityWidget.pressedFMStyleSheet
            )
            s.selectSite("fm1")
            self.firstBtnSlot()
        else:
            self.communityWidget.fm_btn.setStyleSheet(
                self.communityWidget.defaultFMStyleSheet
            )
            s.selectSite("fm0")
            self.firstBtnSlot()

    def globalBtnSlot(self, state):
        if state:
            self.communityWidget.global_btn.setStyleSheet(
                self.communityWidget.pressedGlobalStyleSheet
            )
            s.selectSite("global1")
            self.firstBtnSlot()
        else:
            self.communityWidget.global_btn.setStyleSheet(
                self.communityWidget.defaultGlobalStyleSheet
            )
            s.selectSite("global0")
            self.firstBtnSlot()

    def realBtnSlot(self, state):
        if state:
            self.communityWidget.real_btn.setStyleSheet(
                self.communityWidget.pressedRealStyleSheet
            )
            s.selectSite("real1")
            self.firstBtnSlot()
        else:
            self.communityWidget.real_btn.setStyleSheet(
                self.communityWidget.defaultRealStyleSheet
            )
            s.selectSite("real0")
            self.firstBtnSlot()

    def hitBtnSlot(self, state):
        if state:
            self.communityWidget.hit_btn.setStyleSheet(
                self.communityWidget.pressedHitStyleSheet
            )
            s.selectSite("hit1")
            self.firstBtnSlot()
        else:
            self.communityWidget.hit_btn.setStyleSheet(
                self.communityWidget.defaultHitStyleSheet
            )
            s.selectSite("hit0")
            self.firstBtnSlot()

    def dogBtnSlot(self, state):
        if state:
            self.communityWidget.dog_btn.setStyleSheet(
                self.communityWidget.pressedDogStyleSheet
            )
            s.selectSite("dog1")
            self.firstBtnSlot()
        else:
            self.communityWidget.dog_btn.setStyleSheet(
                self.communityWidget.defaultDogStyleSheet
            )
            s.selectSite("dog0")
            self.firstBtnSlot()

    def humorBtnSlot(self, state):
        if state:
            self.communityWidget.humor_btn.setStyleSheet(
                self.communityWidget.pressedHumorStyleSheet
            )
            s.selectSite("humor1")
            self.firstBtnSlot()
        else:
            self.communityWidget.humor_btn.setStyleSheet(
                self.communityWidget.defaultHumorStyleSheet
            )
            s.selectSite("humor0")
            self.firstBtnSlot()

    def page1BtnSlot(self):
        s.curPage = 1
        self.pageBtnSetEnabled()
        self.pageWidget.page1_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page1_btn.setEnabled(False)
        s.selectPage(s.curPage)
        if not self.tableWidget.setItemModel():
            if self.sortWidget.custom_mode:
                s.query["order"] = "ORDER BY timeUpload "
                self.messageEvent("커스텀 오류! 커스텀 수식이 초기화되었습니다")
            else:
                s.query["condition"] = ""
                self.messageEvent("조건식 오류! 조건식이 초기화되었습니다")
            self.tableWidget.setItemModel()

    def page2BtnSlot(self):
        s.curPage = 2
        self.pageBtnSetEnabled()
        self.pageWidget.page2_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page2_btn.setEnabled(False)
        s.selectPage(s.curPage)
        self.tableWidget.setItemModel()

    def page3BtnSlot(self):
        s.curPage = 3
        self.pageBtnSetEnabled()
        self.pageWidget.page3_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page3_btn.setEnabled(False)
        s.selectPage(s.curPage)
        self.tableWidget.setItemModel()

    def page4BtnSlot(self):
        s.curPage = 4
        self.pageBtnSetEnabled()
        self.pageWidget.page4_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page4_btn.setEnabled(False)
        s.selectPage(s.curPage)
        self.tableWidget.setItemModel()

    def page5BtnSlot(self):
        s.curPage = 5
        self.pageBtnSetEnabled()
        self.pageWidget.page5_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page5_btn.setEnabled(False)
        s.selectPage(s.curPage)
        self.tableWidget.setItemModel()

    def page6BtnSlot(self):
        s.curPage = 6
        self.pageBtnSetEnabled()
        self.pageWidget.page6_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page6_btn.setEnabled(False)
        s.selectPage(s.curPage)
        self.tableWidget.setItemModel()

    def page7BtnSlot(self):
        s.curPage = 7
        self.pageBtnSetEnabled()
        self.pageWidget.page7_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page7_btn.setEnabled(False)
        s.selectPage(s.curPage)
        self.tableWidget.setItemModel()

    def page8BtnSlot(self):
        s.curPage = 8
        self.pageBtnSetEnabled()
        self.pageWidget.page8_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page8_btn.setEnabled(False)
        s.selectPage(s.curPage)
        self.tableWidget.setItemModel()

    def page9BtnSlot(self):
        s.curPage = 9
        self.pageBtnSetEnabled()
        self.pageWidget.page9_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page9_btn.setEnabled(False)
        s.selectPage(s.curPage)
        self.tableWidget.setItemModel()

    def page10BtnSlot(self):
        s.curPage = 10
        self.pageBtnSetEnabled()
        self.pageWidget.page10_btn.setStyleSheet(self.pageWidget.pressedPageStyleSheet)
        self.pageWidget.page10_btn.setEnabled(False)
        s.selectPage(s.curPage)
        self.tableWidget.setItemModel()

    def nextBtnSlot(self):
        s.pageIndex += 1
        if s.pageIndex == 1:
            self.pageWidget.prev_btn.setEnabled(True)
            self.pageWidget.first_btn.setEnabled(True)
        self.changePageIndex()
        self.page1BtnSlot()

    def prevBtnSlot(self):
        s.pageIndex -= 1
        if not s.pageIndex:
            self.pageWidget.prev_btn.setEnabled(False)
            self.pageWidget.first_btn.setEnabled(False)
        self.changePageIndex()
        self.page1BtnSlot()

    def moveToNextPage(self):
        if s.curPage == 1:
            self.page2BtnSlot()
        elif s.curPage == 2:
            self.page3BtnSlot()
        elif s.curPage == 3:
            self.page4BtnSlot()
        elif s.curPage == 4:
            self.page5BtnSlot()
        elif s.curPage == 5:
            self.page6BtnSlot()
        elif s.curPage == 6:
            self.page7BtnSlot()
        elif s.curPage == 7:
            self.page8BtnSlot()
        elif s.curPage == 8:
            self.page9BtnSlot()
        elif s.curPage == 9:
            self.page10BtnSlot()
        elif s.curPage == 10:
            self.nextBtnSlot()

    def moveToPrevPage(self):
        if s.curPage == 1 and s.pageIndex:
            s.pageIndex -= 1
            if not s.pageIndex:
                self.pageWidget.prev_btn.setEnabled(False)
                self.pageWidget.first_btn.setEnabled(False)
            self.changePageIndex()
            self.page10BtnSlot()
        elif s.curPage == 2:
            self.page1BtnSlot()
        elif s.curPage == 3:
            self.page2BtnSlot()
        elif s.curPage == 4:
            self.page3BtnSlot()
        elif s.curPage == 5:
            self.page4BtnSlot()
        elif s.curPage == 6:
            self.page5BtnSlot()
        elif s.curPage == 7:
            self.page6BtnSlot()
        elif s.curPage == 8:
            self.page7BtnSlot()
        elif s.curPage == 9:
            self.page8BtnSlot()
        elif s.curPage == 10:
            self.page9BtnSlot()

    def firstBtnSlot(self):
        s.pageIndex = 1
        self.prevBtnSlot()

    def changePageIndex(self):
        self.pageWidget.page1_btn.setText(str(s.pageIndex * 10 + 1))
        self.pageWidget.page2_btn.setText(str(s.pageIndex * 10 + 2))
        self.pageWidget.page3_btn.setText(str(s.pageIndex * 10 + 3))
        self.pageWidget.page4_btn.setText(str(s.pageIndex * 10 + 4))
        self.pageWidget.page5_btn.setText(str(s.pageIndex * 10 + 5))
        self.pageWidget.page6_btn.setText(str(s.pageIndex * 10 + 6))
        self.pageWidget.page7_btn.setText(str(s.pageIndex * 10 + 7))
        self.pageWidget.page8_btn.setText(str(s.pageIndex * 10 + 8))
        self.pageWidget.page9_btn.setText(str(s.pageIndex * 10 + 9))
        self.pageWidget.page10_btn.setText(str(s.pageIndex * 10 + 10))

    def pageBtnSetEnabled(self):
        self.pageWidget.page1_btn.setEnabled(True)
        self.pageWidget.page2_btn.setEnabled(True)
        self.pageWidget.page3_btn.setEnabled(True)
        self.pageWidget.page4_btn.setEnabled(True)
        self.pageWidget.page5_btn.setEnabled(True)
        self.pageWidget.page6_btn.setEnabled(True)
        self.pageWidget.page7_btn.setEnabled(True)
        self.pageWidget.page8_btn.setEnabled(True)
        self.pageWidget.page9_btn.setEnabled(True)
        self.pageWidget.page10_btn.setEnabled(True)

        self.pageWidget.page1_btn.setStyleSheet(self.pageWidget.defaultPageStyleSheet)
        self.pageWidget.page2_btn.setStyleSheet(self.pageWidget.defaultPageStyleSheet)
        self.pageWidget.page3_btn.setStyleSheet(self.pageWidget.defaultPageStyleSheet)
        self.pageWidget.page4_btn.setStyleSheet(self.pageWidget.defaultPageStyleSheet)
        self.pageWidget.page5_btn.setStyleSheet(self.pageWidget.defaultPageStyleSheet)
        self.pageWidget.page6_btn.setStyleSheet(self.pageWidget.defaultPageStyleSheet)
        self.pageWidget.page7_btn.setStyleSheet(self.pageWidget.defaultPageStyleSheet)
        self.pageWidget.page8_btn.setStyleSheet(self.pageWidget.defaultPageStyleSheet)
        self.pageWidget.page9_btn.setStyleSheet(self.pageWidget.defaultPageStyleSheet)
        self.pageWidget.page10_btn.setStyleSheet(self.pageWidget.defaultPageStyleSheet)

    def messageEvent(self, text):
        QMessageBox.information(self, "Message", text)


if __name__ == "__main__":
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
