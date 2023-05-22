from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import shutil
from selenium import webdriver
from selenium.common.exceptions import JavascriptException


# 第一部分：将url库满足抓取需求
lines = []
with open('data/links.txt', 'r') as f:
    for line in f:
        data = line.rstrip('\n')
        # print(data)  #
        lines.append(data+'fans/follow')
    print(lines)


# 第二部分：设定抓取数据保存的位置
folder = "data/fllowing"
if os.path.exists(folder):
    # 存在则删除文件，重新添加
    shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)
    print(f'文件 {folder} 已重制')
else:
    os.makedirs(folder, exist_ok=True)  #如果没有data文件夹会自动创建
    print(f'文件 {folder} 已添加')
file_name = "fans_following.html"
file_path = os.path.join(folder, file_name)



# 第三部分：抓取的核心代码，操作为自动拉取到最下面然后保存页面到html文件
def scroll_bottom():
    driver.implicitly_wait(2)  # 等待页面加载完成，最多等待10秒   # 数据抓取失败可开启
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

# 第四部分：真正开始抓取数据的地方，自动抓取，用户设计了隐私会返回nothing之后自动跳过
driver = webdriver.Chrome()
for i in lines:
    try:
        print(i)
        driver.get(i)
        scroll_bottom()
        # 定位翻页按钮并点击
        for i in range(2, 5):
            try:
                next_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[@class='be-pager-item']/a[text()='%s']" % i)))
                next_button.click()
                scroll_bottom()
            except:
                    print('nothing')
                    break
    except JavascriptException as e:
        print(f"An exception occurred: {e}. Skipping this iteration.")
        continue


# 第五部分：提取抓取到的数据的地方


# 第六部分：弄一下多线程或多进程加速，毕竟要抓取的数据量实在太大了
