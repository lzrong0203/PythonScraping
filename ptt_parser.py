from bs4 import BeautifulSoup
import requests
import pandas as pd


class Ptt_parser:

    def __init__(self, board):
        self.url = "https://www.ptt.cc{}"
        self.board = board
        self.boardURL = self.url.format("/bbs/" + self.board)
        self.cookies = {"over18": "1"}
        r = requests.get(self.boardURL, cookies=self.cookies)
        self.soup = BeautifulSoup(r.content, "html.parser")

    def get_page_url(self):
        up_down_page = self.soup.find("div", {"class": Locator.PAGE_LOCATOR})
        a = up_down_page.find_all("a")[1]
        return self.url.format(a["href"])

    def paragraph_to_csv(self, mode="w"):
        title = []
        title_href = []
        for t in self.soup.select("div.title"):
            title.append(t.text.strip())

            a = t.select_one("a")
            if a is not None:
                title_href.append(a.get("href"))
        df = pd.DataFrame({"title": title, "href": title_href})

        df.to_csv("{}.csv".format(self.board), mode=mode, header=None)

    def get_next_page(self):
        next_page = self.get_page_url()
        next_page_response = requests.get(next_page, cookies=self.cookies)
        self.soup = BeautifulSoup(next_page_response.content, "html.parser")
        self.paragraph_to_csv("a")



class Locator:
    PAGE_LOCATOR = "btn-group btn-group-paging"


if __name__ == "__main__":
    ptt = Ptt_parser("Gossiping")
    ptt.paragraph_to_csv()
    ptt.get_next_page()
