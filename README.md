# singlecoin(支持windows+linux,交易所目前只支持币安,目前只支持单币运行)

## 目前只支持BNB,ETH。非开源，慎用!

# 策略计算及下单平仓条件说明

两条移动线，对比两个线的值。在配置里line_poor,line_poor_stop,两个参数。当两个移动线的值相差大于line_poor，表示趋势明显向下或向上，要下单，当两个值小于line_poor_stop，表示很小的震荡或者趋势不明显，平仓。

已经在跑机器人，钉钉消息有几个值old_wave,Raw,Wave,Raw - wave。当Wave大于old_wave是趋势向上，反之趋势向下，Raw和Wave是两个移动线的值，Raw比Wave大是向上，反之向下，Raw - wave的绝对值大于line_poor就开仓，小于line_poor_stop就平仓。趋势相反了也平仓。

开仓：Wave大于old_wave且Raw - wave的绝对值大于line_poor开多,Wave不大于old_wave且Raw - wave的绝对值大于line_poor开空.

平仓:多单，Wave不大于old_wave或Raw - wave小于line_poor_stop平仓;空单,Wave大于old_wave或Raw - wave小于line_poor_stop平空.

因为用tradingview回测，没看到平仓条件且还达到下单条件马上下单的效果，所以平仓后要跟完一根K线再判断是不是要下单。不会平仓的同时马上反方向下单。

# tradingview回测最优配置(bnb0.02,eth0.003),这里每几天进行一次对比记录，方便参考

## ETH:
    2021-7-6 
        line_poor=0.38,line_poor_stop=0.2(净利润24.79%，胜率40.74%);  
        line_poor=0.626,line_poor_stop=0.5(净利润29.39%，胜率40.78%);
        
    2021-7-5 
        line_poor=0.38,line_poor_stop=0.2(净利润25.17%，胜率40.9%);  
        line_poor=0.626,line_poor_stop=0.5(净利润29.69%，胜率41.05%);

## BNB:

    2021-7-6 
        line_poor=0.38,line_poor_stop=0.2(净利润23.92%，胜率42.35%);  
        line_poor=0.04,line_poor_stop=0.05(净利润38.7%，胜率42.14%);
        line_poor=0.04,line_poor_stop=0.048(净利润38.85%，胜率41.93%);
        line_poor=0.053,line_poor_stop=0.048(净利润39.24%，胜率41.97%);
        
    2021-7-5 
        line_poor=0.38,line_poor_stop=0.2(净利润25.23%，胜率42.59%);  
        line_poor=0.04,line_poor_stop=0.05(净利润39.19%，胜率42.42%);
        line_poor=0.04,line_poor_stop=0.048(净利润39.83%，胜率42.25%);
        line_poor=0.053,line_poor_stop=0.048(净利润40.22%，胜率42.29%);
        
## 有开发能力，如有在不泄漏策略代码并能对策略进行使用或者回测方案的可以联系我。（注：同一币种，同一配置参数，同一时间周期开仓及平仓的时机所有人一样）

