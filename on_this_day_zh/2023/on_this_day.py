import requests
import re
import datetime
from bs4 import BeautifulSoup

months = list(map(lambda x: str(x) + "月", range(1, 13)))


for index in range(12):

    month = months[index]
    day = 1

    if index != 6:
        url = "https://web.archive.org/web/20230823144757/https://zh.wikipedia.org/zh-cn/Wikipedia:%E5%8E%86%E5%8F%B2%E4%B8%8A%E7%9A%84%E4%BB%8A%E5%A4%A9/" + month
    else: 
        url = "https://web.archive.org/web/20230823144757/https://zh.wikipedia.org/wiki/Wikipedia:%E5%8E%86%E5%8F%B2%E4%B8%8A%E7%9A%84%E4%BB%8A%E5%A4%A9/" + month
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    div_elements = soup.find_all("div", class_="selected-anniversary")

    for div_element in div_elements:

        datetime_time = datetime.datetime(2000, index+1, day)
        formatted_time_yearless = datetime_time.strftime("%m-%d")

        p_element = div_element.find("p")
        dl_element = div_element.find("dl")
        event_elements = dl_element.find_all("div", class_="event")
        ul_element = soup.new_tag("ul")

        for event in event_elements:
            li_element = soup.new_tag("li")
            li_element.append(event)
            ul_element.append(li_element)

        result = (
            str(p_element)
            .replace("/wiki", "https://zh.wikipedia.org/zh-cn")
            .replace('<span class="otd-year">', "<b>")
            .replace("</span>：", "：</b>")
            + str(ul_element)
            .replace("/wiki", "https://zh.wikipedia.org/zh-cn")
            .replace("</dt><dd>", " – ")
            .replace('<div class="event">\n<dt>', "")
            .replace("</dd>\n</div>", "")
        )
        result = re.sub(r"<small>.*?图.*?</small>", "", result)

        with open(formatted_time_yearless + ".html", "w") as file:
            file.write(result)
            file.close()
            day += 1
