# -*- coding: utf-8 -*-

##############################################################################
# Author：QQ173782910
##############################################################################

import logging
from apscheduler.schedulers.background import BlockingScheduler
from utils.brokers import Broker
from getaway.binance_http import Interval, BinanceFutureHttp
from constant.constant import (EVENT_POS, EVENT_KLINE)
from utils.event import EventEngine, Event
from strategies.LineWithBTC import LineWithBTC
from config import key, secret, trading_size

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=format, filename='log_print.txt')
logger = logging.getLogger('print')
logging.getLogger("apscheduler").setLevel(logging.WARNING)  # 设置apscheduler.


class TradeRun:

    def __init__(self):
        self.trading_size = trading_size
        self.min_volume = 0.001
        self.key = key
        self.secret = secret
        self.symbol = "BTCUSDT"  # "YFIUSDT" 白嫖只提供这两个,单币运行
        self.kline_time = 0
        self.engine = EventEngine()
        self.broker = Broker(self.engine, self.key, secret=self.secret, symbol=self.symbol)
        self.initialization_data()
        self.broker.add_strategy(LineWithBTC, symbol=self.symbol, min_volume=self.min_volume)

    def initialization_data(self):

        binance_http = BinanceFutureHttp(key=self.key, secret=self.secret)
        einfo = binance_http.exchangeInfo()
        if isinstance(einfo, dict):
            esymbols = einfo['symbols']
            for i in esymbols:
                if i['symbol'] == self.symbol:
                    for j in i['filters']:
                        if j['filterType'] == 'LOT_SIZE':
                            minQty = float(j['minQty'])
                            if minQty > self.trading_size:
                                print('config.py里的trading_size太小')
                                raise ValueError("config.py里的trading_size太小")
                            self.min_volume = minQty

    def get_kline_data(self):

        data = self.broker.binance_http.get_kline(symbol=self.symbol, interval=Interval.MINUTE_5, limit=100)
        if len(data):
            kline_time = data[-1][0]
            if kline_time != self.kline_time:
                event = Event(EVENT_KLINE, {'symbol': self.symbol, "data": data, '_flag': ''})
                self.broker.event_engine.put(event)
                self.kline_time = kline_time

    def get_position(self):
        if self.symbol != '':
            info = self.broker.binance_http.get_position_info()
            if isinstance(info, list):
                for item in info:
                    symbol = item["symbol"]
                    if self.symbol == symbol:
                        event = Event(EVENT_POS, {"symbol": symbol, "pos": item})
                        self.broker.event_engine.put(event)


if __name__ == '__main__':
    minute_str = '0,5,10,15,20,25,30,35,40,45,50,55'
    RunTrade = TradeRun()
    scheduler = BlockingScheduler()  # 定时的任务.
    scheduler.add_job(RunTrade.get_kline_data, trigger='cron', id='TradeRunk', minute=minute_str, second='3')
    scheduler.add_job(RunTrade.get_position, trigger='cron', id='TradeRunp', second='*/1')  # 仓位
    scheduler.start()