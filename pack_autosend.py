import os
import json
import base64
import datetime
from bs4 import BeautifulSoup
from encode_picture import encode


# Before Everything

datetime_time = datetime.date.today() + datetime.timedelta(days=1)
formatted_time = datetime_time.strftime("%Y-%m-%d")


# Format Email

with open("mailing_list-1.txt") as file: 
	recipients_1 = ", ".join(map(lambda x: "<" + x.strip() + ">", file.readlines()))
with open("mailing_list-2.txt") as file: 
	recipients_2 = ", ".join(map(lambda x: "<" + x.strip() + ">", file.readlines()))

template_1 = f'''Date: Thu, 1 Jan 1970 00:00:00 +0000
Subject: Daily Bulletin {formatted_time}
From: <s22505@ykpaoschool.cn>
Cc: <duncan.weller@ykpaoschool.cn>
Bcc: {recipients_1}
Content-Transfer-Encoding: base64
Content-Type: text/html; charset=UTF-8

'''
template_2 = f'''Date: Thu, 1 Jan 1970 00:00:00 +0000
Subject: Daily Bulletin {formatted_time}
From: <s22505@ykpaoschool.cn>
Cc: <cora.chen@ykpaoschool.cn>
Bcc: {recipients_2}
Content-Transfer-Encoding: base64
Content-Type: text/html; charset=UTF-8

'''


# Format HTML for EML

with open("html/" + formatted_time + ".html") as file: 
	soup = BeautifulSoup(file, "html.parser")
with open("files/styles.css") as file: 
	css = file.read()

soup.find("link").decompose()
style = soup.new_tag("style")
style.string = css
soup.head.append(style)

soup.find("script").decompose()
expands = soup.find_all("tr", class_="expand")
for expand in expands: 
	expand.decompose()

imgs = soup.find_all("img")
for img in imgs: 
	img["src"] = encode(img["src"])

html_1 = str(soup).replace("Daily Bulletin. If you", f'Daily Bulletin. We <em>strongly recommend</em> that you view an <a href="https://albertttan.github.io/daily-bulletin/{formatted_time}.html">online version</a> for better visual effects. If you').replace("公告。如果", f'公告。我们<em>强烈建议</em>您浏览<a href="https://albertttan.github.io/daily-bulletin/{formatted_time}.html">在线版</a>以获得更佳的视觉效果。如果')
html_2 = str(soup).replace("Daily Bulletin. If you", f'Daily Bulletin. We <em>strongly recommend</em> that you view an <a href="https://albertttan.github.io/daily-bulletin/{formatted_time}.html">online version</a> for better visual effects. If you want to share any inspirations, please fill this <a href="https://forms.office.com/r/Ptx2tj7T0N">form</a>, or this <a href="https://forms.office.com/r/FVXVq97rTb">form</a> anonymously. If you').replace("公告。如果", f'公告。我们<em>强烈建议</em>您浏览<a href="https://albertttan.github.io/daily-bulletin/{formatted_time}.html">在线版</a>以获得更佳的视觉效果。如果您想分享任何灵感，请填写这个<a href="https://forms.office.com/r/Ptx2tj7T0N">问卷</a>，或匿名填写这个<a href="https://forms.office.com/r/FVXVq97rTb">问卷</a>。如果')
encoded_html_1 = base64.b64encode(html_1.encode("utf-8")).decode("utf-8", "surrogateescape")
encoded_html_2 = base64.b64encode(html_2.encode("utf-8")).decode("utf-8", "surrogateescape")


# Output

with open("eml/Daily Bulletin " + formatted_time + ".eml", "w") as file: 
	file.write(template_1 + encoded_html_1)
	file.close()
with open("eml/Daily Bulletin " + formatted_time + "-2.eml", "w") as file: 
	file.write(template_2 + encoded_html_2)
	file.close()




html_1
html_2 

