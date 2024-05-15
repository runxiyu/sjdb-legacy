import os
import json
import base64
import datetime
from bs4 import BeautifulSoup
from encode_picture import encode



recipients_1 = ""

template_1 = f'''Date: Thu, 1 Jan 1970 00:00:00 +0000
Subject: Re
From: <s22505@ykpaoschool.cn>
Cc: <duncan.weller@ykpaoschool.cn>
Bcc: {recipients_1}
Content-Transfer-Encoding: base64
Content-Type: text/html; charset=UTF-8

'''



# Format HTML for EML

with open("exam_supplement.html") as file: 
	soup = BeautifulSoup(file, "html.parser")

with open("files/styles.css") as file: 
	css = file.read()

soup.find("link").decompose()
style = soup.new_tag("style")
style.string = css
soup.head.append(style)

html_1 = str(soup)
encoded_html_1 = base64.b64encode(html_1.encode("utf-8")).decode("utf-8", "surrogateescape")


# Output

with open("exam_supplement.eml", "w") as file: 
	file.write(template_1 + encoded_html_1)
	file.close()
