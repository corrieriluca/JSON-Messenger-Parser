#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
from enum import Enum
from DateFormatter import dateFormat, frenchDateFormat

s = 1553939328055
content = "some message"

# Uncomment the following line and comment the line for french format to use english format of date
# readableDate = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f') # english format
# readableDate = datetime.datetime.fromtimestamp(s).strftime('%d-%m-%Y %H:%M:%S') # french format

print(dateFormat(s))
print(frenchDateFormat(s))
