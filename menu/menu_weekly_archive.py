import re
import string
import PyPDF2 as pdf
import datetime


def split_string_en(string):
    pattern = r"[\u3000-\u303f\u4e00-\u9fff]+"
    en_substrings = filter(None, re.split(pattern, string))
    return list(en_substrings)


def split_string_zh(string):
    pattern = r"[^\u3000-\u303f\u4e00-\u9fff /&]+"
    zh_substrings = filter(None, re.split(pattern, string))
    return list(zh_substrings)


def split_list(lst, method):
    length = len(lst)
    if type(method) == type(1):
        method_cleaned = [method] * (length // method)
        if length % method:
            method_cleaned.append(length % method)
    else:
        method_cleaned = []
        method_sum = 0
        for i in method:
            if method_sum + i < length:
                method_cleaned.append(i)
                method_sum += i
            else:
                method_cleaned.append(length - method_sum)
                method_sum = length
                break
        if method_sum < length:
            method_cleaned.append(length - method_sum)
    result = []
    iterator = 0
    for i in method_cleaned:
        result.append([])
        for j in range(iterator, iterator + i):
            result[-1].append(lst[j])
        iterator += i
    return result


datetime_time = datetime.date.today() + datetime.timedelta(days=1)
formatted_time = datetime_time.strftime("%Y-%m-%d")

f = open(formatted_time + ".pdf", "rb")
r = pdf.PdfReader(f)
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Uncertainties
breakfast_info = [
    [1, 1, 1, 1, 1], # Header
    [1, 1, 1, 1, 1], # Kouwei
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1], # Marco Polo
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1], # Looping
    [0, 1, 1, 0, 1],
    [1, 1, 1, 0, 0], # Piazza
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1], # Fruit / Drink
]
lunch_info = [
    [1, 1, 1, 1, 1], # Header
    [1, 1, 1, 1, 1], # Kouwei
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1], # Marco Polo
    [1, 0, 0, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1], # Looping
    [1, 1, 1, 1, 1], # Piazza
    [1, 1, 1, 1, 1], # Vegetarian
    [1, 1, 1, 1, 1], # Daily Soup
    [1, 1, 1, 1, 1], # Dessert / Fruit / Drink
]
dinner_info = [
    [1, 1, 1, 1, 1], # Header
    [1, 1, 1, 1, 1], # Kouwei
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1], # Marco Polo
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0], # Looping
    [1, 1, 1, 1, 0], # Piazza
    [1, 1, 1, 1, 0], # Vegetarian
    [1, 1, 1, 1, 1], # Daily Soup
    [1, 1, 1, 1, 1], # Dessert / Fruit / Drink
]
breakfast_include = [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
lunch_include = [0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0]
dinner_include = [0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0]


breakfast_en = split_list(
    list(
        filter(
            lambda x: x != "",
            map(
                lambda x: x.strip().strip(string.punctuation).replace("\n", " "),
                split_string_en(
                    r.pages[0]
                    .extract_text()
                    .replace("Orange ， \nButter", "Orange, Butter)")
                    .replace("（", "")
                ),
            ),
        )
    ),
    list(map(sum, breakfast_info)),
)
lunch_en = split_list(
    list(
        filter(
            lambda x: x != "",
            map(
                lambda x: x.strip().strip(string.punctuation).replace("\n", " "),
                split_string_en(r.pages[1].extract_text().replace("（", "")),
            ),
        )
    ),
    list(map(sum, lunch_info)),
)
dinner_en = split_list(
    list(
        filter(
            lambda x: x != "",
            map(
                lambda x: x.strip().strip(string.punctuation).replace("\n", " "),
                split_string_en(r.pages[2].extract_text().replace("（", "")),
            ),
        )
    ),
    list(map(sum, dinner_info)),
)
breakfast_zh = split_list(
    list(
        filter(
            lambda x: x != "",
            map(
                lambda x: x.strip().strip(string.punctuation).replace("\n", " "),
                split_string_zh(
                    r.pages[0]
                    .extract_text()
                    .replace("Orange ， \nButter", "Orange, Butter)")
                    .replace("（", "")
                ),
            ),
        )
    ),
    list(map(sum, breakfast_info)),
)
lunch_zh = split_list(
    list(
        filter(
            lambda x: x != "",
            map(
                lambda x: x.strip().strip(string.punctuation).replace("\n", " "),
                split_string_zh(r.pages[1].extract_text().replace("（", "")),
            ),
        )
    ),
    list(map(sum, lunch_info)),
)
dinner_zh = split_list(
    list(
        filter(
            lambda x: x != "",
            map(
                lambda x: x.strip().strip(string.punctuation).replace("\n", " "),
                split_string_zh(r.pages[2].extract_text().replace("（", "")),
            ),
        )
    ),
    list(map(sum, dinner_info)),
)


def output():

    html_str = ""
    html_str += """<table>
\t<caption>Breakfast 早餐</caption>
\t<colgroup>
\t\t<col style="width: 5%">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%; border-left: 2px solid rgb(180, 180, 180);">
\t</colgroup>
\t<thead>
\t\t<tr>
\t\t\t<th scope="col">Day</th>
\t\t\t<th scope="colgroup" colspan=3>Kouwei</th>
\t\t\t<th scope="colgroup" colspan=3>Marco Polo</th>
\t\t\t<th scope="col">Looping</th>
\t\t\t<th scope="col">Morning Snack</th>
\t\t</tr>
\t</thead>
\t<tbody>\n"""
    for day in range(5):
        if day == 0: 
            html_str += f'\t\t<tr class="today">\n\t\t\t<th scope="row">{days[day]}</th>\n'
        else: 
            html_str += f'\t\t<tr class="not-today">\n\t\t\t<th scope="row">{days[day]}</th>\n'
        for i in range(len(breakfast_en)):
            if breakfast_include[i]:
                if breakfast_info[i][day]:
                    index = sum(breakfast_info[i][:day])
                    html_str += f"\t\t\t<td>{breakfast_en[i][index]}<br>{breakfast_zh[i][index]}</td>\n"
                else:
                    html_str += "\t\t\t<td></td>\n"
        html_str += "\t\t\t<td></td>\n\t\t</tr>\n"
    html_str += """\t\t<tr class="expand">
\t\t\t<th>+</th>
\t\t</tr>
\t</tbody>
</table>
"""

    html_str += """
<table>
\t<caption>Lunch 午餐</caption>
\t<colgroup>
\t\t<col style="width: 5%">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%; border-left: 2px solid rgb(180, 180, 180);">
\t</colgroup>
\t<thead>
\t\t<tr>
\t\t\t<th scope="col">Day</th>
\t\t\t<th scope="colgroup" colspan=2>Kouwei</th>
\t\t\t<th scope="colgroup" colspan=2>Marco Polo</th>
\t\t\t<th scope="col">Looping</th>
\t\t\t<th scope="col">Piazza</th>
\t\t\t<th scope="col">Vegetarian</th>
\t\t\t<th scope="col">Afternoon Snack</th>
\t\t</tr>
\t</thead>
\t<tbody>\n"""
    for day in range(5):
        if day == 0: 
            html_str += f'\t\t<tr class="today">\n\t\t\t<th scope="row">{days[day]}</th>\n'
        else: 
            html_str += f'\t\t<tr class="not-today">\n\t\t\t<th scope="row">{days[day]}</th>\n'
        for i in range(len(lunch_en)):
            if lunch_include[i]:
                if lunch_info[i][day]:
                    index = sum(lunch_info[i][:day])
                    html_str += f"\t\t\t<td>{lunch_en[i][index]}<br>{lunch_zh[i][index]}</td>\n"
                else:
                    html_str += "\t\t\t<td></td>\n"
        html_str += "\t\t\t<td></td>\n\t\t</tr>\n"
    html_str += """\t\t<tr class="expand">
\t\t\t<th>+</th>
\t\t</tr>
\t</tbody>
</table>
"""

    html_str += """
<table>
\t<caption>Dinner 晚餐</caption>
\t<colgroup>
\t\t<col style="width: 5%">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%;">
\t\t<col style="width: 11.875%; border-left: 2px solid rgb(180, 180, 180);">
\t</colgroup>
\t<thead>
\t\t<tr>
\t\t\t<th scope="col">Day</th>
\t\t\t<th scope="colgroup" colspan=2>Kouwei</th>
\t\t\t<th scope="colgroup" colspan=2>Marco Polo</th>
\t\t\t<th scope="col">Looping</th>
\t\t\t<th scope="col">Piazza</th>
\t\t\t<th scope="col">Vegetarian</th>
\t\t\t<th scope="col">Evening Snack</th>
\t\t</tr>
\t</thead>
\t<tbody>\n"""
    for day in range(5):
        if day == 0: 
            html_str += f'\t\t<tr class="today">\n\t\t\t<th scope="row">{days[day]}</th>\n'
        else: 
            html_str += f'\t\t<tr class="not-today">\n\t\t\t<th scope="row">{days[day]}</th>\n'
        for i in range(len(dinner_en)):
            if dinner_include[i]:
                if dinner_info[i][day]:
                    index = sum(dinner_info[i][:day])
                    html_str += f"\t\t\t<td>{dinner_en[i][index]}<br>{dinner_zh[i][index]}</td>\n"
                else:
                    html_str += "\t\t\t<td></td>\n"
        html_str += "\t\t\t<td></td>\n\t\t</tr>\n"
    html_str += """\t\t<tr class="expand">
\t\t\t<th>+</th>
\t\t</tr>
\t</tbody>
</table>
"""

    with open("latest_raw.html", "w") as file:
        file.write(html_str)
        file.close()


output()
