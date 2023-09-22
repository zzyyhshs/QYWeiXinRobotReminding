# -*- coding: utf-8 -*-
# file: reminding.py
# author: zhuyao
# email: zzyyhshs@163.com

import os
import sys

sys.path.append(os.path.split(os.path.abspath(__file__))[0])

from QYWeiXinRobot.reminderByCommandLine import main


if __name__ == '__main__':
    main()


