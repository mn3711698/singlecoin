# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################

from datetime import datetime
from strategies.baseBTC import BaseBTC
from getaway.send_msg import dingding, wx_send_msg


class LineWithBTC(BaseBTC):

    def on_pos_data(self, pos_dict):
        # 先判断是否有仓位，如果是多头的仓位， 然后检查下是多头还是空头，设置相应的止损的价格..
        current_pos = float(pos_dict['positionAmt'])
        self.unRealizedProfit = float(pos_dict['unRealizedProfit'])
        entryPrice = float(pos_dict['entryPrice'])
        winPrice = entryPrice * 1.01  # 这个1.01是可修改的止盈参数，持仓价乘以1.01的值，当这个值大于当前价就止盈。
        if self.enter_price == 0 or self.enter_price != entryPrice:
            self.enter_price = entryPrice
            self.win_price = winPrice
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
                dingding(f"仓位检查:{self.symbol},交易所帐户仓位为:{current_pos},有持仓,系统仓位为:{self.pos},重置为:{current_pos}", symbols=self.symbol)
                self.pos = current_pos
                self.sync_data()
                return

    def on_ticker_data(self, ticker):
        self.ticker_data(ticker)

    def ticker_data(self, ticker):

        if self.symbol == ticker['symbol']:
            last_price = float(ticker['last_price'])  # 最新的价格.
            self.last_price = last_price

            if self.pos != 0:
                if self.high_price > 0:
                    self.high_price = max(self.high_price, self.last_price)
                if self.low_price > 0:
                    self.low_price = min(self.low_price, self.last_price)

            if self.pos == 0:  # 无持仓

                if self.order_flag > self.last_price > 0:
                    # 因为有一个止盈，在策略计算没有平仓信号的情况下平仓了，那遇到更低价的机会也不能错过
                    self.pos = self.round_to(self.trading_size, self.min_volume)
                    enter_price = self.ask
                    res_buy = self.buy(enter_price, abs(self.pos), mark=True)
                    self.enter_price = enter_price
                    self.high_price = enter_price
                    self.low_price = enter_price
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.pos_update_time = datetime.now()
                    self.sync_data()
                    HYJ_jd_first = f"回补仓位,交易对:{self.symbol},仓位:{self.pos}"
                    HYJ_jd_tradeType = "开多"
                    HYJ_jd_curAmount = f"{enter_price}"
                    HYJ_jd_remark = f"回补仓位,留意仓位"
                    self.dingding(f"开多交易所返回:{res_buy}", symbols=self.symbol)
                    self.wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.pos > 0:  # 多单持仓

                enter_price = self.bid2  # +1
                Profit = self.round_to((enter_price - self.enter_price) * abs(self.pos), self.min_price)
                if last_price > self.win_price > 0:  # 策略未出来平仓信号，有利润要止盈
                    res_sell = self.sell(enter_price, abs(self.pos), mark=True)
                    HYJ_jd_first = "止盈平多:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                        self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                    self.pos = 0
                    HYJ_jd_tradeType = "平多"
                    HYJ_jd_curAmount = "%s" % enter_price
                    HYJ_jd_remark = "止盈平多:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price, self.high_price, self.low_price)
                    self.enter_price = 0
                    self.high_price = 0
                    self.low_price = 0
                    self.maxunRealizedProfit = 0
                    self.unRealizedProfit = 0
                    self.lowProfit = 0
                    self.sync_data()
                    self.dingding(f"止盈平多,交易所返回:{res_sell}", symbols=self.symbol)
                    self.wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)