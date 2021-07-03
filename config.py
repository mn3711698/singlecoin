# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################

# 注意：
#    持仓方向为单向,不会设置杠杆
#    下边的dingding_token,wx_openid为空的话是不会发送钉钉消息和公众号消息

version_flag = '20210703'

key = ""  # 币安API的key
secret = ""  # 币安API的secret
symbol = "BNBUSDT"  # 交易对,目前保证支持BNBUSDT,ETHUSDT这两个
trading_size = 0.02  # 下单量,至少要比币对最小值要大,注意控制风险 eth最小为0.003,BNB:0.02 还要注意价值要大于5u

dingding_token = ""  # 钉钉webhook的access_token
wx_openid = ""  # 关注简道斋后发送openid得到的那一串字符就是这个

tactics_flag = 1  # 此为机器人执行策略计算无信号是否发送钉钉消息，约15分钟发送一次，1为发送，不发送请留空或其他值

orders_seconds = 0  # 预留

stoploss = 8 / 100  # eth,bnb,止损百分比 持仓价涨跌这个值止损
takeprofit = 2.328 / 100  # etn,止盈百分比  持仓价涨跌这个值止盈
line_poor = 0.04  # 计算参数bnb:15min:0.626/0.38/0.04,5min:0.36,eth:5.2,其他未知
line_poor_stop = 0.05  # 计算参数bnb:15min:0.5/0.2/0.05,5min:0.4,eth:15min:6.22,其他未知
