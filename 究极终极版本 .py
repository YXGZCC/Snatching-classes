import requests
import re
from PIL import Image
import io
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json
import time
import websocket

def pad(text):
    block_size = 16
    padding = block_size - len(text) % block_size
    return text + chr(padding) * padding

def unpad(text):
    padding = ord(text[-1])
    return text[:-padding]


def encrypt(text, key):
    # 使用 PKCS7 填充
    text = pad(text)
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    ciphertext = cipher.encrypt(text.encode("utf-8"))
    return base64.b64encode(ciphertext).decode("utf-8")

def decrypt(encrypted_text, key):
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    decrypted_text = cipher.decrypt(base64.b64decode(encrypted_text))
    return unpad(decrypted_text).decode("utf-8")
# 定义获取验证码的函数
def acq_PIN():
    url = 'http://xkfw.xasyu.cn/xsxk/auth/captcha'
    headers = {
        'Referer': 'http://xkfw.xasyu.cn/xsxk/profile/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    response = requests.post(url=url, headers=headers)

    if response.status_code == 200:
        response_text = response.text
        url2 = re.findall('"captcha": "(.*)",', response_text)[0]
        uuid = re.findall('"uuid": "(.*)"', response_text)[0]

        a = url2.split(',')[1]
        imagedata = base64.b64decode(a)

        image = Image.open(io.BytesIO(imagedata))
        image.show()  # 显示图像

        with open('1.jpg', 'wb') as file:
            file.write(imagedata)

        print(f"验证码图片已保存为1.jpg")
        print(f"uuid: {uuid}")
        return uuid
    else:
        print("获取验证码图片失败")
        return None


def login(Account, PS, PIN, uuid):
    s = requests.Session()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Host': 'xkfw.xasyu.cn',
        'Origin': 'http://xkfw.xasyu.cn',
        'Referer': 'http://xkfw.xasyu.cn/xsxk/profile/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        # 添加其他标头信息，如Authorization和Cookie
    }
    if uuid and PIN:
        url_now = 'http://xkfw.xasyu.cn/xsxk/web/now'
        data_now = {}
        response_now = s.post(url=url_now, data=data_now, headers=headers).json()
        if response_now['code'] == 200:
            print("now1请求成功")
            print(response_now)
        else:
            print("now1请求失败")
            print(response_now)

        url_login = 'http://xkfw.xasyu.cn/xsxk/auth/login'
        data_login = {
            'loginname': Account,
            'password': PS,
            'captcha': PIN,
            'uuid': uuid
        }
        print(f"时间请求发送成功，uuid: {uuid}")

        response_login = s.post(url=url_login, data=data_login, headers=headers).json()
        token = response_login["data"]["token"]
        if response_login['code'] == 200:
            print("登录成功，展示提交的登录信息")
            print(f"Account: {Account}")
            print(f"PS: {PS}")
            print(f"PIN: {PIN}")
            print(f"uuid: {uuid}")
            print("展示返回的信息")
            print("Token:", token)
        else:
            print("登录失败，展示提交的登录信息")
            print(f"Account: {Account}")
            print(f"PS: {PS}")
            print(f"PIN: {PIN}")
            print(f"uuid: {uuid}")
            print("展示返回的信息")
            print(response_login)

        batchId ="7feb0bfe885f4beb8239786163dfa69b"
#上面都ok，下面是user请求

    return token

def user(Authorization):
    s2 = requests.Session()
    url_user = 'http://xkfw.xasyu.cn/xsxk/elective/user'
    data_user = {'batchId': '7feb0bfe885f4beb8239786163dfa69b'}
    headers_user = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization':Authorization,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie':Authorization,
        'DNT': '1',
        'Host': 'xkfw.xasyu.cn',
        'Origin': 'http://xkfw.xasyu.cn',
        'Referer': 'http://xkfw.xasyu.cn/xsxk/profile/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    response_user = s2.post(url=url_user, data=data_user, headers=headers_user).json()
    if response_user['code'] == 200:
        print("user请求成功")
        print(response_user)
    else:
        print("user请求失败")
        print(response_user)

def now2(Authorization):
    s3 = requests.Session()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': Authorization,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': Authorization,
        'DNT': '1',
        'Host': 'xkfw.xasyu.cn',
        'Origin': 'http://xkfw.xasyu.cn',
        'Referer': 'http://xkfw.xasyu.cn/xsxk/profile/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    if uuid and PIN:
        url_now = 'http://xkfw.xasyu.cn/xsxk/web/now'
        data_now = {}
        response_now = s3.post(url=url_now, data=data_now, headers=headers).json()
        if response_now['code'] == 200:
            print("now2请求成功")
            print(response_now)
        else:
            print("now2请求失败")
            print(response_now)

