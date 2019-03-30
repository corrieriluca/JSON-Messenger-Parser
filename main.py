#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author : Luca Corrieri
# JSON-messenger-exporter
# 2019 MIT License

import sys, getopt, json
from dateFormatter import dateFormat, frenchDateFormat

# ------------------- Message and Conversation classes -------------------------

class Message():
    def __init__(self, sender, timestamp, content, date):
        self.sender = sender
        self.timestamp = timestamp # timestamp for sorting messages
        self.content = content
        self.date = date # readable date from timestamp

class Conversation():
    def __init__(self, title, participants, messages):
        self.title = title
        self.participants = participants
        self.messages = messages

# ---------------------------- JSON file ---------------------------------------

def loadJSONFile(file):
    '''
        Returns a json object from the json file
        @param file: path to the file
    '''
    with open("test.json") as file:
        data = file.read()

    return json.loads(data)

def buildMessageList(messages, formatOfDate):
    n = len(messages)
    L = []
    
    for i in range(n - 1, 0, -1): # in order to be sorted
        sender = messages[i]["sender_name"]
        timestamp = messages[i]["timestamp_ms"]
        content = "NO CONTENT IN THIS MESSAGE"
        if "content" in messages[i].keys():
            content = messages[i]["content"]
        
        date = ""
        if formatOfDate == "FR":
            date = frenchDateFormat(timestamp)
        elif formatOfDate == "EN":
            date = dateFormat(timestamp)
        else:
            raise Exception("Unknown format of date")

        message = Message(sender, timestamp, content, date)
        
        L.append(message)

    return L

# ------------------------------- Program --------------------------------------

def helpDisplay():
    print("Basic usage: main.py -i <jsonfile> -o <htmlouputfile> -n <your_username>")
    print("")
    print("Arguments:")
    print("-i, --input <path>: the path to the Messenger JSON file of your conversation")
    print("-o --output <path>: the path to the HTML output file (created if it does not exist)")
    print("-n, --username <your_username>: your username in the conversation (ex: -n 'John Doe')")
    print("-f, --format <FR/EN>: the format to display dates")
    print("-h, --help: display this help")
    print("")

def wrongArguments():
    print("Wrong arguments: main.py -i <jsonfile> -o <htmlouputfile> -n <your_username> -f <FR/EN>")

def loadArguments(argv):
    inputfile = ''
    outputfile = ''
    username = ''
    formatOfDate = 'ERROR'

    if len(argv) == 0:
        wrongArguments()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "hi:o:n:f:", ["help", "input=", "output=", "username=", "format="])
    except getopt.GetoptError:
        wrongArguments()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helpDisplay()
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
        elif opt in ("-n", "--username"):
            username = arg
        elif opt in ("-f", "--format") and arg in ("FR", "EN"):
            formatOfDate = arg

    return (inputfile, outputfile, username, formatOfDate)

# ------------------------------ Main ------------------------------------------

def main():
    print(firstMessage.displayMessage())

def main2(argv):
    (inputfile, outputfile, username, formatOfDate) = loadArguments(argv)

    # Debug
    print(inputfile)
    print(outputfile)
    print(username)
    print(formatOfDate)

    jsonData = loadJSONFile(inputfile)
    participants = jsonData["participants"]
    title = "Conversation with " + jsonData["title"]
    messages = buildMessageList(jsonData["messages"], formatOfDate)

    conversation = Conversation(title, participants, messages)

    # HTML templating here...

    # Debugging
    conv = ""
    for message in conversation.messages:
        conv += message.date + ' ' + message.content + '\n'

    with open(outputfile, 'w') as output:
        output.write(conv)


if __name__ == "__main__":
    main2(sys.argv[1:])
