# self.__score_list ------ Your all info like this: {"Attempt":"..", "credit":"..", "detail_assessment":"..", ... " 'detail_assessment'": [{detailed_every_assessment}]
# self.__name ---> name
# self.__ID ---> ID card
from bs4 import BeautifulSoup
import requests
import re


class Ebridge():
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36",
            "Connection": "keep-alive",
            "Host": "ebridge.xjtlu.edu.cn",
            "Referer": "https://ebridge.xjtlu.edu.cn/",
            "Upgrade-Insecure-Requests": "1"}
        self.__data = {"MUA_CODE.DUMMY.MENSYS.1": account, "PASSWORD.DUMMY.MENSYS.1": password,
                       "SCREEN_WIDTH.DUMMY.MENSYS.1": "1198", "SCREEN_HEIGHT.DUMMY.MENSYS.1": "1216",
                       "%.DUMMY.MENSYS.1": "",
                       "PARS.DUMMY.MENSYS.1": "", "BP101.DUMMY_B.MENSYS.1": "Log in"}
        self.__xjtlu = "https://ebridge.xjtlu.edu.cn/urd/sits.urd/run/"
        self.__session = requests.session()
        self.__get_directed()
        self.__get_score_info()

        self.purple = "\033[1;35;m"
        self.red = "\033[1;31;m"
        self.white = "\033[0m"
        self.blue = "\033[1;36;m"

    def __get_directed(self):
        self.__session = requests.session()
        preserved_wb = self.__session.get("https://ebridge.xjtlu.edu.cn/urd/sits.urd/run/siw_lgn",
                                          headers=self.__headers)
        self.__data["RUNTIME.DUMMY.MENSYS.1"] = self.__get_runtime(preserved_wb)
        score_url = self.__get_score_page()

        # request and save the the score table, which is in score page
        score_wb = self.__session.get(score_url)
        score_wb_soup = BeautifulSoup(score_wb.text, "lxml")
        score_wb_url = [i for i in score_wb_soup.find_all("a") if i.text == "Full Academic Records"][0].get(
            "href").replace("../run/", "")
        whole_score_url = self.__xjtlu + score_wb_url
        self.__score_page = whole_score_url

    # if post the home page, get the score page
    def __get_score_page(self):
        home_page = self.__session.get(self.__get_post_data())
        home_page_data = BeautifulSoup(home_page.text, "lxml")
        score_url = self.__xjtlu + home_page_data.find_all("a", {"title": "Academic Records"})[0].get("href")
        return score_url

    # util get the runtime data, post the data
    def __get_post_data(self):
        session_whole_post = self.__session.post("https://ebridge.xjtlu.edu.cn/urd/sits.urd/run/siw_lgn",
                                                 headers=self.__headers, data=self.__data)
        soup = BeautifulSoup(session_whole_post.text, "lxml")  # have been successfully login!
        directed_url = soup.find_all("a")[1].get("href")
        whole_directed_url = self.__xjtlu + directed_url
        return whole_directed_url

    # runtime is required message and changed with login html
    def __get_runtime(self, wb_data):
        soup = BeautifulSoup(wb_data.text, "lxml")
        run_time = soup.find_all("input", {"name": "RUNTIME.DUMMY.MENSYS.1"})[0].get("value")
        return run_time

    def __get_score_info(self):
        wb_data = self.__session.get(self.__score_page)
        soup = BeautifulSoup(wb_data.text, "lxml")
        ID = soup.select("div.sv-panel-body > div > div > div > div:nth-of-type(2) > b")[0].text
        name = soup.select("div.sv-panel-body > div > div > div > div:nth-of-type(4)")[0].text.replace("&nbsp", " ")
        self.__ID = ID
        self.__name = name

        self.__score_list = []
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
            self.__score_list.append(single_course_info)

    @property
    def score_data(self):
        return self.__score_list

    @property
    def student_name(self):
        return self.__name

    @property
    def student_ID(self):
        return self.__ID


