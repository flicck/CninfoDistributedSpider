# -*- coding: utf-8 -*-
#用于调试的类
from scrapy.cmdline import execute

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print(os.path.dirname(os.path.abspath(__file__)))

execute()
