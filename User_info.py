import requests

with open('links.txt', 'r') as file:
    for url in file:
        url = url.strip()  # 去除换行符和空格

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        response = requests.get(url,headers=headers)

        if response.status_code == 200:
            html_data = response.text

            with open('output.html', 'w', encoding='utf-8') as file:
                file.write(html_data)
                print("网页数据保存成功")
        else:
            print("无法访问网页")
