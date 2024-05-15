import os
import json
import datetime
import subprocess
from bs4 import BeautifulSoup
from encode_picture import encode


# Setting up

with open("cycle_days.json") as file: 
	cycle_days = json.load(file)

datetime_time = datetime.date.today() + datetime.timedelta(days=1)
formatted_time = datetime_time.strftime("%Y-%m-%d")
formatted_time_yearless = datetime_time.strftime("%m-%d")
formatted_time_weekday = datetime_time.strftime("%w")
formatted_time_weekday_full = datetime_time.strftime("%A")
zh_weekdays = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
formatted_time_weekday_zh = zh_weekdays[int(formatted_time_weekday)]
cycle_day = cycle_days[formatted_time]

base_dir = os.path.abspath(os.path.dirname(__file__))


# Before Everything

html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Daily Bulletin {formatted_time}</title>
<link rel="stylesheet" href="files/styles.css">
</head>
<body>
<header>
<h1>Daily Bulletin 每日公告</h1>
<p><time datetime="{formatted_time}">{formatted_time}</time>, {formatted_time_weekday_full}, Day {cycle_day}<p>
</header>
<article>
<p>Happy {formatted_time_weekday_full}! Thank you very much for supporting the Daily Bulletin. If you want to provide any suggestions, feel free to fill this <a href="https://forms.office.com/r/ui7iTB5BrD">form</a>. Please note that this is supplementary to The Week Ahead: please still check The Week Ahead for official information. By default, we will deliver a similar email to your inbox every day; if you no longer wish to receive this email anymore, please <a href="https://forms.office.com/r/S8LpFi87WV">unsubscribe</a>. Thank you!<br>{formatted_time_weekday_zh}快乐！感谢您支持每日公告。如果您想提出建议，请填写这个<a href="https://forms.office.com/r/ui7iTB5BrD">问卷</a>。请注意，每日公告只是每周展望的补充，若想获得官方信息，请继续查阅每周展望。我们每天都会向您的收件箱投递一封类似的邮件；如果您不想继续接收每日公告，请<a href="https://forms.office.com/r/S8LpFi87WV">取消订阅</a>。谢谢！</p>
'''


# Exam Reminders


if not os.path.isfile("exam_reminders/" + formatted_time + ".html"): 
	os.chdir(os.path.join(base_dir, "exam_reminders/"))
	try: 
		subprocess.run(["python3", "update.py"])
	except BaseException as e: 
		print(e)
	os.chdir(os.path.join(base_dir))

if os.path.isfile("exam_reminders/" + formatted_time + ".html"):
	with open("exam_reminders/" + formatted_time + ".html") as file: 
		tmp = file.read()
		if tmp: 
			html += '<h2>Exam Reminders 考试计划</h2>\n'
			html += tmp


# Community Time

if not os.path.isfile("community_time/" + formatted_time + ".html"): 
	os.chdir(os.path.join(base_dir, "community_time/"))
	subprocess.run(["python3", "update.py"])
	os.chdir(os.path.join(base_dir))

with open("community_time/" + formatted_time + ".html") as file: 
	tmp = file.read()
	if tmp: 
		html += '<h2>Community Time 午休时间</h2>\n'
		html += tmp


# Important Events

if not os.path.isfile("important_events/" + formatted_time + ".html"): 
	os.chdir(os.path.join(base_dir, "important_events/"))
	subprocess.run(["python3", "update.py"])
	os.chdir(os.path.join(base_dir))

with open("important_events/" + formatted_time + ".html") as file: 
	tmp = file.read()
	if tmp: 
		html += '<h2>Important Events 重要事件</h2>\n'
		html += tmp
		html += '<p><cite>Fetched from Songjiang Student Calendar.<br>选自松江校区学生日历。</cite></p>\n'


# New Notices

if os.path.isfile("notices/" + formatted_time + ".html"): 
	with open("notices/" + formatted_time + ".html") as file: 
		tmp = file.read()
		if tmp: 
			html += '<h2>New Notices 最新通知</h2>\n'
			html += tmp
	with open("notices/latest.html", "w") as file: 
		file.write(tmp)


# Delicious Dinings

if not os.path.isfile("menu/" + formatted_time + ".html"): 
	os.chdir(os.path.join(base_dir, "menu/"))
	subprocess.run(["python3", "update.py"])
	os.chdir(os.path.join(base_dir))

with open("menu/" + formatted_time + ".html") as file: 
	tmp = file.read()
	if tmp: 
		html += '<h2>Delicious Dinings 今日佳肴</h2>\n'
		html += tmp


# Daily Inspiration

with open("daily_inspiration/" + formatted_time + ".html") as file:
	tmp = file.read()
	if tmp: 
		html += '<h2>Daily Inspiration 每日灵感</h2>\n'
		html += tmp


# On This Day

html += '<h2>On This Day 以史为鉴</h2>\n'

with open("on_this_day/" + formatted_time_yearless + ".html") as file: 
	otd_en_soup = BeautifulSoup(file, "html.parser")
with open("on_this_day_zh/" + formatted_time_yearless + ".html") as file: 
	otd_zh_soup = BeautifulSoup(file, "html.parser")
	
(en_p1, en_p2) = tuple(otd_en_soup.find_all("p"))
en_ul = otd_en_soup.find("ul")
zh_p1 = otd_zh_soup.find("p")
zh_ul = otd_zh_soup.find("ul")

html += (str(en_p1) + str(zh_p1)).replace("</p><p>", "<br>")
html += str(en_ul)
html += str(zh_ul)
html += str(en_p2)
html += '<p><cite>Fetched from Wikipedia.<br>选自维基百科。</cite></p>\n'


# In the News

html += '<h2>In the News 时事要闻</h2>\n'

os.chdir(os.path.join(base_dir, "in_the_news/"))
subprocess.run(["python3", "in_the_news.py"])
os.chdir(os.path.join(base_dir, "in_the_news_zh/"))
subprocess.run(["python3", "in_the_news.py"])
os.chdir(os.path.join(base_dir))

with open("in_the_news/latest.html") as file: 
	itn_en_soup = BeautifulSoup(file, "html.parser")
with open("in_the_news_zh/latest.html") as file: 
	itn_zh_soup = BeautifulSoup(file, "html.parser")

en_ul = itn_en_soup.find("ul")
en_p1 = itn_en_soup.find("p")
zh_ul = itn_zh_soup.find("ul")
zh_p1 = itn_zh_soup.find("p")

html += str(en_ul)
html += str(zh_ul)
html += str(en_p1)
html += str(zh_p1)
html += '<p><cite>Fetched from Wikipedia.<br>选自维基百科。</cite></p>\n'



'''
# The School Inspires

