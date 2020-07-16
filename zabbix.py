import requests
import json

url = 'http://192.168.1.100/api_jsonrpc.php'    # url地址
headers = {'Content-Type': 'application/json-rpc'}  # 头部信息
#####################################################
# 查看非隐私信息, 不需要认证, 可以直接获取
# data = {
#     "jsonrpc": "2.0",   # zabbix使用的协议, 固定值,不用改
#     "method": "apiinfo.version",   # 获取软件版本的方法
#     "params": [],     # 参数
#     "id": 1,    # 随便填一个数字,表示作业号
# }

# 查看隐私信息需要认证, 通过用户名和密码获取token
# data = {
#     "jsonrpc": "2.0",
#     "method": "user.login",
#     "params": {
#         "user": "Admin",
#         "password": "111111"
#     },
#     "id": 1,
#     "auth": None
# }
# dd3d107a8d9c2cd98310e0b7fc179126

# 获取主机信息
# data = {
#     "jsonrpc": "2.0",
#     "method": "host.get",
#     "params": {
#         "output": "extend",
#         "filter": {     # 过滤满足条件的主机
#             "host": [
#                 # "Zabbix server",
#                 # "Linux server"
#             ]
#         }
#     },
#     "id": 2,
#     "auth": "dd3d107a8d9c2cd98310e0b7fc179126"
# }
# 'hostid': '10259'
#####################################################
# 删除主机
# data = {
#     "jsonrpc": "2.0",
#     "method": "host.delete",
#     "params": [
#         "10259",  # 填写要删除主机的hostid
#         # "32"
#     ],
#     "auth": "dd3d107a8d9c2cd98310e0b7fc179126",
#     "id": 1
# }
#####################################################
# 创建主机要先获取组丶模板
# 获取组, 'groupid': '2'
# data = {
#     "jsonrpc": "2.0",
#     "method": "hostgroup.get",
#     "params": {
#         "output": "extend",
#         "filter": {
#             "name": [
#                 # "Zabbix servers",
#                 "Linux servers"
#             ]
#         }
#     },
#     "auth": "dd3d107a8d9c2cd98310e0b7fc179126",
#     "id": 1
# }
#####################################################
# 获取模板, 'templateid': '10001'
# data = {
#     "jsonrpc": "2.0",
#     "method": "template.get",
#     "params": {
#         "output": "extend",
#         "filter": {
#             "host": [
#                 "Template OS Linux",
#                 # "Template OS Windows"
#             ]
#         }
#     },
#     "auth": "dd3d107a8d9c2cd98310e0b7fc179126",
#     "id": 1
# }
#####################################################
# 创建主机
data = {
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": "dbserver1",  # 主机名
        "interfaces": [  # zabbix agent接口配置
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": "192.168.4.10",   # 要创建的主机IP
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": "2"
            }
        ],
        "templates": [
            {
                "templateid": "10001"
            }
        ],
        "inventory_mode": 0,  # 资产清单
        "inventory": {
            "macaddress_a": "qwertyu",  # 可以随便写
            "macaddress_b": "56768"     # 可以随便写
        }
    },
    "auth": "dd3d107a8d9c2cd98310e0b7fc179126",
    "id": 1
}




#####################################################
r = requests.post(url, headers=headers, data=json.dumps(data))
print(r.json()) #返回的消息, 主要关注result即可