with open("mailing_list-1.txt") as file: 
	recipients_1_aug = map(lambda x: x.strip(), file.readlines())
with open("mailing_list-2.txt") as file: 
	recipients_2_aug = map(lambda x: x.strip(), file.readlines())

import logging
import msal  # type: ignore
import requests
import datetime
from configparser import ConfigParser
from typing import Any, Optional


def acquire_token(app: msal.PublicClientApplication, config: ConfigParser) -> str:
	result = app.acquire_token_by_username_password(
		config["credentials"]["username"],
		config["credentials"]["password"],
		scopes=config["credentials"]["scope"].split(" "),
	)

	if "access_token" in result:
		assert type(result["access_token"]) is str
		return result["access_token"]
	else:
		raise ValueError("Authentication error in password login")


def sendmail(
	token: str,
	subject: str,
	body: str,
	to: list[str],
	bcc: list[str],
	cc: list[str],
	when: Optional[datetime.datetime] = None,
	content_type: str = "HTML",
	importance: str = "Normal",
) -> None:
	data = {
		"subject": subject,
		"importance": importance,
		"body": {"contentType": content_type, "content": body},
		"toRecipients": [{"emailAddress": {"address": a}} for a in to],
		"ccRecipients": [{"emailAddress": {"address": a}} for a in cc],
		"bccRecipients": [{"emailAddress": {"address": a}} for a in bcc],
	}

	if when is not None:
		#if when.tzinfo is None:
		#	raise ValueError("Naive datetimes are no longer supported")
		utcwhen = when.astimezone(datetime.timezone.utc)
		isoval = utcwhen.isoformat(timespec="seconds").replace("+00:00", "Z")
		data["singleValueExtendedProperties"] = [
			{"id": "SystemTime 0x3FEF", "value": isoval}
		]

	response = requests.post(
		"https://graph.microsoft.com/v1.0/me/messages",
		json=data,
		headers={"Authorization": "Bearer " + token},
	).json()
	response2 = requests.post(
		"https://graph.microsoft.com/v1.0/me/messages/%s/send" % response["id"],
		headers={"Authorization": "Bearer " + token},
	)
	if response2.status_code != 202:
		raise ValueError(
			"Graph response to messages/%s/send returned someething other than 202 Accepted"
			% response["id"],
			response2,
		)

def main() -> None:
	config = ConfigParser()
	config.read("config.ini")
	app = msal.PublicClientApplication(
		config["credentials"]["client_id"],
		authority=config["credentials"]["authority"],
	)
	token = acquire_token(app, config)
	import datetime
	import zoneinfo
	shanghai_timezone = zoneinfo.ZoneInfo('Asia/Shanghai')
	current_time = datetime.datetime.now(tz=shanghai_timezone)
	tomorrow = current_time + datetime.timedelta(days=1)
	target_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 6, 30, 0, tzinfo=shanghai_timezone)
	utcwhen = target_time.astimezone(datetime.timezone.utc)
	isoval = utcwhen.isoformat(timespec="seconds").replace("+00:00", "Z")
	when = target_time

	sendmail(
		token,
		subject="Daily Bulletin %s" % formatted_time,
		body=html_1,
		to=[],
		cc=["duncan.weller@ykpaoschool.cn"],
		bcc=recipients_1_aug,
		when=when,
		content_type="HTML",
		importance="Normal",
	)
	sendmail(
		token,
		subject="Daily Bulletin %s" % formatted_time,
		body=html_2,
		to=[],
		cc=["cora.chen@ykpaoschool.cn"],
		bcc=recipients_2_aug,
		when=when,
		content_type="HTML",
		importance="Normal",
	)

main()

os.system(f"cp html/{formatted_time}.html /Users/albert/albertttan.github.io/daily-bulletin/{formatted_time}.html")
os.chdir("/Users/albert/albertttan.github.io/")
os.system("git add .")
os.system('git commit -m "Daily Update of Daily Bulletin"')
os.system("git push origin main")
