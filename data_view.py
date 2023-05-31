# 提取数据根据词频添加到数据库

import re
import jieba
import pymysql
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 连接MySQL数据库
conn = pymysql.connect(host='localhost', user='root', password='root', database='fans_following')
cursor = conn.cursor()

# 删除表
drop_table_sql = '''
    drop table if exists top_words;
'''
cursor.execute(drop_table_sql)

# 创建一个名为top_words的表
create_table_sql = '''
    CREATE TABLE top_words (
        id INT(11) NOT NULL AUTO_INCREMENT,
        word VARCHAR(255) NOT NULL,
        count INT(11) NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''
cursor.execute(create_table_sql)

# 从数据库中读取数据
sql = 'SELECT title FROM links'  # 这里是表单，不是数据库
cursor.execute(sql)
results = cursor.fetchall()  # fetch抓取，将提取出来的数据保持到了results

# 使用jieba分词并统计词频
word_counts = {}
for result in results:
    # 取评论
    content = result[0]
    # 正则保存中文  将字符串content中的非中文字符替换为空字符串。
    content = re.sub(r'[^\u4e00-\u9fa5]+', '', content)
    # 结巴分词
    # words = jieba.lcut(content)
    # 循环遍历算出现次数
    if len(content) > 1:
        if content not in word_counts:
            word_counts[content] = 1
        else:
            word_counts[content] += 1


# 生成词云图
wordcloud = WordCloud(font_path='simhei.ttf',
                      background_color='white',
                      max_words=100,
                      max_font_size=100,
                      width=800,
                      height=600).generate_from_frequencies(word_counts)

# 显示词云图
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 按词频排序
sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# 取出前十个词
top_words = sorted_word_counts[:10]
print(top_words)

# 将结果写入数据库
for word, count in top_words:
    sql = 'INSERT INTO top_words(word, count) VALUES (%s, %s)'
    cursor.execute(sql, (word, count))

# 提交修改并关闭连接
conn.commit()
cursor.close()
conn.close()
