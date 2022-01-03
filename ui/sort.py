import pymysql
from db_env import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


class Sort:
    def __init__(self):
        self.query = {
            "select": "SELECT * FROM post_table ",
            "site": [],
            "condition": "",
            "word": "",
            "date": "",
            "order": "ORDER BY timeUpload ",
            "limit": "DESC LIMIT 24 ",
            "offset": "OFFSET 0",
        }
        self.pageIndex = 0
        self.curPage = 1

    # site, num, url, title, replyNum, viewNum, voteNum, timeUpload(게시물 작성 시간), timeUpdate(크롤링 시간), isChecked(bool) + len
    def selectSite(self, site=None):
        if site == "fm1":
            self.query["site"].append(' site = "FM" ')
        elif site == "global1":
            self.query["site"].append(' site = "GLOBAL" ')
        elif site == "real1":
            self.query["site"].append(' site = "REAL" ')
        elif site == "hit1":
            self.query["site"].append(' site = "HIT" ')
        elif site == "dog1":
            self.query["site"].append(' site = "DOG" ')
        elif site == "humor1":
            self.query["site"].append(' site = "HUMOR" ')

        elif site == "fm0":
            self.query["site"].remove(' site = "FM" ')
        elif site == "global0":
            self.query["site"].remove(' site = "GLOBAL" ')
        elif site == "real0":
            self.query["site"].remove(' site = "REAL" ')
        elif site == "hit0":
            self.query["site"].remove(' site = "HIT" ')
        elif site == "dog0":
            self.query["site"].remove(' site = "DOG" ')
        elif site == "humor0":
            self.query["site"].remove(' site = "HUMOR" ')

    def selectWord(self, word=None):
        self.query["word"] = ""
        word_len = len(word)
        if not word:
            return

        if word_len > 1:
            word = " ".join(["+" + s for s in word.split()])
            self.query["word"] = 'MATCH title AGAINST ("%s" IN BOOLEAN MODE) ' % word

        else:
            self.query["word"] = 'title LIKE "%%%s%%" ' % word

    def selectDate(self, start_date=None, end_date=None):
        self.query["date"] = ""
        if start_date and end_date:
            self.query["date"] = 'timeUpload BETWEEN "%s" AND "%s" ' % (
                start_date + " 00:00:00",
                end_date + " 23:59:59",
            )

    def selectCondition(self, expression=None):
        self.query["condition"] = expression + " "

    def selectOrder(self, order_mode="timeUpload", expression=None):
        if order_mode == "popular":
            order = "viewNum / 1000 + voteNum"
        elif order_mode == "custom":
            order = expression
        else:
            order = order_mode
        self.query["order"] = "ORDER BY (%s) " % order

    def selectPage(self, page=1):
        page = (page - 1) * 24 + self.pageIndex * 10 * 24
        self.query["offset"] = "OFFSET %d" % page

    def updateIsChecked(self, sites):
        f = open("./cache.txt", "a")
        for site in sites:
            f.write(site + "\n")
        f.close()

    def getData(self):
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                db=DB_NAME,
                charset="utf8",
            )
            cursor = conn.cursor()
            site_query = ""
            if self.query["site"]:
                site_query = "(" + "OR ".join(self.query["site"]) + ") "

            sort_query = ""
            sort_query_list = list(
                filter(
                    None,
                    [
                        site_query,
                        self.query["word"],
                        self.query["date"],
                        self.query["condition"],
                    ],
                )
            )
            if sort_query_list:
                sort_query = "WHERE " + "AND ".join(sort_query_list)

            sql = (
                self.query["select"]
                + sort_query
                + self.query["order"]
                + self.query["limit"]
                + self.query["offset"]
            )
            print(sql)
            cursor.execute(sql)
            return cursor.fetchall()

        except pymysql.err.InternalError as e:
            print(e)
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

        except Exception as e:
            print(e)
            return False


s = Sort()
