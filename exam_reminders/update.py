import os
import datetime
from bs4 import BeautifulSoup


datetime_time = datetime.date.today() + datetime.timedelta(days=1)
formatted_time = datetime_time.strftime("%Y-%m-%d")
yesterday_datetime_time = datetime.date.today()
yesterday_formatted_time = yesterday_datetime_time.strftime("%Y-%m-%d")

if not os.path.isfile(yesterday_formatted_time + ".html"): 
    quit()

with open(yesterday_formatted_time + ".html") as file: 
    soup = BeautifulSoup(file, "html.parser")

today_trs = soup.find_all("tr", class_="today")
for tr in today_trs: 
    next_tr = tr.find_next("tr")
    if next_tr:
        try:
            if next_tr["class"] == ["not-today"]: 
                next_tr["class"] = "today"
                next_tr = next_tr.find_next("tr")
                while next_tr:
                    if next_tr.find("th"): 
                        break
                    next_tr["class"] = "today"
                    next_tr = next_tr.find_next("tr")
                tr.decompose()
            elif next_tr["class"] == ["today"]: 
                tr.decompose()
            else: 
                tr.parent.parent.decompose()
        except KeyError:
            tr.parent.parent.decompose()
    else: 
        tr.parent.parent.decompose()

with open(formatted_time + ".html", "w") as file: 
    file.write(str(soup))
