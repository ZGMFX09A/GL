# -*-coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common import by
from bs4 import BeautifulSoup
import re

find_link = re.compile('<a (href=".*?")>.*?</a>')
link = 'https://www.linovelib.com/novel/1854/number.html'
n = 67239
c = 0
st_li = []

start = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace">
<head>
  <link href="../Styles/style.css" rel="stylesheet" type="text/css" />
  <script src="../Misc/notereplace.js" type="text/javascript">
</script>
  <title>biaoti</title>
</head>

<body>
  <div>
  '''


end = '''  </div>
</body>
</html>'''

driver = webdriver.Chrome()

driver.get(link.replace('number', str(n)))


def get_page():
    global c
    html = driver.page_source
    bs = BeautifulSoup(html, 'html.parser')
    ele = bs.find_all('a')[-1]
    np = driver.find_element(by=by.By.CSS_SELECTOR, value=f'a[{re.findall(find_link, str(ele))[0]}')
    title = bs.find_all('h1')[0]
    if '（' not in str(title) and '）' not in str(title):
        st_li.append(title)
    p_li = bs.find_all('p', class_='')
    for s in p_li:
        st_li.append(str(s))
    if '（2/2）' in str(title) or '（3/3）' in str(title) or '（4/4）' in str(title):
        with open(f'{c}.xhtml', 'w', encoding='utf-8') as f:
            biaoti = str(st_li[0].text.replace('&', '&amp;'))
            st_li[0] = str(st_li[0])
            f.write((start.replace('biaoti', biaoti)+'\n\n'.join(st_li)+end).replace('（2/2）', '').replace('（3/3）', ''))
        st_li.clear()
        c += 1

    np.click()


for i in range(29):
    get_page()
