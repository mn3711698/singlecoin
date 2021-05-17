# singlecoin(支持windows+linux,交易所目前只支持币安,目前只支持单币运行)

## 有人担心安全，有人认为胜率造假，我只能说担心安全的请不要用，担心造假的我可以上图，但胜率这个还是建议使用者自己蚂蚁仓实盘试一下。

![](https://github.com/mn3711698/singlecoin/blob/main/order.png)

# 当你还在为要不要使用时，不少人因为收益不错问我能不能提供源码
已经有使用者主动告诉我，他所在的机构使用虚拟机的方式部署跑多个币对(一个虚拟机一个币对)，
有的使用者买多个云主机跑多个币对。让这些使用者这么麻烦我真的不好意思，只能说多币对机器人已经在开发了

## 本项目只是提供代码，不对使用者因使用本代码实际产生的盈亏负责(实盘测试时,2021-5-11至2021-5-17使用蚂蚁仓跑ETHUSDT胜率百分百)

## 提供多级止盈，可以自行设置计算止盈的配置参数及修改止损配置(目前止损没有设置，只提供一个趋势止损)

# 注意(白嫖更要注意安全，因为核心代码没有开源，大家慎用)

## API的权限只需要有交易权限就够了，不要开提币权限,还要限制ip！

## API的权限只需要有交易权限就够了，不要开提币权限,还要限制ip！

## API的权限只需要有交易权限就够了，不要开提币权限,还要限制ip！

# 需要准备云主机，windows支持64位的python,3.8或3.7,linux系统支持python3.6或python3.7

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

填好config.py里边的配置项，确认python版本，如果使用的是python3.7要将RunUse里的TradeRun_l37.so重命名为TradeRun.so，
strategies下的base_l37.so重命名为base.so,
如果使用的是python3.6要将RunUse里的TradeRun_l36.so重命名为TradeRun.so,strategies下的base_l36.so重命名为base.so

到此所有准备工作都做好了。在项目目录/var/games/singlecoin/下执行python3 Start.py 或python Start.py ,就可以躺着赚钱了

相关持仓及订单信息请看币安的网页或者APP对应的交易对下的数据。

建议使用Supervisor启动

如果后续有更新代码，可以直接git下载就好了。重新执行python3 Start.py就好了

注意:持仓方向是单向(双向持仓要改为单向否则无法下单)，杠杆是交易所默认未进行另外设定
## 关于代码更新说明
建议使用git命令来下载，这样更新就不影响。

## 多级止盈说明

由于不同的币(交易标的)，不同的交易张数，不同的行情所产生的收益是不一致的，
这就要求在配置多级止盈时所填写的收益值及回撤值需要自己计算。
由于我也没有确定相关收益值及回撤值，所以是没有任何参考数据的，需要使用者自己小额使用，根据实际情况进行确定。
目前我也是用ETH永续U本位合约，每次交易0.003张。

具体代码看strategies/LineWith.py文件的on_ticker_data这个方法，这里是止盈止损处理，可自行修改

当某些币不能保持百分之百的胜率，那完全可以不要多级止盈，单纯交由策略处理，这样利益最大化，使得盈利有可能比亏损多，保持正收益。

增加亏损后加倍开单量，毕竟在这样高胜率的情况下，这是完全可行的，前提是保证金够。

目前是没有亏损多少进行止损的处理，使用者有需要可以自己增加这一部分的处理代码。

## 百分百胜率说明(并不是每个币都能保证)

config.py配置是我跑ETH的默认配置，代码也是我跑eth相关的设置。

我默认开单0.003张，止盈是多级，默认最小是开单张数10倍u也就是0.03U收益止盈。

当开仓先亏损并达到设定值后再盈利，那这个盈利值为0.02u。

目前我最高的单次收益为0.05U。

已有多人跑不同的币收益很不错，并希望我能提供源码，所以我跑的胜率不会造假，至于不同的配置跑的胜率多少只能各自实测。


# 特别提醒

不同的币的计算参数是不一样的，请各位自己参考我代码的eth设置，去设置自己要跑的币种。比如BNB,直接用这个配置跑是下不了单的，最小下单数是0.01。
收益默认设置是下单数的10倍u，那就是0.1u了，我没怎么试，不知道是否容易达到，所以建议是先0.01u收益开始去设置多级，以保证收益。


# 更新日志  (开源协议为MIT)

2021-05-17 增加止盈止损部分说明，增加亏损后加倍开单量的开关及处理代码

2021-05-15  增加对策略运行消息是否发钉钉的控制，增加从交易所币最小值的查询适应所有币交易,增加提供配置参数

2021-05-14  初始始上传


# 联系
打开http://small.yjyzj.cn 可以扫码加开发者微信或微信群

# 关于核心代码编译的说明

大家想赚钱，那只有跟着大户的车赚点小钱。那些已经实现财富自由的人，请不要使用本机器人，为散户留口汤喝。
当一个交易对某开仓的方向资金量达到一定的程度，那必然会成为大户的目标，这样再好的策略或者机器人都只能是下酒菜。
所以，我为了一个策略能使用的足够久而不需要经常去修改参数只能对部分代码进行编译。
这样首先就让一部分担心安全的人没有了使用的冲动，那会使用的人必然资金量不大(因为我本人也是用30U去跑这个机器人)或者会使用小号去跑这个机器人。
这样的结果必然是只要机器人够好，那使用者都可以跟着大户的车赚点小钱。
当然我也有点小心思，想着这个机器人足够好的话，那我完全可以基于这个策略去做量化平台或者进行收费。为了收费核心代码编译是必须的。
当然，我会一直提供白嫖(只要在小程序每天签到就可以永久白嫖)。万一有人看上我的这个策略有个几十万我也会卖掉。

# 用到的链接

wss://fstream.binance.com/  币安ws
https://fapi.binance.com  币安api
https://oapi.dingtalk.com  发送钉钉webhook消息
https://link.yjyzj.cn/  我的，用来收集异常错误及发微信公众号消息，后续如果收费也会用这个进行授权

## 看到这还在担心资金安全问题，请不要使用本机器人

