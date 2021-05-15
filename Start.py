# -*- coding: utf-8 -*-

##############################################################################
# Author：QQ173782910
##############################################################################

import logging
from apscheduler.schedulers.background import BlockingScheduler
from RunUse import TradeRun
from config import key, secret, symbol, trading_size


format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=format, filename='log_print.txt')
logger = logging.getLogger('print')
logging.getLogger("apscheduler").setLevel(logging.WARNING)  # 设置apscheduler.


if __name__ == '__main__':
    RunTrade = TradeRun(key, secret, symbol, trading_size)
    scheduler = BlockingScheduler()  # 定时的任务.
    scheduler.add_job(RunTrade.get_kline_data, trigger='cron', second='*/2')
    scheduler.add_job(RunTrade.get_open_orders, trigger='cron', second='*/1')
    scheduler.add_job(RunTrade.get_position, trigger='cron', second='*/2')
    scheduler.start()