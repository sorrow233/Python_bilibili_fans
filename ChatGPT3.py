from selenium import webdriver
import time

from selenium.common import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import shutil
import pymysql
import threading

# 先链接数据库
def conn_mysql():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        database='fans_following',
        charset='utf8mb4'
    )

    # 创建游标对象
    cursor = conn.cursor()

    # 删除表单，如果存在
    drop_table = "DROP TABLE IF EXISTS links"
    cursor.execute(drop_table)

    # 创建表格（如果不存在）
    create_table = '''CREATE TABLE IF NOT EXISTS links
                            (id INT AUTO_INCREMENT PRIMARY KEY,
                            href VARCHAR(255),
                            title VARCHAR(255))'''
    cursor.execute(create_table)

# 第一部分：将url库满足抓取需求
def links():
    lines = []
    with open('data/links.txt', 'r') as f:
        for line in f:
            data = line.rstrip('\n')
            lines.append(data+'fans/follow')
        print(lines)

# 第二部分：设定抓取数据保存的位置
folder = "data/fllowing"
def flie_address():
    if os.path.exists(folder):
        # 存在则删除文件，重新添加
        shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)
        print(f'文件 {folder} 已重制')
    else:
        os.makedirs(folder, exist_ok=True)  # 如果没有data文件夹会自动创建
        print(f'文件 {folder} 已添加')
    file_name = "fans_following.html"
    file_path = os.path.join(folder, file_name)


# 第三部分：抓取的核心代码，操作为：自动拉取到最下面然后保存页面到html文件
def scroll_bottom(driver):
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
def fetch_data(links):
    driver = webdriver.Chrome()
    try:
        print(links)
        driver.get(links)
        scroll_bottom(driver)
        save_data()
    except JavascriptException as e:
        print(f"An exception occurred: {e}. Skipping this iteration.")
    finally:
        driver.quit()


# 第五部分：提取抓取到的数据的地方
def save_data():
    soup = BeautifulSoup(file_path, 'html.parser')

    # 初步抓取数据：span和a
    span_tags = soup.find_all('span', class_='fans-name')
    a_href = soup.find_all('a', class_='title')

    # 一次循环抓取两个数据到数据库
    for span in span_tags:
        title = span.text
        href = None  # 初始化href
        for a in a_href:
            href = a['href']
            break  # 只获取第一个a标签的href
        if href:
            insert_query = "INSERT INTO links (href, title) VALUES (%s, %s)"
            cursor.execute(insert_query, (href, title))

    conn.commit()


# 主函数
def main():
    threads = []
    for link in lines:
        t = threading.Thread(target=fetch_data, args=(link,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


# 执行主函数
if __name__ == '__main__':
    main()
