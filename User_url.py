from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

# 启动 Chrome 浏览器
driver = webdriver.Chrome()

# 访问目标网站
driver.get("https://space.bilibili.com/35310591/fans/fans")

# 等待页面加载完成
driver.implicitly_wait(10)

# 拉到最下面，加载全部网页
while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

# 获取完整的 HTML 页面
html = driver.page_source

#创建文件将数据写入
filename = "html.txt"  # 文件名
with open(f'1.html', "w" , encoding='utf-8') as f:
    f.write(html)

for i in range(2, 5):
    # 定位翻页按钮并点击
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='be-pager-item']/a[text()='%s']" % i)))
    next_button.click()

    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

    # 获取当前页面的源代码并保存
    html = driver.page_source
    with open(f'1.html', "a", encoding='utf-8') as f:   # a表示追加模式打开
        f.write(html)




# 读取本地HTML文件
with open('1.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 解析HTML文档
soup = BeautifulSoup(html, 'html.parser')

# 提取class为cover的a标签的href
links = []
for a in soup.find_all('a', class_='cover'):
    links.append(a['href'])

# 将所有链接前面加上https:
for i in range(len(links)):
    links[i] = re.sub(r'^//', 'https://', links[i])
print(links)


# 将链接保存到文件中，每个链接占一行
with open('links.txt', 'w') as f:
    for link in links:
        f.write(link + '\n')

