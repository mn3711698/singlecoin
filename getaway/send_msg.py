import json
import requests
import traceback
import time
from config import dingding_token, wx_openid, symbol


def dingding(msg, symbols=''):
    if dingding_token == '':
        return

    if symbols == '':
        symbols = symbol

    webhook = "https://oapi.dingtalk.com/robot/send?access_token=%s"%dingding_token
    headers = {"Content-Type": "application/json", "Charset": "UTF-8"}
    message = {
        "msgtype": "text",
        "text": {"content": "%s提醒%s:%s"%(getToday(9), symbols, msg)},
        "at": {"isAtall": False}
    }
    try:
        message_json = json.dumps(message)
        _http = requests.Session()
        info = _http.post(url=webhook, data=message_json.encode('utf-8'), headers=headers)
    except:
        bugcode(traceback, ctype='singlecoin_dingding')


def getToday(format=3):
    """返回今天的日期字串"""
    t = time.time()
    date_ary = time.localtime(t)
    if format == 1:
        x = time.strftime("%Y%m%d", date_ary)
    elif format == 2:
        x = time.strftime("%H:%M", date_ary)
    elif format == 3:
        x = time.strftime("%Y/%m/%d", date_ary)
    elif format == 4:
        x = time.strftime("%Y/%m/%d %H:%M", date_ary)
    elif format == 5:
        x = time.strftime("%y%m%d", date_ary)
    elif format == 6:
        x = time.strftime("%Y-%m-%d", date_ary)
    elif format == 7:
        x = time.strftime("%Y/%m/%d %H:%M:%S", date_ary)
    elif format == 8:
        x = time.strftime("%Y-%m-%d %H:%M", date_ary)
    elif format == 9:
        x = time.strftime("%Y-%m-%d %H:%M:%S", date_ary)
    elif format == 10:
        x = time.strftime("%Y年%m月%d日 %H:%M", date_ary)
    else:
        x = time.strftime("%Y-%m-%d %H:%M:%S", date_ary)
    return x


def bugcode(traceback, ctype = 'ok'):

    if ctype != 'ok':
        errInf = str(traceback.format_exc())
    else:
        errInf = traceback

    gUrl = 'https://link.yjyzj.cn/api'
    pdata = {'viewid': 'home', 'part': 'collect',
             'ctype': ctype, 'errInf': errInf,'title': 'singlecoin'}
    try:
        _http = requests.Session()
        r = _http.post(gUrl, data=pdata)
    except:
        pass


def wx_send_msg(first, tradeType, curAmount, remark):
    if wx_openid == '':
        return
    data = {"sendId": wx_openid,
            "first": first,  # 第一行的内容
            "tradeType": tradeType,  # 交易类型的内容
            "curAmount": curAmount,  # 交易金额的内容
            "remark": remark,  # 备注的内容
          }

    gUrl = 'https://yjyzj.cn/stockwx'
    try:
        _http = requests.Session()
        r = _http.post(gUrl, data=data)
    except:
        bugcode(traceback, ctype='singlecoin_wx_send_msg')