def listpost(Authorization,lei,clazzId,page):
    s4 = requests.Session()
    url_list = 'http://xkfw.xasyu.cn/xsxk/elective/clazz/list'
    data_list = {
        'teachingclazzType':'XGKC',
        'pageNumber':page,
        'pageSize':'10',
        'orderBy':' ',
        'campus':'1',
        'XGXKLB':lei
    }
    headers_list = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': Authorization,
        'batchid': '7feb0bfe885f4beb8239786163dfa69b',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': Authorization,
        'DNT': '1',
        'Host': 'xkfw.xasyu.cn',
        'Origin': 'http://xkfw.xasyu.cn',
        'Referer': 'http://xkfw.xasyu.cn/xsxk/elective/grablessons?batchId=7feb0bfe885f4beb8239786163dfa69b',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    response_list = s4.post(url=url_list, data=json.dumps(data_list), headers=headers_list)

    if response_list.status_code == 200:
        print("list请求成功")
        time.sleep(1.0)
        time.sleep(1.0)
        i = 0
        data = response_list.json()
        target_teaching_clazz_id = clazzId
        secret_val = None

        found_target_clazz = False  # 用于标记是否找到了目标课程

        for row in data['data']['rows']:
            if any(limit.get('teachingclazzID') == target_teaching_clazz_id for limit in row.get('limitKindList', [])):
                found_target_clazz = True  # 找到了目标课程
            elif found_target_clazz and 'secretVal' in row:
                secret_val = row['secretVal']
                break



        if secret_val is not None:
            print(f"找到 {target_teaching_clazz_id} 对应的 secretVal 值为: {secret_val}")
            return secret_val
        else:
            print(f"未找到 {target_teaching_clazz_id} 对应的 secretVal")

    else:
        print("list请求失败")




def clazzpost(Authorization,clazzId,secretVal):
    s6 = requests.Session()
    url_list = 'http://xkfw.xasyu.cn/xsxk/elective/clazz/add'
    data_list = {
        'clazzType': 'XGKC',
        'clazzId': clazzId,
        'secretVal': secretVal
    }
    headers_list = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': Authorization,
        'batchid': '7feb0bfe885f4beb8239786163dfa69b',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': Authorization,
        'DNT': '1',
        'Host': 'xkfw.xasyu.cn',
        'Origin': 'http://xkfw.xasyu.cn',
        'Referer': 'http://xkfw.xasyu.cn/xsxk/elective/grablessons?batchId=7feb0bfe885f4beb8239786163dfa69b',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    print("开始抢课，参数校验")
    print(f"找到 {clazzId} 对应的 secretVal 值为: {secretVal}")

    while True:
        response = s6.post(url=url_list, data=json.dumps(data_list), headers=headers_list)
        response_data = response.json()  # 解析响应内容
        time.sleep(1.0)

        if response.status_code == 200:
            if response_data.get('code') == 200:
                print("抢课成功")
                print(response_data)
                print("抢课到此结束，抢其它课请重新运行此程序")
                break
            elif response_data.get('code') == 500:
                print("未开始或学分已满，详情如下行：（无限循环抢课，如果学分已满请强制结束运行）")
                print(response_data)
        else:
            print("抢课请求遇到未知网络错误，详情如下，请截图反馈")
            print(response_data)


#
#
# def keep_websocket_heartbeat(url, custom_headers):
#     def on_message(ws, message):
#         print("Received message:", message)
#         # 在此处理接收到的消息，可以根据需要进行逻辑处理
#
#     def on_error(ws, error):
#         print("Error:", error)
#
#     def on_close(ws, close_status_code, close_msg):
#         print(f"Closed with status code {close_status_code}: {close_msg}")
#
#     def on_open(ws):
#         print("WebSocket connection opened.")
#         ws.send("ping")
#         while True:
#             # 这里可以加入心跳的逻辑
#             try:
#                 # 定期发送心跳消息
#                 ws.send("ping")
#             except Exception as e:
#                 print("Error sending heartbeat:", str(e))
#                 # 如果发送心跳失败，处理错误并继续
#
#     ws = websocket.WebSocketApp(url, header=custom_headers, on_message=on_message, on_error=on_error, on_close=on_close)
#     ws.on_open = on_open
#
#     # 运行WebSocket连接，此函数会持续运行直到手动关闭连接
#     ws.run_forever()
#




if __name__ == "__main__":
    key = "MWMqg2tPcDkxcm11"
    print("此程序为源星光子编写，通宵完成，为交流学习使用，请于下载后24小时内删除")
    Account = input("请输入账号: ")
    text = input("请输入密码: ")
    PS = encrypt(text, key)
    uuid = acq_PIN()
    PIN = input("请输入验证码: ")
    sid = input("请输入课程号（去掉括号,数字连起来，一共9位数字）: ")
    clazzId =f"202320241{sid}"
    lei = input("请输入课程所在的类别:（科技输入05，阅读18，生命19，历史22，艺术27，沟通41） ")
    page = input("请输入课程所在的页数:（单个数字） ")
    Authorization=login(Account, PS, PIN, uuid)
    time.sleep(1.0)
    user(Authorization)
    time.sleep(1.0)
    now2(Authorization)
    # # WebSocket URL
    # websocket_url = "ws://xkfw.xasyu.cn/xsxk/websocket/2021100374"
    #
    # # 自定义请求标头，根据您的需求进行修改
    # custom_headers = {
    #     "Host": "xkfw.xasyu.cn",
    #     "Connection": "Upgrade",
    #     "Pragma": "no-cache",
    #     "Cache-Control": "no-cache",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    #     "Upgrade": "websocket",
    #     "Origin": "http://xkfw.xasyu.cn",
    #     "Sec-WebSocket-Version": "13",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Accept-Language": "zh-CN,zh;q=0.9",
    #     # 添加其他标头根据需要
    # }
    #
    # keep_websocket_heartbeat(websocket_url, custom_headers)

    time.sleep(1.0)
    print("clazzId:",clazzId)
    print("lei:",lei)
    secretVal=listpost(Authorization,lei,clazzId,page)
    time.sleep(1.0)
    clazzpost(Authorization, clazzId, secretVal)


