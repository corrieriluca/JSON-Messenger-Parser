#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author : Luca Corrieri
# JSON-messenger-exporter
# 2019 MIT License

import datetime
from enum import Enum

class MonthEN(Enum):
    JAN = ('January', 1)
    FEB = ('February', 2)
    MAR = ('March', 3)
    APR = ('April', 4)
    MAY = ('May', 5)
    JUN = ('June', 6)
    JUL = ('July', 7)
    AUG = ('August', 8)
    SEP = ('September', 9)
    OCT = ('October', 10)
    NOV = ('November', 11)
    DEC = ('December', 12)

class MonthFR(Enum):
    JAN = ('Janvier', 1)
    FEB = ('Février', 2)
    MAR = ('Mars', 3)
    APR = ('Avril', 4)
    MAY = ('Mai', 5)
    JUN = ('Juin', 6)
    JUL = ('Juillet', 7)
    AUG = ('Août', 8)
    SEP = ('Septembre', 9)
    OCT = ('Octobre', 10)
    NOV = ('Novembre', 11)
    DEC = ('Décembre', 12)

def dateFormat(s):
    '''
        Format the timestamp_ms into a readable date like this :
        'On January 1 2019 at 00:42:00'
        @param s: milliseconds from unix epoch
    '''
    s /= 1000.0

    messageDay = datetime.datetime.fromtimestamp(s).strftime('%d ')
    messageMonthInt = int(datetime.datetime.fromtimestamp(s).strftime('%m'))
    messageMonthStr = 'ERROR '
    messageYear = datetime.datetime.fromtimestamp(s).strftime('%Y')
    messageTime = datetime.datetime.fromtimestamp(s).strftime('%H:%M:%S')

    for month in MonthEN:
        if messageMonthInt == month.value[1]:
            messageMonthStr = month.value[0] + ' '
            break

    fullyReadableMessageDate = 'On ' + messageMonthStr + messageDay + messageYear + ' at ' + messageTime

    return fullyReadableMessageDate

def frenchDateFormat(s):
    '''
        Format the timestamp_ms into a readable date like this :
        'Le 1 Janvier 2019 à 00:42:00'
        @param s: milliseconds from unix epoch
    '''
    s /= 1000.0

    messageDay = datetime.datetime.fromtimestamp(s).strftime('%d ')
    messageMonthInt = int(datetime.datetime.fromtimestamp(s).strftime('%m'))
    messageMonthStr = 'ERROR'
    messageYear = datetime.datetime.fromtimestamp(s).strftime('%Y')
    messageTime = datetime.datetime.fromtimestamp(s).strftime('%H:%M:%S')

    for month in MonthFR:
        if messageMonthInt == month.value[1]:
            messageMonthStr = month.value[0] + ' '
            break

    fullyReadableMessageDate = 'Le ' + messageDay + messageMonthStr + messageYear + ' à ' + messageTime

    return fullyReadableMessageDate
