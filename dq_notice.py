import json
import re
import requests
import os






#必须放到ql/scricp目录下，建议0 */2 * * *
#必填必填必填必填必填必填必填必填必填必填必填
#ip地址
ip = 'xxx.xxx.xxx.xxx:xxx'
#企业微信机器人的key
jqr_key = 'xxx-xxx-xxx-xxx-xxx'














s = requests.session()

current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
auth_path = father_path + '/config/auth.json'

with open(auth_path, 'r', encoding='utf-8') as f:
    auth = f.readlines()
auth = json.loads(auth[0])



header = {
    'Authorization': 'Bearer ' + auth['token']
}
datas = ''
count = 0
counts = 0
nums = 0


def vcbot(msg):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='+jqr_key
    data = {
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    s.post(url, json=data)


def dq_ck(cookie, remarks, status, ids, timestamp):
    usr_data = ''.join(re.findall(r"pt_pin=(.+?);", cookie))
    body = [ids]
    global count, counts
    url = "https://api.m.jd.com/client.action?functionId=friendListInitForFarm&body=%7B%22version%22%3A12%2C%22channel%22%3A1%7D&appid=wh5"
    header1 = {
        'charset': 'UTF-8',
        'accept-encoding': 'br,gzip,deflate',
        'user-agent': 'okhttp/3.12.1;jdmall;android;version/10.0.1;build/88405;screen/1080x2249;os/11;network/wifi;',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
    }
    try:
        res = s.get(url, headers=header1)
    except:
        msgs = "这个ck出现问题了：" + cookie
        print(msgs)
        vcbot(msgs)
    if 'not login' in res.text:
        count = count + 1
        counts = counts + 1
        try:
            if status == 1:
                status_msg = "已禁用" + '\n最后一次修改时间：\n' + timestamp + '\n\n\n'
            else:
                s.put("http://" + ip + "/api/envs/disable", json=body, headers=header)
                status_msg = "未操作,已标记禁用\n" + '最后一次修改时间：\n' + timestamp + '\n\n\n'
            datas = "备注：" + remarks + "的" + ''.join(
                usr_data) + "\n已过期\n当前状态" + status_msg
            print(datas)
            return datas
        except:
            msgs = "备注：" + remarks + "的" + ''.join(usr_data) + "账号有问题\n"
            print(msgs)
            return msgs
    else:
        if status == 1:
            s.put("http://" + ip + "/api/envs/enable", json=ids, headers=header)
            msgs = '用户' + remarks + '未过期但被禁用，已启动。\n' + '最后一次修改时间：\n' + timestamp + '\n\n\n'
            return msgs
    return ''


def get_ck():
    global datas, nums, count
    get_url = 'http://' + ip + '/api/envs'
    sssssss = s.get(get_url, headers=header)
    get_res = s.get(get_url, headers=header).json().get('data')
    print(sssssss.text)
    nums = len(get_res)
    for i in range(len(get_res)):
        try:
            datas = datas + dq_ck(get_res[i]['value'], get_res[i]['remarks'], get_res[i]['status'],
                                  get_res[i]['_id'], get_res[i]['timestamp'])
        except:
            datas = datas + dq_ck(get_res[i]['value'], '无备注', get_res[i]['status'],
                                  get_res[i]['_id'], get_res[i]['timestamp'])
        if count == 30:
            datas = '当前总ck数：' + str(nums) + '\n\n' + datas + '\n\n当前过期总个数：' + str(counts)
            vcbot(datas)
            datas = ''
            count = 0
    return datas


if __name__ == "__main__":
    msgs = get_ck()
    msg = '当前总ck数：' + str(nums) + '\n\n' + msgs + '\n\n当前过期总个数：' + str(counts)
    vcbot(msg)