class Score(Ebridge):
    @property
    def average(self):
        total_credit = 0
        total_score = 0
        for i in self.score_data:
            mark = float(i["mark"])
            credit = float(i["credit"])
            single_mark = mark * credit
            total_credit += credit
            total_score += single_mark
        average = total_score / total_credit
        if (average > 70):
            return "Your score is " + self.purple + str(average) + " excellent :) "
        elif (average < 40):
            return "Your score is " + self.red + str(average) + " loser :( "
        else:
            return "Your score is " + self.white + str(average) + " normal : | "

    def analyse(self):
        self.fail_list = []
        for i in self.score_data:
            if i["grades"] != "P":
                self.fail_list.append(i)

        if self.fail_list:
            print(
                "Dear " + self.blue + self.student_name + self.red + ", Unfortunately during this semester you have failed these modules: " + self.white)
            print("ModuleCode              Description                                                     YourScore")
            print(
                "+-----------------------+----------------------------------------------------------------+----------+")
            for t in self.fail_list:
                print(t["module_code"] + "                  " + t["module_title"] + "                  " + t[
                    "mark"])
            print(
                "+-----------------------+----------------------------------------------------------------+----------+")
            addition = input("Do you want to View your detail score?(Y/N)")
            if addition == "Y":
                self.__detail_analyse()
            else:
                afraid = input("Are you afraid?(Y/N)")
                if afraid == "N":
                    print("Show you detail :) following:")
                    self.__detail_analyse()
                else:
                    print("Loser")
        else:
            print(
                "Dear " + self.blue + self.student_name + self.purple + " StudyAbility●MAX " + self.white + " NONE OF YOUR SCORE IS UNDER 40")

    # analyze the detail ass which fails
    def __detail_analyse(self):
        if self.fail_list:
            for i in self.fail_list:
                print(
                    "Dear " + self.blue + self.student_name + self.red + ", These modules you did really terrible: " + self.white)
                print(
                    "ModuleCode              Assessments/Coursework       Type                YourScore")
                print("+-----------------------+----------------------------+-----------------+----------+")
                for m in i["detail_assessment"]:
                    print(
                        i["module_code"] + "                   " + m["component_title"] + "                  " + m[
                            "component_title"] + "          " + self.red + m["mark"] + self.white)
                    print("+-----------------------+----------------------------------------------+----------+")


class FakeScore(Ebridge):
    def fake_score_table(self):
        score_table_info = ""
        for i in self.score_data:
            file1 = open("web_frame/score_table.txt")
            score_table = file1.read()
            file1.close()
            replaced_text = score_table.replace("{{ Period }}", i["period"]).replace("{{ Module Code }}",
                                                                                     i["module_code"]).replace(
                "{{ Credit }}", i["credit"]).replace("{{ Mark }}", "100").replace("{{ Grade }}", "P").replace(
                "{{ Module Title }}", i["module_title"]).replace("{{ Attempt }}", "1")
            component_marks = ""
            for single_info in i["detail_assessment"]:
                single_file = open("web_frame/single_detail.txt")
                single_detail = single_file.read()
                single_file.close()
                replaced_single_detail = single_detail.replace("{{ Component title }}",
                                                               single_info["component_title"]).replace(
                    "{{ Assessment type }}", single_info["assessment_type"]).replace("{{ Weight }}",
                                                                                     single_info["weight"]).replace(
                    "{{ Mark }}", "100")
                component_marks += replaced_single_detail
            final_info = replaced_text.replace("{{ single_detail }}", component_marks).replace("{{ Module_Code }}",
                                                                                               i["module_code"])
            score_table_info += final_info
        clean_score_table = score_table_info.replace("\n", "")

        file = open("web_frame/fake_frame.txt", "rb")
        frame_info = file.read()
        decoded = frame_info.decode('utf-8')
        file.close()
        frame_info_replaced = decoded.replace("{{ student.ID }}", self.student_ID).replace("{{ student.name }}",
                                                                                           self.student_name).replace(
            "{{ score_table }}", clean_score_table)
        clean_frame_info = frame_info_replaced.replace("\n", "")
        fake_score = open("ebridge_website/fake_score.html", "wb")
        fake_score.write(clean_frame_info.encode("utf-8"))
        fake_score.close()
        print(" Hey" + self.red + " Fake score has been produced! :)")


if __name__ == "__main__":
    name = input("Input Your ebridge account: ")
    password = input("Input Your ebridge password: ")
    fake_score = FakeScore(name, password)
    fake_score.fake_score_table()
