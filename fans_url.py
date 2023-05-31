from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import shutil

# 代码问题
# 01怎么让产生的数据文件到指定的数据文件夹，不要污染py代码
# 02是否有api地址而我没找到，以及动态网页使用get能请求到多页地址吗
# 代码问题 end

# 打开浏览器并打开网页
driver = webdriver.Chrome()
driver.get("https://space.bilibili.com/35310591/fans/fans")

# 确定文件地址
folder = "data"
# 检查文件是否存在
if os.path.exists(folder):
    # 存在则删除文件，重新添加
    shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)
    print(f'文件 {folder} 已重制')
else:
    os.makedirs(folder, exist_ok=True)  #如果没有data文件夹会自动创建
    print(f'文件 {folder} 已添加')

file_name = "all_html.html"
file_path = os.path.join(folder, file_name)





# 核心代码，自动将页面拉到最下面，加载全部网页,然后保存html到文件夹
def scroll_bottom():
    # driver.implicitly_wait(10)  # 等待页面加载完成，最多等待10秒   # 开启该代码会造成运行缓慢
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
    html = driver.page_source  # 获取数据
    with open(file_path, "a", encoding='utf-8') as f:  # a在这里是追加模式，用w只会保存最后一次数据
        f.write(html)


scroll_bottom() # 抓取第一页数据

# 抓取其他页面
for i in range(2, 5):
    # 定位翻页按钮并点击
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@class='be-pager-item']/a[text()='%s']" % i)))
    next_button.click()
    scroll_bottom()

# 读取本地HTML文件
with open('data/all_html.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 解析HTML文档
soup = BeautifulSoup(html, 'html.parser')

# 提取class为cover的a标签的href
links = []
for a in soup.find_all('a', class_='title'):
    href = 'https:' + a['href']
    print(href + '\n')
    with open('data/links.txt', 'a') as f:
        f.write(href + '\n')
    links.append(a['href'])
