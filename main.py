#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
from dateFormatter import dateFormat, frenchDateFormat

class Message():
    def __init__(self, sender, timestamp, content, date):
        self.sender = sender
        self.timestamp = timestamp # timestamp for sorting messages
        self.content = content
        self.date = date # readable date from timestamp

    def displayMessage(self):
        display = self.sender + ' a écrit: ' + self.content + ' le ' + self.date
        return display

# JSON file
with open("test.json") as file:
    data = file.read()

jsonConv = json.loads(data)

messageNumber = len(jsonConv["messages"])

firstMessageJSON = jsonConv["messages"][messageNumber - 1]
firstMessage = Message(firstMessageJSON["sender_name"], firstMessageJSON["timestamp_ms"], firstMessageJSON["content"], frenchDateFormat(firstMessageJSON["timestamp_ms"]))


# Uncomment the following line and comment the line for french format to use english format of date
# readableDate = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f') # english format
# readableDate = datetime.datetime.fromtimestamp(s).strftime('%d-%m-%Y %H:%M:%S') # french format

print(firstMessage.displayMessage())