# -*- coding: utf-8 -*-

##############################################################################
# Author：QQ173782910
##############################################################################
# linux支持python3.7,python3.6 windows支持64位python3.8,python3.7
import platform

if platform.system() == 'Windows':
    if '3.8' in platform.python_version():
        try:
            from .base import Base
        except Exception as e:
            raise ValueError(e)
    elif '3.7' in platform.python_version():
        try:
            from .base import Base
        except Exception as e:
            raise ValueError(e)
    else:
        raise ValueError("python版本未提供支持")
elif platform.system() == 'Linux':
    if '3.6' in platform.python_version():
        try:
            from .base import Base
        except Exception as e:
            raise ValueError(e)
    elif '3.7' in platform.python_version():
        try:
            from .base import Base
        except Exception as e:
            raise ValueError(e)
    else:
        raise ValueError("python版本未提供支持")
else:
    raise ValueError("操作系统未提供支持")
