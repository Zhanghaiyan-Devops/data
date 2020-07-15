import requests
import json

# # 把webhook地址赋值给url
url = 'https://oapi.dingtalk.com/robot/send?access_token=07efd7a4eb2def249285487fb4869b8dc5e4b47ada566c535878822a76fbcebe'
# 内容的类型是json格式,字符集必须设为utf-8
headers = {'Content-Type': 'application/json;charset=utf-8'}

# 文本类型
# data = {
#     "msgtype": "text",  # 纯文本格式
#     "text": {
#         "content": "nsd1909我就是我, 是不一样的烟火@156xxxx8827"  #消息正文
#     },
#     "at": {
#         "atMobiles": [
#             "156xxxx8827", # 发消息时要@哪些人
#             "189xxxx8325"
#         ],
#         "isAtAll": False    # 是否@所有人
#     }
# }

# link类型
# data = {
#     "msgtype": "link",
#     "link": {
#         "text": "nsd1909这个即将发布的新版本，创始人xx称它为红树林。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是红树林",
#         "title": "时代的火车向前开",
#         "picUrl": "https://i04picsos.sogoucdn.com/24b7ffb04628c42b",   # 图片的url地址
#         "messageUrl": "http://www.sogou.com"    # 超链接,点一下会跳到哪个网站
#     }
# }

# markdown类型,也是一种纯文本格式

data = {
     "msgtype": "markdown",
     "markdown": {
         "title":"杭州天气",
         "text": "nsd1909#### 杭州天气 @150XXXXXXXX \n> 9度，西北风1级，空气良89，相对温度73%\n> ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n> ###### 10点20分发布 [天气](https://www.dingtalk.com) \n"
     },
      "at": {
          "atMobiles": [
              "150XXXXXXXX"
          ],
          "isAtAll": False
      }
 }

r = requests.post(url, headers=headers, data=json.dumps(data))
print(r.json())  # 打印返回信息