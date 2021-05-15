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
                self.stop_price = entryPrice - self.price_stop
            elif current_pos < 0:
                self.stop_price = entryPrice + self.price_stop
        if self.pos != 0:
            if self.unRealizedProfit > 0:
                self.maxunRealizedProfit = max(self.maxunRealizedProfit, self.unRealizedProfit)
            elif self.unRealizedProfit < 0:
                self.lowProfit = min(self.lowProfit, self.unRealizedProfit)

        if self.pos != current_pos:  # 检查仓位是否是一一样的.

            if current_pos == 0:
                dingding(f"仓位检查:{self.symbol},交易所帐户仓位为0，无持仓，系统仓位为:{self.pos},重置为0")
                self.pos = 0
                self.sync_data()
                return
            elif current_pos != 0:
                dingding(f"仓位检查:{self.symbol},交易所帐户仓位为:{current_pos},有持仓,系统仓位为:{self.pos},重置为:{current_pos}")
                self.pos = current_pos
                self.sync_data()
                return

        if self.unRealizedProfit > self.winPoints:  # 有利润，要平仓
            if self.pos > 0 and self.high_price - self.last_price > self.slOffset:  # 多单,回撤超过slOffset
                enter_price = self.bid2  # +1
                res_sell = self.sell(enter_price, abs(self.pos))  # 平多
                HYJ_jd_first = "多单止盈平仓:交易对:%s,当前利润:%s,最大利润:%s,最大亏损:%s" % (
                    self.symbol, self.unRealizedProfit, self.maxunRealizedProfit, self.lowProfit)
                HYJ_jd_tradeType = "平多"
                HYJ_jd_curAmount = "%s" % self.enter_price
                self.stop_price = 0
                Profit = self.round_to((enter_price - self.enter_price) * abs(self.pos), self.min_price)
                HYJ_jd_remark = "winPoints止盈,净利润:%s,当前价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.pos = 0
                self.times = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"多单winPoints止盈交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.pos < 0 and self.last_price - self.low_price > self.slOffset:  # 空单,回撤超过slOffset

                enter_price = self.ask2  # +1
                res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                self.stop_price = 0
                HYJ_jd_first = "空单止盈平仓:交易对:%s,当前利润:%s,最大利润:%s,最大亏损:%s" % (
                    self.symbol, self.unRealizedProfit, self.maxunRealizedProfit, self.lowProfit)
                HYJ_jd_tradeType = "平空"
                HYJ_jd_curAmount = "%s" % self.enter_price
                Profit = self.round_to((self.enter_price - enter_price) * abs(self.pos), self.min_price)
                HYJ_jd_remark = "winPoints止盈,净利润:%s,当前价:%s,最高价:%s,最低价:%s" % (
                Profit, self.last_price, self.high_price, self.low_price)
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.times = 0
                self.pos = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"空单winPoints止盈交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)
        else:
            self.sync_data()

    def on_ticker_data(self, ticker):

        if self.symbol == ticker['symbol']:
            last_price = ticker['last_price']  # 最新的价格.
            self.last_price = float(last_price)

        if self.pos != 0:
            if self.high_price > 0:
                self.high_price = max(self.high_price, self.last_price)
            if self.low_price > 0:
                self.low_price = min(self.low_price, self.last_price)

        if self.pos == 0:

            if self.HYJ_jd_ss == 1:

                self.HYJ_jd_ss = 0
                pos = self.trading_size
                self.pos = self.round_to(pos, self.min_volume)
                enter_price = self.ask  # -1
                res_buy = self.buy(enter_price, abs(self.pos))
                self.enter_price = enter_price
                self.stop_price = enter_price - self.price_stop
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
                dingding(f"开多交易所返回:{res_buy}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.HYJ_jd_ss == -1:

                self.HYJ_jd_ss = 0
                pos = self.trading_size
                self.pos = self.round_to(pos, self.min_volume)
                enter_price = self.bid  # -1
                res_sell = self.sell(enter_price, abs(self.pos))
                self.pos = -self.pos
                self.enter_price = enter_price
                self.stop_price = enter_price + self.price_stop
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
                dingding(f"开空交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

        elif self.pos > 0:

            enter_price = self.bid2  # +1
            Profit = self.round_to((enter_price - self.enter_price) * abs(self.pos), self.min_price)

            if self.HYJ_jd_ss == 11:

                res_sell = self.sell(enter_price, abs(self.pos))
                self.HYJ_jd_ss = 0
                self.stop_price = 0
                HYJ_jd_first = "规则平多:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_tradeType = "平多"
                HYJ_jd_curAmount = "%s" % enter_price
                HYJ_jd_remark = "盈损:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"规则平多,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 40 and self.high_price - self.last_price > 4:

                res_sell = self.sell(enter_price, abs(self.pos))
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_remark = "A:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
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
                dingding(f"多单,A止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 35 and self.high_price - self.last_price > 3.35:

                res_sell = self.sell(enter_price, abs(self.pos))
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_remark = "B:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
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
                dingding(f"多单,B止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 30 and self.high_price - self.last_price > 2.6:

                res_sell = self.sell(enter_price, abs(self.pos))
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_remark = "C:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
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
                dingding(f"多单,C止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 25 and self.high_price - self.last_price > 1.95:

                res_sell = self.sell(enter_price, abs(self.pos))
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_remark = "D:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
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
                dingding(f"多单,D止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 20 and self.high_price - self.last_price > 1.4:

                res_sell = self.sell(enter_price, abs(self.pos))
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_remark = "E:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
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
                dingding(f"多单,E止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 15 and self.high_price - self.last_price > 0.95:

                res_sell = self.sell(enter_price, abs(self.pos))
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_remark = "F:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
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
                dingding(f"多单,F止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 10 and self.high_price - self.last_price > 0.6:

                res_sell = self.sell(enter_price, abs(self.pos))
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_remark = "G:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
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
                dingding(f"多单,G止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.unRealizedProfit > 0 and Profit > self.trading_size * 5 \
                    and self.high_price - self.last_price > 3 and self.stop_price <= self.low_price:

                res_sell = self.sell(enter_price, abs(self.pos))
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_remark = "H:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
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
                dingding(f"多单,H止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

        elif self.pos < 0:

            enter_price = self.ask2
            Profit = self.round_to((self.enter_price - enter_price) * abs(self.pos), self.min_price)

            if self.HYJ_jd_ss == -11:

                self.stop_price = 0
                res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "规则平空:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_remark = "盈损:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                HYJ_jd_tradeType = "平空"
                HYJ_jd_curAmount = "%s" % self.enter_price
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"规则平空,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 40 and self.last_price - self.low_price > 4:

                res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_tradeType = "平空"
                HYJ_jd_curAmount = "%s" % self.enter_price
                HYJ_jd_remark = "A:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                self.stop_price = 0
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"空单,A止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 35 and self.last_price - self.low_price > 3.35:

                res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_tradeType = "平空"
                HYJ_jd_curAmount = "%s" % self.enter_price
                HYJ_jd_remark = "B:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                self.stop_price = 0
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"空单,B止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 30 and self.last_price - self.low_price > 2.6:

                res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_tradeType = "平空"
                HYJ_jd_curAmount = "%s" % self.enter_price
                HYJ_jd_remark = "C:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                self.stop_price = 0
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"空单,C止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 25 and self.last_price - self.low_price > 1.95:

                res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_tradeType = "平空"
                HYJ_jd_curAmount = "%s" % self.enter_price
                HYJ_jd_remark = "D:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                self.stop_price = 0
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"空单,D止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 20 and self.last_price - self.low_price > 1.4:

                res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_tradeType = "平空"
                HYJ_jd_curAmount = "%s" % self.enter_price
                HYJ_jd_remark = "E:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                self.stop_price = 0
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"空单,E止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 15 and self.last_price - self.low_price > 0.95:

                res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_tradeType = "平空"
                HYJ_jd_curAmount = "%s" % self.enter_price
                HYJ_jd_remark = "F:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                self.stop_price = 0
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"空单,F止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.maxunRealizedProfit > self.trading_size * 10 and self.last_price - self.low_price > 0.6:

                res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_tradeType = "平空"
                HYJ_jd_curAmount = "%s" % self.enter_price
                HYJ_jd_remark = "G:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                self.stop_price = 0
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"空单,G止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

            elif self.unRealizedProfit > 0 and Profit > self.trading_size * 5 \
                    and self.last_price - self.low_price > 3 and self.stop_price <= self.high_price:

                res_sell = self.buy(enter_price, abs(self.pos))  # 平空
                self.HYJ_jd_ss = 0
                HYJ_jd_first = "止盈:交易对:%s,最大亏损:%s,最大利润:%s,当前利润:%s,仓位:%s" % (
                    self.symbol, self.lowProfit, self.maxunRealizedProfit, self.unRealizedProfit, self.pos)
                self.pos = 0
                HYJ_jd_tradeType = "平空"
                HYJ_jd_curAmount = "%s" % self.enter_price
                HYJ_jd_remark = "H:净利:%s,最新价:%s,最高价:%s,最低价:%s" % (
                    Profit, self.last_price, self.high_price, self.low_price)
                self.stop_price = 0
                self.enter_price = 0
                self.high_price = 0
                self.low_price = 0
                self.maxunRealizedProfit = 0
                self.unRealizedProfit = 0
                self.lowProfit = 0
                self.sync_data()
                dingding(f"空单,H止盈,交易所返回:{res_sell}")
                wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)
