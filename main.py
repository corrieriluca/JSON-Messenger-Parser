#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author : Luca Corrieri
# JSON-messenger-exporter
# 2019 MIT License

import sys, getopt, json, time, os.path
from dateFormatter import dateFormat, frenchDateFormat
from jinja2 import Template

# ------------------- Message and Conversation classes -------------------------

class Message():
    def __init__(self, sender, content, date):
        self.sender = sender
        self.content = content
        self.date = date # pretty formated first

class Conversation():
    def __init__(self, title, participants, messages, username):
        self.title = title
        self.participants = participants
        self.messages = messages
        self.username = username

# ---------------------------- JSON file ---------------------------------------

def loadJSONFile(file):
    '''
        Returns a json object from the json file
        @param file: path to the file
    '''
    try:
        with open(file) as file:
            data = file.read()
    except FileNotFoundError:
        print("ERROR: You have to specify a correct path")
        sys.exit(42)

    return json.loads(data)

def buildMessageList(messages, language):
    '''
        Returns the built list of messages correctly formatted in the chosen language
        @param messages: the message dictionnary
        @param language: the language (FR/EN)
    '''
    n = len(messages)
    L = []
    
    for i in range(n - 1, -1, -1): # in order to be sorted
        sender = encodingCorrection(messages[i]["sender_name"])
        
        content = "NO CONTENT IN THIS MESSAGE" # to be replaced by media integration in the future
        if "content" in messages[i].keys():
            content = encodingCorrection(messages[i]["content"])
        
        timestamp = messages[i]["timestamp_ms"]
        date = ""
        if language == "FR":
            date = frenchDateFormat(timestamp)
        elif language == "EN":
            date = dateFormat(timestamp)
        else:
            raise Exception("Unknown language")

        message = Message(sender, content, date)
        
        L.append(message)

    return L

# ------------------------------- Program --------------------------------------

def helpDisplay():
    print("Basic usage: main.py -i <jsonfile> -o <htmlouputfile> -n <your_username> -l <FR/EN>")
    print("")
    print("Arguments:")
    print("-i, --input <path>: the path to the Messenger JSON file of your conversation")
    print("-o --output <path>: the path to the HTML output file (created if it does not exist)")
    print("-n, --username <your_username>: your username in the conversation (ex: -n 'John Doe')")
    print("-l, --lang <FR/EN>: the language to display dates and other elements")
    print("-g, --log: save a log in messenger_log.txt (same folder as ouput file)")
    print("-h, --help: display this help")
    print("")

def wrongArguments():
    print("Wrong arguments: main.py -i <jsonfile> -o <htmlouputfile> -n <your_username> -l <FR/EN>")

def loadArguments(argv):
    inputfile = ''
    outputfile = ''
    username = 'NOBODY'
    language = 'ERROR'
    saveLog = False

    if len(argv) == 0:
        wrongArguments()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "hi:o:n:l:g", ["help", "input=", "output=", "username=", "lang=", "log"])
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
        elif opt in ("-l", "--lang") and arg in ("FR", "EN"):
            language = arg
        elif opt in ("-g", "--log"):
            saveLog = True

    return (inputfile, outputfile, username, language, saveLog)

def encodingCorrection(string):
    return string.encode('latin1').decode('utf-8')

# ------------------------------ Main ------------------------------------------

def main(argv):
    (inputfile, outputfile, username, language, saveLog) = loadArguments(argv)

    # Debugging
    print("Input file:", inputfile)
    print("Ouput file:", outputfile)
    print("Your name:", username)
    print("Your language:", language)
    print("")
    print("Parsing, this may take a while...")

    jsonData = loadJSONFile(inputfile)

    participants = jsonData["participants"]
    for participant in participants:
        participant = encodingCorrection(participant["name"])

    title = encodingCorrection(jsonData["title"])
    messages = buildMessageList(jsonData["messages"], language)

    conversation = Conversation(title, participants, messages, username)

    # HTML rendering
    if language == 'FR':
        with open('templates/templateFR.html') as temp:
            template = Template(temp.read())
    elif language == 'EN':
        with open('templates/templateEN.html') as temp:
            template = Template(temp.read())
    else:
        raise Exception("Unknown language")

    htmlRender = template.render(conversation=conversation)
    
    try:
        with open(outputfile, 'w') as output:
            output.write(htmlRender)
    except FileNotFoundError:
        print("ERROR: You have to specify a correct path")
        sys.exit(42)

    # Logs
    if saveLog:
        log = "JSON to HTML Messenger Parser Log\nOn " + time.strftime('%c') +'\n\n'
        for message in conversation.messages:
            log += message.date + '\n' + message.sender + ': ' + message.content + '\n'

        logLocation = os.path.split(outputfile)[0] + '/messenger_log.txt'
        with open(logLocation, 'w') as logFile:
            logFile.write(log)

        print("Log successfully saved in", logLocation)

    print("Conversation successfully parsed into HTML in", outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
