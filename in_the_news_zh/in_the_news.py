import requests
import re
import copy
import datetime
from bs4 import BeautifulSoup


url = "https://zh.m.wikipedia.org/zh-cn/Wikipedia:%E9%A6%96%E9%A1%B5"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

div_element = soup.find("div", id="column-itn")
ul_element = div_element.find("ul")
ul_element_2 = ul_element.find_next("ul")
ul_element_3 = ul_element_2.find_next("ul")
span_element_2 = ul_element_2.find("span", class_="hlist inline")
span_element_3 = ul_element_3.find("span", class_="hlist inline")
p_element_2 = soup.new_tag("p")
p_element_3 = soup.new_tag("p")
p_element_2.append(span_element_2)
p_element_3.append(span_element_3)

result = (
    str(ul_element).replace("/wiki", "https://zh.wikipedia.org/zh-cn") + str(p_element_2)
    .replace('<span class="hlist inline">', "<b>正在发生：</b>")
    .replace("</span>", "")
    .replace("－", "；")
    .replace('（<a href="/wiki/%E4%BF%84%E7%BE%85%E6%96%AF%E5%85%A5%E4%BE%B5%E7%83%8F%E5%85%8B%E8%98%AD%E6%99%82%E9%96%93%E8%BB%B8" title="俄罗斯入侵乌克兰时间轴">时间轴</a>）', "")
    .replace("/wiki", "https://zh.wikipedia.org/zh-cn")
    + str(p_element_3)
    .replace('<span class="hlist inline">', "<b>最近逝世：</b>")
    .replace("</span>", "")
    .replace("－", "；")
    .replace("/wiki", "https://zh.wikipedia.org/zh-cn")
).replace("</p><p>", "<br>")
result = re.sub(r'<small.*?>.*?</small>', "", result)

with open("latest.html", 'r') as file:
    existing_content = file.read()

if existing_content != result:
    datetime_time = datetime.datetime.today() + datetime.timedelta(days=-1)
    formatted_time = datetime_time.strftime("%Y-%m-%d")
    new_filename = formatted_time + ".html"

    with open(new_filename, "w") as file:
        file.write(existing_content)
        file.close()

    with open("latest.html", "w") as file:
        file.write(result)
        file.close()
