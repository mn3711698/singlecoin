# -*- coding: utf-8 -*-

##############################################################################
# Author：QQ173782910
##############################################################################
# linux支持python3.7,python3.6 windows支持64位python3.8,python3.7
import platform

if platform.system() == 'Windows':
    if '3.8' in platform.python_version():
        try:
            from .TradeRun import TradeRun
        except Exception as e:
            raise ValueError("请将本目前下的TradeRun_w38重命名为TradeRun替换原来的TradeRun")

    elif '3.7' in platform.python_version():
        try:
            from .TradeRun import TradeRun
        except Exception as e:
            raise ValueError("请将本目前下的TradeRun_w37重命名为TradeRun替换原来的TradeRun")
    else:
        raise ValueError("python版本未提供支持")
elif platform.system() == 'Linux':
    if '3.6' in platform.python_version():
        try:
            from .TradeRun import TradeRun
        except Exception as e:
            raise ValueError("请将本目前下的TradeRun_l36.so重命名为TradeRun.so替换原来的TradeRun.so")
    elif'3.7' in platform.python_version():
        try:
            from .TradeRun import TradeRun
        except Exception as e:
            raise ValueError("请将本目前下的TradeRun_l37.so重命名为TradeRun.so替换原来的TradeRun.so")
    else:
        raise ValueError("python版本未提供支持")
else:
    raise ValueError("操作系统未提供支持")
