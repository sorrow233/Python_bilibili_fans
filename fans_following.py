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

# 第一部分：设定数据抓取之后保存的地方
folder = "data/fllowing"
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



# 第二部分：将url库满足抓取需求
def change_links():
    global lines   # 使用全局变量，注意不要滥用全局变量，只有这种关键的才适合全局
    lines = []
    with open('data/links.txt', 'r') as f:
        for line in f:
            data = line.rstrip('\n')
            lines.append(data+'fans/follow')
        print(lines)



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


# 第四部分：提取抓取到的数据的地方，且利用两个循环函数保存到Mysql
def save_data():
    # 链接到数据库
    global conn
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        database='fans_following',
        charset='utf8mb4'
    )

    global cursor   # 创建全局游标对象
    cursor = conn.cursor()

    drop_table = "DROP TABLE IF EXISTS links"
    cursor.execute(drop_table)
    print('已删除原表单')

    create_table = '''CREATE TABLE IF NOT EXISTS links
                                (id INT AUTO_INCREMENT PRIMARY KEY,
                                href VARCHAR(255),
                                title VARCHAR(255))'''
    cursor.execute(create_table)
    print('新建表单成功')

    # 链接数据库之后，打开文件然后提取数据
    with open(file_path, 'r', encoding='utf-8') as f:
        fans_following = f.read()
    soup = BeautifulSoup(fans_following, 'html.parser')

    # 初步抓取数据：span和a
    span_tags = soup.find_all('span', class_='fans-name')   # 自动返回列表
    a_href = soup.find_all('a', class_='title')

    # 一次循环抓取两个数据到数据库
    for i, span in enumerate(span_tags):
        title = span.text
        if i < len(a_href):   # 如果两个列表长度不一样，需要加入防止越界.如果你确保两个列表的长度相等，可以不加
            href = a_href[i]['href']  # 这是enumerate方法的关键操作。[i]索引了a_href列表 ['href']提取了索引过后的数据
            insert_query = "INSERT INTO links (href, title) VALUES (%s, %s)"
            cursor.execute(insert_query, (href, title))
            print('数据插入成功')

    conn.commit()  # 提交更改，不提交插入数据代码白写



# 最终环节：真正开始抓取数据的地方，自动抓取，用户设计了隐私会返回nothing之后自动跳过
def fetch_data(links):
    driver = webdriver.Chrome()
    try:
        print(links)
        driver.get(links)
        scroll_bottom(driver)

    except JavascriptException as e:
        print(f"An exception occurred: {e}. Skipping this iteration.")
    finally:
        driver.quit()




# 主函数
def main():
    threads = []   # 存储线程对象
    for link in lines:
        t = threading.Thread(target=fetch_data, args=(link,))
        threads.append(t)
        t.start()

    # 管理线程对象，等待每个线程完成
    for t in threads:
        t.join()



# 执行主函数
if __name__ == '__main__':
    change_links()
    main()    # 启动多线程，多线程会自动调取运行脚本，运行脚本又会自动调用其他函来实现抓取
    save_data()  # 等待多线程全部运行完毕之后，再执行save_data()，save只执行最终一次
