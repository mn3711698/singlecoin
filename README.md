# singlecoin(支持windows+linux,交易所目前只支持币安,目前只支持单币运行)

## 本项目只是提供代码，不对使用者因使用本代码实际产生的盈亏负责(测试时,使用蚂蚁仓跑ETHUSDT胜率百分百)

## 提供多级止盈，可以自行计算止盈的数值

# 注意

## API的权限只需要有交易权限就够了，不要开提币权限！

## API的权限只需要有交易权限就够了，不要开提币权限！

## API的权限只需要有交易权限就够了，不要开提币权限！

# windows支持64位的python,3.8或3.7,linux系统支持python3.6或python3.7

## windows使用说明(路径写死了)
下载本项目代码压缩包，放在C盘根目录下，解压，最终代码在C:\singlecoin\下。如果是git下载，也请代码放在C:\singlecoin\下，建议使用git下载，方便后续更新

先下载https://download.microsoft.com/download/5/f/7/5f7acaeb-8363-451f-9425-68a90f98b238/visualcppbuildtools_full.exe
安装时，直接下一步，不需要选择其他的。

安装相关库(只支持python3)  pip3 install -r requirements.txt 或 pip install -r requirements.txt

填好config.py里边的配置项，到此，准备工作做好。在项目目录C:\singlecoin\下执行python3 Start.py

如果遇到启动不了，要先确认python是不是64版本，如果使用的是python3.7要将RunUse里的TradeRun_w37.pyd重命名为TradeRun.pyd，
strategies下的base_w37.pyd重命名为base.pyd,
如果使用的是python3.8要将RunUse里的TradeRun_w38.pyd重命名为TradeRun.pyd,strategies下的base_w38.pyd重命名为base.pyd

相关持仓及订单信息请看币安的网页或者APP对应的交易对下的数据。

如果后续有更新代码，可以直接git下载就好了。下载好后，关掉cdm窗口，重新打开窗口执行python3 Start.py就好了

## linux使用说明(路径写死了)
下载本项目代码压缩包，放在/var/games/目录下，解压，最终代码在/var/games/singlecoin/下。

如果是git下载，也请代码放在/var/games/singlecoin/下，建议使用git下载，方便后续更新

安装相关库(只支持python3)  pip3 install -r requirements.txt 或 pip install -r requirements.txt

填好config.py里边的配置项，到此所有准备工作都做好了。在项目目录/var/games/singlecoin/下执行python3 Start.py 或python Start.py

如果遇到启动不了，要先确认python是不是64版本，如果使用的是python3.7要将RunUse里的TradeRun_l37.so重命名为TradeRun.so，
strategies下的base_l37.so重命名为base.so,
如果使用的是python3.6要将RunUse里的TradeRun_l36.so重命名为TradeRun.so,strategies下的base_l36.so重命名为base.so

相关持仓及订单信息请看币安的网页或者APP对应的交易对下的数据。

建议使用Supervisor启动

如果后续有更新代码，可以直接git下载就好了。下载好后，关掉cdm窗口，重新打开窗口执行python3 Start.py就好了

## 关于代码更新说明
建议使用git命令来下载，这样更新就不影响。

## 多级动态止盈配置说明

由于不同的币(交易标的)，不同的交易张数，不同的行情所产生的收益是不一致的，这就要求在配置多级动态止盈时所填写的收益值及回撤值需要自己计算。
由于我也没有确定相关收益值及回撤值，所以是没有任何参考数据的，需要使用者自己小额使用，再根据持仓日志，止盈止损日志，持仓流水三个页面的记录数据，自己计算出不同的收益值，
在达到某个回撤值时进行止盈。页面及代码都有计算说明，目前我也是用ETH永续本币，每次交易１张，准备根据相关日志来确定不同的收益值要设置多少的回撤值。当我确定了我的收益值及回撤值会在些提示参考。

# 更新日志  (开源协议为MIT)

2021-05-14  初始始上传


# 联系
wx:huangyjwx(请注明机器人)


