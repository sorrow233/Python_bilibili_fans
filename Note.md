https://api.bilibili.com/x/space/wbi/acc/info?mid=3493130124921039&token=&platform=web&web_location=1550101&w_rid=7aac6a2a4e2f297f6279e39477e84106&wts=1684738781

w_rid每一次都会更改，因此想调用api抓取必须先破解w_rid

JS HOOK：不破解直接注入修改？太酷了，很符合我对hacking的想象，有空学一下。爬虫简单，JS才是难点啊，能学会JS混淆破解，离进监狱也不远了





https://space.bilibili.com/3493130124921039/

https://space.bilibili.com/3493130124921039/fans/follow

~~抓取个人信息实在太难了，涉及了很复杂的JS加密，而HTML网页根本没有显示这些个人信息，开摆~~
找到了一个api，果然，用别人的轮子比自己造简单太多了

01 抓取关注列表     虽然一点简单的代码写了很久，但做出来之后看着自己的爬虫疯狂爬取页面的感觉真的太刺激了

02 最近投币视频

03 收藏列表，不是收藏夹，相当于订阅的合集
