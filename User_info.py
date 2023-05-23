import requests

url = 'https://api.vc.bilibili.com/account/v1/user/cards'
cookies = {'SESSDATA': '7814cba3%2C1700373239%2C7e695%2A51'}
params = {'uids': '34814137,2,3'}

response = requests.get(url, params=params, cookies=cookies)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("请求失败")

