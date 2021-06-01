# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################

# 注意：
#    持仓方向为单向,不会设置杠杆
#    下边的dingding_token,wx_openid为空的话是不会发送钉钉消息和公众号消息
#    以下参数是以ethusdt为交易标的并且仓位为0.003来设定的，如果你的交易标的不是ethusdt或仓位不是0.003那请自行计算修改

version_flag = '20210601'

key = ""  # 币安API的key
secret = ""  # 币安API的secret
symbol = ""  # 交易对,目前公保证支持BTCUSDT,ETHUSDT这两个
dingding_token = ""  # 钉钉webhook的access_token
wx_openid = ""  # 关注简道斋后发送openid得到的那一串字符就是这个
trading_size = 0.003  # 下单量,至少要比币对最小值要大,注意控制风险 btc最小为0.001,eth最小为0.003,还要注意价值要大于5u
tick_flag = 3  # 请看strategies/LineWith.py文件的on_ticker_data，根据这个值的不同执行不同的处理，提供1,2,3选择，默认是3，其他值为自定义

place_order = 1  # 是否以五档价进行开仓,1为是,其他值为否,通常五档价会马上成交,如未成交则orders_seconds的秒后取消订单,这个参数我为0
orders_seconds = 240  # 当Place_order不为1时,这个值才会有明显效果,表示多少秒后取消订单

price_stop = 50  # 对比差价,持仓价加减这个值为self.stop_price,影响先浮亏后盈利的订单判断 测试时我用btc为90,eth为50(20210519更新)
tactics_flag = 1  # 此为机器人执行策略计算无信号是否发送钉钉消息，1为发送，不发送请留空或其他值
slOffset = 1.5  # on_pos_data里的self.slOffset，当你觉得winPoints值的利润足够了，那当最高(低)价格回撤本值就止盈
winPoints = 0.5  # on_pos_data里的self.winPoints,当你觉得这个利润已经足够了，那就止盈
times_flag = 0  # 亏损后加倍开单数，1开启，0或其他不开启，默认不开启
trend_price_stop = 95  # 20210519前的止损是以策略判断趋势是否反转来止损，发现这个不够精确，那么将增加这个参数，当亏损价差超过这个值，再趋势反转就止损。
difference_stop = 105  # 20210519增加固定止损价差价，当现价比持仓价相关这个值且亏损就平仓止损
strategy_flag = 2  # 使用的策略版本,目前有两个版本默认值为1,1为最原来策略，2为在1的基础上再减少开单量,其他值也为1
