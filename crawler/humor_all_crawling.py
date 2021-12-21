from bs4 import BeautifulSoup
from datetime import date, datetime, time
from pymysql import connect

from multiprocessing import Pool, Manager
import requests
import time as t
import random
import sys
import re
import logging
import logging.config
import logging.handlers
import warnings


class Crawling:
    def __init__(self):
        self.post_list = []
        self.url_list = []
        manager = Manager()
        self.len_imgCount_url_tuple_list = manager.list()

    def execute(self, page, cnt) -> None:
        self.get_post_list(page)
        self.insert_post_list()
        del self.post_list

        for _ in range(cnt // 5):
            pool = Pool(processes=5)
            tmp = []
            for _ in range(5):
                if self.url_list:
                    tmp.append(self.url_list.pop())
            pool.map(self.get_content, tmp)
            pool.close()
            pool.join()
        self.update_content()

    def connect_to_db(self) -> connect:
        conn = connect(
            host="db-community.chytu2uaulrn.ap-northeast-2.rds.amazonaws.com",
            user="leesoomok",
            password="!zx1421568400",
            db="crawler_data",
            charset="utf8",
        )
        return conn

    def get_post_list(self, page) -> None:
        base_url = "http://web.humoruniv.com/board/humor/list.html?table=pick&pg="
        try:
            reqUrl = requests.get(
                base_url + str(page),
                headers={
                    "Cache-Control": "no-cache",
                    "Cookie": "c_cpuid_uuid=92b-3282-9091; c_cpuid=H-1d01-aa12; c_uuid_global=92b-3282-9091; adfit_sdk_id=c43de104-4c2e-4c14-b922-f115eeaf2357; c_check=6dbe464628d539fdd666d275e88b6991; c_cpuid_set=wOLgwJC_w2DGTJrV7qjkYpRkZn4EwOCVvdwgTnDo; hu_auto_cook=Fzxo; bad_count_cook=0; link=ok; __utma=150955945.314112250.1602219537.1602300124.1602341084.6; __utmb=150955945.0.10.1602341084; __utmc=150955945; __utmz=150955945.1602341084.6.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); wcs_bt=395c7d0a9352ac:1602341285",
                    "Referer": "strict-origin-when-cross-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
                },
                verify=False,
            )

            soup = BeautifulSoup(
                reqUrl.content.decode("euc-kr", "replace"), "html.parser"
            )

            soup = soup.find("table", id="post_list")

            for i in soup.find_all("tr", id=re.compile("^li_chk_pds-")):

                url = (
                    "http://web.humoruniv.com/board/humor/" + i.find_all("a")[1]["href"]
                )

                replyNum = (
                    i.find("span", "list_comment_num")
                    .text.strip()
                    .replace("[", "")
                    .replace("]", "")
                    .replace(",", "")
                )

                title = i.find_all("a")[1]
                for tag in title.find_all("span"):
                    tag.replaceWith("")
                title = title.get_text().strip()

                timeString = i.find("span", "w_time").text.strip().split(":")

                timeValue = datetime.combine(
                    date.today(), time(int(timeString[0]), int(timeString[1]))
                )

                viewNum = i.find_all("td", "li_und")[0].text.strip().replace(",", "")

                voteNum = i.find_all("td", "li_und")[1].text.strip().replace(",", "")

                num = url[url.find("number=") :].replace("number=", "").strip()

                self.post_list.append(
                    (
                        num,
                        url,
                        title,
                        replyNum,
                        viewNum,
                        voteNum,
                        timeValue.strftime("%Y-%m-%d %H:%M:%S"),
                        url,
                        title,
                        replyNum,
                        viewNum,
                        voteNum,
                        timeValue.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                )
                self.url_list.append(url)

        except Exception as e:
            logging.error(f"Failed to crawl post_list: {str(e)}")

        finally:
            logging.debug(f"{len(self.post_list)} Posts Crawled")

    def get_content(self, url) -> None:
        t.sleep(random.randint(5, 6))
        try:
            reqUrl = requests.get(
                url,
                headers={
                    "Cache-Control": "no-cache",
                    "Cookie": "c_cpuid_uuid=92b-3282-9091; c_cpuid=H-1d01-aa12; c_uuid_global=92b-3282-9091; adfit_sdk_id=c43de104-4c2e-4c14-b922-f115eeaf2357; c_check=6dbe464628d539fdd666d275e88b6991; c_cpuid_set=wOLgwJC_w2DGTJrV7qjkYpRkZn4EwOCVvdwgTnDo; hu_auto_cook=Fzxo; bad_count_cook=0; link=ok; __utma=150955945.314112250.1602219537.1602300124.1602341084.6; __utmb=150955945.0.10.1602341084; __utmc=150955945; __utmz=150955945.1602341084.6.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); wcs_bt=395c7d0a9352ac:1602341285",
                    "Referer": "strict-origin-when-cross-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
                },
                verify=False,
            )

            soup = BeautifulSoup(
                reqUrl.content.decode("euc-kr", "replace"), "html.parser"
            )

            content_element = soup.find("div", id="cnts")

            thumb_elements = content_element.find_all("div", "comment_img_div")
            cover_element = content_element.find("div", id=re.compile("^racy_show_"))
            hidden_element = content_element.find("div", id=re.compile("^racy_hidden_"))

            if thumb_elements:
                for e in thumb_elements:
                    if len(e.find_all()) != 1:
                        e.decompose()
            if cover_element:
                cover_element.decompose()
            if hidden_element:
                hidden_element.decompose()

            content_text = content_element.text.strip()
            transTable = ["\xa0", " ", "\n", "\r", "\t"]
            for s in transTable:
                content_text = content_text.replace(s, "")

            content_img = content_element.find_all("img")

            self.len_imgCount_url_tuple_list.append(
                (len(content_text), len(content_img), url)
            )

        except Exception as e:
            logging.error(f"Failed to get content: {str(e)}")
            logging.error(f'Site: "HUMOR" Url: {url}')

    def insert_post_list(self) -> None:
        try:
            insert_post_list_sql = "INSERT INTO post_table (site, num, url, title, replyNum, viewNum, voteNum, timeUpload) VALUES ('HUMOR', %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE url = %s, title = %s, replyNum = %s, viewNum = %s, voteNum = %s, timeUpload = %s"
            conn = self.connect_to_db()
            cursor = conn.cursor()
            cursor.executemany(insert_post_list_sql, self.post_list)

        except Exception as e:
            logging.error(f"Failed to insert post_list: {str(e)}")

        finally:
            conn.commit()
            conn.close()
            logging.debug("Post_list Inserted")

    def update_content(self) -> None:
        try:
            update_content_sql = (
                "UPDATE post_table SET len = %s, imgCount = %s WHERE url = %s"
            )
            conn = self.connect_to_db()
            cursor = conn.cursor()
            cursor.executemany(update_content_sql, self.len_imgCount_url_tuple_list)

        except Exception as e:
            logging.error(f"Failed to update content: {str(e)}")

        finally:
            conn.commit()
            conn.close()
            logging.debug("Content Updated")


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    config = {
        "version": 1,
        "formatters": {
            "complex": {
                "format": "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "complex",
                "level": "DEBUG",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "humor_all_error.log",
                "formatter": "complex",
                "encoding": "utf-8",
                "level": "ERROR",
            },
        },
        "root": {"handlers": ["console", "file"], "level": "DEBUG"},
    }
    logging.config.dictConfig(config)
    root_logger = logging.getLogger()

    with open("humor_count.txt", "r") as file:
        data = file.read().splitlines()[-1]
        if data == "-1":
            logging.info("SOP")
            sys.exit(0)

    data = int(data) - 1
    c = Crawling()
    start = t.time()
    c.execute(page=data, cnt=20)
    end = t.time()
    logging.debug(f"{(end - start):.1f}s")
    with open("humor_count.txt", "w") as file:
        file.write(f"{data}")

# 2021-12-21: page 299 - 0
