from pprint import pprint
data = self.data


def fake_score_table(self):
    score_table_info = ""
    for i in self:
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
        final_info = replaced_text.replace("{{ single_detail }}", component_marks)
    clean_score_table = score_table_info.replace("\n", "")

    file = open("web_frame/fake_frame.txt", "rb")
    frame_info = file.read()
    decoded = frame_info.decode('utf-8')
    file.close()
    frame_info_replaced = decoded.replace("{{ score_table }}", clean_score_table)
    clean_frame_info = frame_info_replaced.replace("\n", "")
    fake_score = open("ebridge_website/fake_score.html", "wb")
    fake_score.write(clean_frame_info.encode("utf-8"))
    fake_score.close()


fake_score_table(data)
