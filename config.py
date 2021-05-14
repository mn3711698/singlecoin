# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################

# 注意,下边的dingding_token,wx_openid为空的话是不会发送钉钉消息和公众号消息

key = ""  # 币安API的key
secret = ""  # 币安API的secret
symbol = ""  # 交易对,目前公保证支持BTCUSDT,ETHUSDT这两个
trading_size = 0.003  # 下单量,至少要比最少值要大,注意控制风险 btc最小为0.001,eth最小为0.003
price_stop = 15  # 对比差价,持仓价加减这个值为self.stop_price,影响先浮亏后盈利的订单判断 测试时我用btc为50,eth为15
dingding_token = ""  # 钉钉webhook的access_token
wx_openid = ""  # 关注简道斋后发送openid得到的那一串字符就是这个