with open("part_school_inspires.html") as file: 
	tmp = file.read()
	if tmp: 
		html += '<h2>The School Inspires 学校灵感</h2>\n'
		html += tmp


# Rather New Notices

if not os.path.isfile("notices/" + formatted_time + ".html"): 
	with open("notices/latest.html") as file: 
		tmp = file.read()
		if tmp: 
			html += '<h2>Rather New Notices 较新通知</h2>\n'
			html += tmp


# Regular Notices

with open("part_regular_notices.html") as file: 
	tmp = file.read()
	if tmp: 
		html += '<h2>Regular Notices 常规通知</h2>\n'
		html += tmp


# The School Recommends

with open("part_school_recommends.html") as file: 
	tmp = file.read()
	if tmp: 
		html += '<h2>The School Recommends 学校推荐</h2>\n'
		html += tmp
'''

# After Everything


html += '''</article>
<footer>
<p><a href="https://albertttan.github.io/daily-bulletin/">Home Page</a> · <a href="https://albertttan.github.io/daily-bulletin/archive.html">Archive</a> · <a href="mailto:s22505@ykpaoschool.cn">Contact</a></p>
</footer>
<script src="files/table-expand.js"></script>
</body>
</html>
'''

with open("html/" + formatted_time + ".html", "w") as file: 
	file.write(html)