## 以下为策略在tradingview采用15min线进行的回测
BNB仓位0.02每单
![](https://github.com/mn3711698/singlecoin/blob/main/BNB0.02.png)
BNB仓位1每单
![](https://github.com/mn3711698/singlecoin/blob/main/BNB1.png)
ETH仓位0.003每单
![](https://github.com/mn3711698/singlecoin/blob/main/ETH0.003.png)
ETH仓位1每单
![](https://github.com/mn3711698/singlecoin/blob/main/ETH1.png)
BNB参数跑ETH仓位1每单
![](https://github.com/mn3711698/singlecoin/blob/main/BNB1TOETH1.png)

BNB仓位0.02每单最新
![](https://github.com/mn3711698/singlecoin/blob/main/BNBnew.png)

ETH仓位0.003每单最新
![](https://github.com/mn3711698/singlecoin/blob/main/eth20210726.png)
## 本项目只是提供代码，不对使用者因使用本代码实际产生的盈亏负责。不要跟我说开源，我从来就没有想过要开源，只是开放使用。

## 可以自行设置计算止盈的配置参数及修改止损配置

# 注意(白嫖更要注意安全，因为核心代码没有开源，大家慎用)

## API的权限只需要有交易权限就够了，不要开提币权限,还要限制ip！

## API的权限只需要有交易权限就够了，不要开提币权限,还要限制ip！

## API的权限只需要有交易权限就够了，不要开提币权限,还要限制ip！

# 需要准备云主机，windows支持64位的python,3.8或3.7,linux系统支持python3.6

# 需要网络可以访问币安交易所，否则机器人无法使用

## windows使用说明(路径写死了)
下载本项目代码压缩包，放在C盘根目录下，解压，最终代码在C:\singlecoin\下。如果是git下载，也请代码放在C:\singlecoin\下，建议使用git下载，方便后续更新

先下载https://download.microsoft.com/download/5/f/7/5f7acaeb-8363-451f-9425-68a90f98b238/visualcppbuildtools_full.exe
安装时，直接下一步，不需要选择其他的。

安装相关库(只支持python3)  pip3 install -r requirements.txt 或 pip install -r requirements.txt

填好config.py里边的配置项，确认python是不是64版本，如果使用的是python3.7要将RunUse里的TradeRun_w37.pyd重命名为TradeRun.pyd，
strategies下的base_w37.pyd重命名为base.pyd,
如果使用的是python3.8要将RunUse里的TradeRun_w38.pyd重命名为TradeRun.pyd,strategies下的base_w38.pyd重命名为base.pyd

到此，准备工作做好。在项目目录C:\singlecoin\下执行python3 Start.py,就可以躺着赚钱了

相关持仓及订单信息请看币安的网页或者APP对应的交易对下的数据。

如果后续有更新代码，可以直接git下载就好了。下载好后，关掉cdm窗口，重新打开窗口执行python3 Start.py就好了

注意:持仓方向是单向(双向持仓要改为单向否则无法下单)，杠杆是交易所默认未进行另外设定
## linux使用说明(路径写死了)
下载本项目代码压缩包，放在/var/games/目录下，解压，最终代码在/var/games/singlecoin/下。

如果是git下载，也请代码放在/var/games/singlecoin/下，建议使用git下载，方便后续更新

安装相关库(只支持python3)  pip3 install -r requirements.txt 或 pip install -r requirements.txt

填好config.py里边的配置项，确认python版本为python3.6，
要将RunUse里的TradeRun_l36.so重命名为TradeRun.so,strategies下的base_l36.so重命名为base.so

到此所有准备工作都做好了。在项目目录/var/games/singlecoin/下执行python3 Start.py 或python Start.py ,就可以躺着赚钱了

相关持仓及订单信息请看币安的网页或者APP对应的交易对下的数据。

建议使用Supervisor启动

如果后续有更新代码，可以直接git下载就好了。重新执行python3 Start.py就好了

注意:持仓方向是单向(双向持仓要改为单向否则无法下单)，杠杆是交易所默认未进行另外设定

## 关于代码更新说明
建议使用git命令来下载，这样更新就不影响。

# 更新日志

2021-07-08 优化多空不同处理参数(注释价格回撤止盈,可自行开启)

2021-07-05 优化取消订单再次下单,应对浮盈回吐变浮亏，增加两级价格回撤止盈(可自行设定)

2021-07-04 处理取消订单再次下单的bug

2021-07-03 对下单未成交取消进行再次下单处理

2021-07-02 简化策略，增加收益及减少亏损(重大更新)

2021-06-28 修改策略和止盈止损处理(大更新)，策略是趋势策略，遇到震荡行情可以停用。

2021-06-01 增加strategy_flag参数，此参数控制策略版本，20210601对原策略进行修改，增加一个版本，对空单进行优化开仓，下单量会更小.

2021-05-20 修改配置文件参数排序,修改止盈止损位置的bug,增加新的配置参数tick_flag，提供多种止盈止损处理.

2021-05-19 增加配置项适应新的止盈止损处理，修改止盈止损处理，增加版本记录，增加新的下单价格处理

2021-05-17 增加止盈止损部分说明，增加亏损后加倍开单量的开关及处理代码

2021-05-15  增加对策略运行消息是否发钉钉的控制，增加从交易所币最小值的查询适应所有币交易,增加提供配置参数

2021-05-14  初始始上传


# 联系(建议加群,方便第一时间通知)
打开http://small.yjyzj.cn 可以扫码加开发者微信或微信群

# 关于核心代码编译的说明

大家想赚钱，那只有跟着大户的车赚点小钱。那些已经实现财富自由的人，请不要使用本机器人，为散户留口汤喝。
当一个交易对某开仓的方向资金量达到一定的程度，那必然会成为大户的目标，这样再好的策略或者机器人都只能是下酒菜。
所以，我为了一个策略能使用的足够久而不需要经常去修改参数只能对部分代码进行编译。
这样首先就让一部分担心安全的人没有了使用的冲动，那会使用的人必然资金量不大(因为我本人也是用30U去跑这个机器人)或者会使用小号去跑这个机器人。
这样的结果必然是只要机器人够好，那使用者都可以跟着大户的车赚点小钱。
当然我也有点小心思，想着这个机器人足够好的话，那我完全可以基于这个策略去做量化平台或者进行收费。为了收费核心代码编译是必须的。

# 用到的链接

wss://fstream.binance.com/  币安ws
https://fapi.binance.com  币安api
https://oapi.dingtalk.com  发送钉钉webhook消息
https://link.yjyzj.cn/  我的，用来收集异常错误及发微信公众号消息，后续如果收费也会用这个进行授权

## 看到这还在担心资金安全问题，请不要使用本机器人

