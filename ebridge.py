# self.score_list ------ Your all info like this: {"Attempt":"..", "credit":"..", "detail_assessment":"..", ... " 'detail_assessment'": [{detailed_every_assessment}]
# self.name ---> name
# self.ID ---> ID card
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re


class Ebridge:
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36",
            "Connection": "keep-alive",
            "Host": "ebridge.xjtlu.edu.cn",
            "Referer": "https://ebridge.xjtlu.edu.cn/",
            "Upgrade-Insecure-Requests": "1"}
        self.data = {"MUA_CODE.DUMMY.MENSYS.1": account, "PASSWORD.DUMMY.MENSYS.1": password,
                     "SCREEN_WIDTH.DUMMY.MENSYS.1": "1198", "SCREEN_HEIGHT.DUMMY.MENSYS.1": "1216",
                     "%.DUMMY.MENSYS.1": "",
                     "PARS.DUMMY.MENSYS.1": "", "BP101.DUMMY_B.MENSYS.1": "Log in"}
        self.xjtlu = "https://ebridge.xjtlu.edu.cn/urd/sits.urd/run/"
        self.session = requests.session()
        self.get_directed()
        self.get_score_info()

    def get_directed(self):
        self.session = requests.session()
        preserved_wb = self.session.get("https://ebridge.xjtlu.edu.cn/urd/sits.urd/run/siw_lgn", headers=self.headers)
        self.data["RUNTIME.DUMMY.MENSYS.1"] = self.get_runtime(preserved_wb)
        score_url = self.get_score_page()

        # request and save the the score table, which is in score page
        score_wb = self.session.get(score_url)
        score_wb_soup = BeautifulSoup(score_wb.text, "lxml")
        score_wb_url = [i for i in score_wb_soup.find_all("a") if i.text == "Full Academic Records"][0].get(
            "href").replace("../run/", "")
        whole_score_url = self.xjtlu + score_wb_url
        self.score_page = whole_score_url

    # if post the home page, get the score page
    def get_score_page(self):
        home_page = self.session.get(self.get_post_data())
        home_page_data = BeautifulSoup(home_page.text, "lxml")
        score_url = self.xjtlu + home_page_data.find_all("a", {"title": "Academic Records"})[0].get("href")
        return score_url

    # util get the runtime data, post the data
    def get_post_data(self):
        session_whole_post = self.session.post("https://ebridge.xjtlu.edu.cn/urd/sits.urd/run/siw_lgn",
                                               headers=self.headers, data=self.data)
        soup = BeautifulSoup(session_whole_post.text, "lxml")  # have been successfully login!
        directed_url = soup.find_all("a")[1].get("href")
        whole_directed_url = self.xjtlu + directed_url
        return whole_directed_url

    # runtime is required message and changed with login html
    def get_runtime(self, wb_data):
        soup = BeautifulSoup(wb_data.text, "lxml")
        run_time = soup.find_all("input", {"name": "RUNTIME.DUMMY.MENSYS.1"})[0].get("value")
        return run_time

    def get_score_info(self):
        wb_data = self.session.get(self.score_page)
        soup = BeautifulSoup(wb_data.text, "lxml")
        ID = soup.select("div.sv-panel-body > div > div > div > div:nth-of-type(2) > b")[0].text
        name = soup.select("div.sv-panel-body > div > div > div > div:nth-of-type(4)")[0].text.replace("&nbsp", "")
        self.ID = ID
        self.name = name

        self.score_list = []
        detail_score = soup.find_all("table", {"class": "sitstablegrid"})
        # start prasing_general_info, start with 1, 0 is none because it is the title
        tr = soup.select("table > tr")[1:len(detail_score) + 1]
        counter = 0
        for i in tr:
            single_course_info = {}
            # print out the tr
            all_info = i.find_all("td")[0:7]

            single_course_info["period"] = all_info[0].text
            single_course_info["module_code"] = all_info[1].text
            single_course_info["module_title"] = all_info[2].text
            single_course_info["credit"] = all_info[3].text
            mark = re.search("\d+", all_info[4].text)
            single_course_info["mark"] = mark.group()
            single_course_info["grades"] = all_info[5].text
            single_course_info["Attempt"] = all_info[6].text

            # start detailed score
            module_detail_score_list = []
            ass_raw_list = detail_score[counter]
            ass_items = ass_raw_list.find_all("tr")[1:]
            # pprint(ass_items)
            for i in ass_items:
                detail_line = {}
                ass_raw_info = i.find_all("td")
                detail_line["component_title"] = ass_raw_info[0].text
                detail_line["assessment_type"] = ass_raw_info[1].text
                weight = re.search("\d+", ass_raw_info[2].text)
                detail_line["weight"] = weight.group()
                mark = re.search("\d+", ass_raw_info[3].text)
                detail_line["mark"] = mark.group()
                module_detail_score_list.append(detail_line)
            single_course_info["detail_assessment"] = module_detail_score_list
            counter += 1
            self.score_list.append(single_course_info)

    def average(self):
        total_credit = 0
        total_score = 0
        for i in self.score_list:
            mark = float(i["mark"])
            credit = float(i["credit"])
            single_mark = mark * credit
            total_credit += credit
            total_score += single_mark

        return total_score / total_credit


if __name__ == "__main__":
    name = input("Input Your EBridge account: ")
    password = input("Input Your EBridge password: ")
    test = Ebridge(name, password)
    print(test.average())
