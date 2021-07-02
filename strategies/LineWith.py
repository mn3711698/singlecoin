# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################

from datetime import datetime
from strategies import Base
from getaway.send_msg import dingding, wx_send_msg


class LineWith(Base):

    def on_pos_data(self, pos_dict):
        # 先判断是否有仓位，如果是多头的仓位， 然后检查下是多头还是空头，设置相应的止损的价格..
        current_pos = float(pos_dict['positionAmt'])
        self.unRealizedProfit = float(pos_dict['unRealizedProfit'])
        entryPrice = float(pos_dict['entryPrice'])
        if self.enter_price == 0 or self.enter_price != entryPrice:
            self.enter_price = entryPrice
            if current_pos > 0:
                self.stoploss_price = entryPrice * (1 - self.stoploss)
                self.takeprofit_price = entryPrice * (1 + self.takeprofit)
            elif current_pos < 0:
                self.stoploss_price = entryPrice * (1 + self.stoploss)
                self.takeprofit_price = entryPrice * (1 - self.takeprofit)
        if self.pos != 0:
            if self.unRealizedProfit > 0:
                self.maxunRealizedProfit = max(self.maxunRealizedProfit, self.unRealizedProfit)
            elif self.unRealizedProfit < 0:
                self.lowProfit = min(self.lowProfit, self.unRealizedProfit)

        if self.pos != current_pos:  # 检查仓位是否是一一样的.

            if current_pos == 0:
                dingding(f"仓位检查:{self.symbol},交易所帐户仓位为0，无持仓，系统仓位为:{self.pos},重置为0", symbols=self.symbol)
                self.pos = 0
                self.sync_data()
                return
            elif current_pos != 0:
                if self.HYJ_jd_ss != 0:
                    self.HYJ_jd_ss = 0
                dingding(f"仓位检查:{self.symbol},交易所帐户仓位为:{current_pos},有持仓,系统仓位为:{self.pos},重置为:{current_pos}", symbols=self.symbol)
                self.pos = current_pos
                self.sync_data()
                return

    def on_ticker_data(self, ticker):

        if self.symbol == "BNBUSDT":
            self.ticker_data_BNB(ticker)  # 适用BNB
        elif self.symbol == "ETHUSDT":
            self.ticker_data_ETH(ticker)  # 适用ETH 注意这个还没有处理好

    def ticker_data_ETH(self, ticker):  # 请参考其他三个写自己的(这里的代码与ticker_data_two比少了固定止损处理)

        if self.symbol == ticker['symbol']:
            last_price = float(ticker['last_price'])  # 最新的价格.
            self.last_price = last_price

            if self.pos != 0:
                if self.high_price > 0.0:
                    self.high_price = max(self.high_price, self.last_price)
                if self.low_price > 0.0:
                    self.low_price = min(self.low_price, self.last_price)

            if self.pos == 0:  # 无持仓

                if self.HYJ_jd_ss == 1:  # 策略计算出来是开多信号
                    pos = self.trading_size
                    self.pos = self.round_to(pos, self.min_volume)
                    enter_price = self.ask
                    res_buy = self.buy(enter_price, abs(self.pos))
                    self.HYJ_jd_ss = 0
                    self.enter_price = enter_price
                    self.stoploss_price = enter_price * (1 - self.stoploss)
                    self.takeprofit_price = enter_price * (1 + self.takeprofit)
                    self.high_price = enter_price
                    self.low_price = enter_price
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.pos_update_time = datetime.now()
                    self.sync_data()
                    HYJ_jd_first = f"交易对:{self.symbol},仓位:{self.pos}"
                    HYJ_jd_tradeType = "开多"
                    HYJ_jd_curAmount = f"{enter_price}"
                    HYJ_jd_remark = f"最新价:{self.last_price}"
                    dingding(f"开多交易所返回:{res_buy}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.HYJ_jd_ss == -1:  # 策略计算出来是开空信号
                    pos = self.trading_size
                    self.pos = self.round_to(pos, self.min_volume)
                    enter_price = self.bid

                    res_sell = self.sell(enter_price, abs(self.pos))
                    self.HYJ_jd_ss = 0
                    self.pos = -self.pos
                    self.enter_price = enter_price
                    self.stoploss_price = enter_price * (1 + self.stoploss)
                    self.takeprofit_price = enter_price * (1 - self.takeprofit)
                    self.high_price = enter_price
                    self.low_price = enter_price
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.pos_update_time = datetime.now()
                    self.sync_data()
                    HYJ_jd_first = f"交易对:{self.symbol},仓位:{self.pos}"
                    HYJ_jd_tradeType = "开空"
                    HYJ_jd_curAmount = f"{enter_price}"
                    HYJ_jd_remark = f"最新价:{self.last_price}"
                    dingding(f"开空交易所返回:{res_sell}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.pos > 0:  # 多单持仓，目前止损是以 HYJ_jd_ss = 11,如有需要其他的止损请在下边增加自己的代码

                enter_price = self.bid2  # +1
                Profit = self.round_to((enter_price - self.enter_price) * abs(self.pos), self.min_price)

                if self.HYJ_jd_ss == 11:  # self.HYJ_jd_ss = 11 是趋势反转了
                    res_sell = self.sell(enter_price, abs(self.pos))
                    self.HYJ_jd_ss = 0
                    if Profit < 0:
                        self.times += 1  # 这个是亏损后加倍开单计数
                    self.stop_price = 0
                    HYJ_jd_first = "趋势反转平多:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_tradeType = "平多"
                    HYJ_jd_curAmount = "%s" % enter_price
                    HYJ_jd_remark = "趋势反转平多:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"趋势反转平多,交易所返回:{res_sell}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.last_price < self.stoploss_price:
                    res_sell = self.sell(enter_price, abs(self.pos))
                    self.HYJ_jd_ss = 0
                    if Profit < 0:
                        self.times += 1  # 这个是亏损后加倍开单计数
                    self.stop_price = 0
                    HYJ_jd_first = "止损平多:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_tradeType = "止损平多"
                    HYJ_jd_curAmount = "%s" % enter_price
                    HYJ_jd_remark = "止损平多:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"止损平多,交易所返回:{res_sell}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.takeprofit_price != 0 and self.last_price > self.takeprofit_price:

                    res_sell = self.sell(enter_price, abs(self.pos))
                    self.HYJ_jd_ss = 0
                    HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_remark = "净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.stop_price = 0
                    HYJ_jd_tradeType = "平多"
                    HYJ_jd_curAmount = "%s" % enter_price
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"多单,止盈,交易所返回:{res_sell}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.pos < 0:  # 空单持仓，目前止损是以 HYJ_jd_ss = -11,如有需要其他的止损请在下边增加自己的代码

                enter_price = self.ask2
                Profit = self.round_to((self.enter_price - enter_price) * abs(self.pos), self.min_price)

                if self.HYJ_jd_ss == -11:
                    self.stop_price = 0
                    res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                    self.HYJ_jd_ss = 0
                    if Profit < 0:
                        self.times += 1  # 这个是亏损后加倍开单计数
                    HYJ_jd_first = "趋势反转平空:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_remark = "趋势反转平空:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    HYJ_jd_tradeType = "平空"
                    HYJ_jd_curAmount = "%s" % self.enter_price
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"趋势反转平空,交易所返回:{res_sell}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.stoploss_price != 0 and self.last_price > self.stoploss_price:

                    self.stop_price = 0
                    res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                    self.HYJ_jd_ss = 0
                    if Profit < 0:
                        self.times += 1  # 这个是亏损后加倍开单计数
                    HYJ_jd_first = "止损平空:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_remark = "止损:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    HYJ_jd_tradeType = "平空"
                    HYJ_jd_curAmount = "%s" % self.enter_price
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"止损平空,交易所返回:{res_sell}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.takeprofit_price > self.last_price:

                    res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                    self.HYJ_jd_ss = 0
                    HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_tradeType = "平空"
                    HYJ_jd_curAmount = "%s" % self.enter_price
                    HYJ_jd_remark = "净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.stop_price = 0
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"空单,止盈,交易所返回:{res_sell}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

    def ticker_data_BNB(self, ticker):

        if self.symbol == ticker['symbol']:
            last_price = float(ticker['last_price'])  # 最新的价格.
            self.last_price = last_price

            if self.pos != 0:
                if self.high_price > 0:
                    self.high_price = max(self.high_price, self.last_price)
                if self.low_price > 0:
                    self.low_price = min(self.low_price, self.last_price)

            if self.pos == 0:  # 无持仓

                if self.HYJ_jd_ss == 1:  # 策略计算出来是开多信号
                    self.HYJ_jd_ss = 0
                    pos = self.trading_size
                    # if self.times_flag == 1 and self.times != 0:  # 进行加倍开单
                    #     pos = pos + 0.01 * self.times
                    self.pos = self.round_to(pos, self.min_volume)
                    enter_price = self.ask
                    res_buy = self.buy(enter_price, abs(self.pos))
                    self.enter_price = enter_price
                    self.stoploss_price = enter_price * (1 - self.stoploss)
                    self.takeprofit_price = enter_price * (1 + self.takeprofit)
                    self.high_price = enter_price
                    self.low_price = enter_price
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.pos_update_time = datetime.now()
                    self.sync_data()
                    HYJ_jd_first = f"交易对:{self.symbol},仓位:{self.pos}"
                    HYJ_jd_tradeType = "开多"
                    HYJ_jd_curAmount = f"{enter_price}"
                    HYJ_jd_remark = f"最新价:{self.last_price}"
                    dingding(f"开多交易所返回:{res_buy}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.HYJ_jd_ss == -1:  # 策略计算出来是开空信号
                    self.HYJ_jd_ss = 0
                    pos = self.trading_size
                    # if self.times_flag == 1 and self.times != 0:  # 进行加倍开单
                    #     pos = pos + 0.01 * self.times
                    self.pos = self.round_to(pos, self.min_volume)
                    enter_price = self.bid

                    res_sell = self.sell(enter_price, abs(self.pos))
                    self.pos = -self.pos
                    self.enter_price = enter_price
                    self.stoploss_price = enter_price * (1 + self.stoploss)
                    self.takeprofit_price = enter_price * (1 - self.takeprofit)
                    self.high_price = enter_price
                    self.low_price = enter_price
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.pos_update_time = datetime.now()
                    self.sync_data()
                    HYJ_jd_first = f"交易对:{self.symbol},仓位:{self.pos}"
                    HYJ_jd_tradeType = "开空"
                    HYJ_jd_curAmount = f"{enter_price}"
                    HYJ_jd_remark = f"最新价:{self.last_price}"
                    dingding(f"开空交易所返回:{res_sell}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.pos > 0:  # 多单持仓，目前止损是以 HYJ_jd_ss = 11,如有需要其他的止损请在下边增加自己的代码

                enter_price = self.bid2  # +1
                Profit = self.round_to((enter_price - self.enter_price) * abs(self.pos), self.min_price)

                if self.HYJ_jd_ss == 11:  # self.HYJ_jd_ss = 11 是趋势反转了
                    res_sell = self.sell(enter_price, abs(self.pos))
                    self.HYJ_jd_ss = 0
                    if Profit < 0:
                        self.times += 1  # 这个是连续亏损计数
                    else:
                        self.times = 0
                    self.stop_price = 0
                    HYJ_jd_first = "趋势反转平多:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_tradeType = "平多"
                    HYJ_jd_curAmount = "%s" % enter_price
                    HYJ_jd_remark = "趋势反转平多:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"趋势反转平多,交易所返回:{res_sell}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.last_price < self.stoploss_price:
                    res_sell = self.sell(enter_price, abs(self.pos))
                    self.HYJ_jd_ss = 0

                    self.times += 1  # 这个是连续亏损计数
                    self.stop_price = 0
                    HYJ_jd_first = "止损平多:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_tradeType = "止损平多"
                    HYJ_jd_curAmount = "%s" % enter_price
                    HYJ_jd_remark = "止损平多:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"止损平多,交易所返回:{res_sell}")
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.times > 2 and self.maxunRealizedProfit > 0.03 and self.high_price - self.last_price > 0.5:  # 当连续亏损超过2次
                    res_sell = self.sell(enter_price, abs(self.pos))
                    self.HYJ_jd_ss = 0
                    HYJ_jd_first = "止盈A:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_remark = "净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.times = 0
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.stop_price = 0
                    HYJ_jd_tradeType = "平多"
                    HYJ_jd_curAmount = "%s" % enter_price
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"多单,止盈A,交易所返回:{res_sell}")
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.takeprofit_price != 0 and self.last_price > self.takeprofit_price:

                    res_sell = self.sell(enter_price, abs(self.pos))
                    self.HYJ_jd_ss = 0
                    HYJ_jd_first = "止盈B:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_remark = "净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.times = 0
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.stop_price = 0
                    HYJ_jd_tradeType = "平多"
                    HYJ_jd_curAmount = "%s" % enter_price
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"多单,止盈B,交易所返回:{res_sell}")
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.pos < 0:  # 空单持仓
                enter_price = self.ask2
                Profit = self.round_to((self.enter_price - enter_price) * abs(self.pos), self.min_price)

                if self.HYJ_jd_ss == -11:
                    self.stop_price = 0
                    res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                    self.HYJ_jd_ss = 0
                    if Profit < 0:
                        self.times += 1  # 这个是连续亏损计数
                    else:
                        self.times = 0
                    HYJ_jd_first = "趋势反转平空:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_remark = "趋势反转平空:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    HYJ_jd_tradeType = "平空"
                    HYJ_jd_curAmount = "%s" % self.enter_price
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"趋势反转平空,交易所返回:{res_sell}", symbols=self.symbol)
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.stoploss_price != 0 and self.last_price > self.stoploss_price:

                    self.stop_price = 0
                    res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                    self.HYJ_jd_ss = 0
                    self.times += 1  # 这个是连续亏损计数

                    HYJ_jd_first = "止损平空:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_remark = "止损:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    HYJ_jd_tradeType = "平空"
                    HYJ_jd_curAmount = "%s" % self.enter_price
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"止损平空,交易所返回:{res_sell}")
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.times > 2 and self.maxunRealizedProfit > 0.03 and self.last_price - self.low_price > 0.5:  # 当连续亏损超过2次
                    res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                    self.HYJ_jd_ss = 0
                    HYJ_jd_first = "止盈A:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_tradeType = "平空"
                    HYJ_jd_curAmount = "%s" % self.enter_price
                    HYJ_jd_remark = "净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.times = 0
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.stop_price = 0
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"空单,止盈A,交易所返回:{res_sell}")
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.takeprofit_price > self.last_price:

                    res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                    self.HYJ_jd_ss = 0
                    HYJ_jd_first = "止盈B:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_tradeType = "平空"
                    HYJ_jd_curAmount = "%s" % self.enter_price
                    HYJ_jd_remark = "净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.times = 0
                    self.stoploss_price = 0
                    self.takeprofit_price = 0
                    self.stop_price = 0
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    dingding(f"空单,止盈B,交易所返回:{res_sell}")
                    wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)
