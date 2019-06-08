#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author : Luca Corrieri
# JSON-messenger-exporter
# 2019 MIT License

import sys, getopt, json, time, os.path
from dateFormatter import dateFormat, frenchDateFormat
from jinja2 import Environment, FileSystemLoader

# ------------------- Message and Conversation classes -------------------------

class Message():
    def __init__(self, sender, contentType, content, addContent, date):
        self.sender = sender
        self.contentType = contentType # text / photos / audio / gif / sticker / video
        self.content = content # plain text or a media link
        self.addContent = addContent # sometimes an additional text content comes (like in videos)
        self.date = date # pretty formated


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
        print("ERROR: You have to specify a correct path for input folder")
        sys.exit(42)

    return json.loads(data)


def buildMessageList(messages, language, inputfolder, stickers):
    '''
        Returns the built list of messages correctly formatted in the chosen language
        @param messages: the message dictionnary
        @param language: the language (FR/EN)
    '''
    n = len(messages)
    L = []
    
    for i in range(n - 1, -1, -1): # in order to be sorted
        sender = encodingCorrection(messages[i]["sender_name"])
        addContent = "" # by default
        content = []

        # 6 types : photos, audio_files, sticker, gifs, videos, content (text)
        if "content" in messages[i].keys() and not "videos" in messages[i].keys(): # text
            content.append(encodingCorrection(messages[i]["content"]))
            contentType = "text"
        elif "photos" in messages[i].keys(): # photos (path)
            for photo in messages[i]["photos"]:
                content.append(mediaManager(encodingCorrection(photo["uri"]), "photos", inputfolder, stickers))
            contentType = "photos"
        elif "audio_files" in messages[i].keys(): # audio_files (path)
            for audio in messages[i]["audio_files"]:
                content.append(mediaManager(encodingCorrection(audio["uri"]), "audio_files", inputfolder, stickers))
            contentType = "audio"
        elif "gifs" in messages[i].keys(): # gifs (path)
            for gif in messages[i]["gifs"]:
                content.append(mediaManager(encodingCorrection(gif["uri"]), "gifs", inputfolder, stickers))
            contentType = "gif"
        elif "videos" in messages[i].keys(): # videos (path)
            if "content" in messages[i].keys(): # because sometimes videos come with a text content...
                addContent = encodingCorrection(messages[i]["content"])
            for video in messages[i]["videos"]:
                content.append(mediaManager(encodingCorrection(video["uri"]), "videos", inputfolder, stickers))
            contentType = "video"
        elif "sticker" in messages[i].keys(): # sticker (path)
            content.append(mediaManager(encodingCorrection(messages[i]["sticker"]["uri"]), "sticker", inputfolder, stickers))
            contentType = "sticker"
        
        timestamp = messages[i]["timestamp_ms"]
        date = ""
        if language == "FR":
            date = frenchDateFormat(timestamp)
        elif language == "EN":
            date = dateFormat(timestamp)
        else:
            raise Exception("Unknown language")

        message = Message(sender, contentType, content, addContent, date)
        
        L.append(message)

    return L


def mediaManager(path, contentType, inputfolder, stickers):
    '''
    returns the correct path for a media file
    '''
    filename = os.path.basename(path)
    filepath = ""
    if contentType == "photos":
        filepath = inputfolder + '/photos/' + filename
    elif contentType == "audio_files":
        filepath = inputfolder + '/audio/' + filename
    elif contentType == "gifs":
        filepath = inputfolder + '/gifs/' + filename
    elif contentType == "videos":
        filepath = inputfolder + '/videos/' + filename
    elif contentType == "sticker" and stickers != '':
        filepath = stickers + filename

    return os.path.normpath(filepath)

# ------------------------------- Program --------------------------------------

def helpDisplay():
    print("Basic usage: main.py -i <inputfolder> -o <htmlouputfile> [-s <stickerfolder>] -n <your_username> -l <FR/EN>")
    print("")
    print("Arguments:")
    print("-i, --input <path>: the path to the folder containing your conversation (the JSON file must be named 'message_1.json')")
    print("-o, --output <path>: the path to the HTML output file (created if it does not exist)")
    print("-s, --stickers <path>: the path to the folder containing your stickers (optional)")
    print("-n, --username <your_username>: your username in the conversation (ex: -n 'John Doe')")
    print("-l, --lang <FR/EN>: the language to display dates and other elements")
    print("-g, --log: save a log with the messages in [outputfile].log")
    print("-h, --help: display this help")
    print("")


def wrongArguments():
    print("Wrong arguments: main.py -i <inputfolder> -o <htmlouputfile> [-s <stickerfolder>] -n <your_username> -l <FR/EN>")
    print("Run main.py -h for more info")


def loadArguments(argv):
    inputfolder = ''
    outputfile = ''
    username = 'NOBODY'
    language = 'ERROR'
    saveLog = False
    stickers = ''

    if len(argv) == 0:
        wrongArguments()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "hi:o:n:l:gs:", ["help", "input=", "output=", "username=", "lang=", "log", "stickers="])
    except getopt.GetoptError:
        wrongArguments()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helpDisplay()
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfolder = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
        elif opt in ("-n", "--username"):
            username = arg
        elif opt in ("-l", "--lang") and arg in ("FR", "EN"):
            language = arg
        elif opt in ("-g", "--log"):
            saveLog = True
        elif opt in ("-s", "--stcikers"):
            stickers = arg

    return (inputfolder, outputfile, username, language, saveLog, stickers)


def encodingCorrection(string):
    return string.encode('latin1').decode('utf-8')

# ------------------------------ Main ------------------------------------------

def main(argv):
    (inputfolder, outputfile, username, language, saveLog, stickers) = loadArguments(argv)

    # Debugging
    print("Input folder:", inputfolder)
    print("Ouput file:", outputfile)
    print("Stickers folder:", stickers)
    print("Your name:", username)
    print("Your language:", language)
    print("")
    print("Parsing, this may take a few seconds...")

    jsonData = loadJSONFile(inputfolder + "message_1.json")

    participants = jsonData["participants"]
    for participant in participants:
        participant = encodingCorrection(participant["name"])

    title = encodingCorrection(jsonData["title"])
    messages = buildMessageList(jsonData["messages"], language, inputfolder, stickers)

    conversation = Conversation(title, participants, messages, username)

    # HTML rendering
    todaysTimestamp = ""
    env = Environment(loader=FileSystemLoader('templates'))

    if language == 'FR':
        todaysTimestamp = frenchDateFormat(int(round(time.time() * 1000)))
        template = env.get_template('FR/base.html')
    elif language == 'EN':
        todaysTimestamp = dateFormat(int(round(time.time() * 1000)))
        template = env.get_template('EN/base.html')
    else:
        raise Exception("Unknown language")

    htmlRender = template.render(conversation=conversation, date=todaysTimestamp)
    
    try:
        with open(outputfile, 'w') as output:
            output.write(htmlRender)
    except FileNotFoundError:
        print("ERROR: You have to specify a correct path for output folder")
        sys.exit(42)

    # Logs
    if saveLog:
        log = "JSON to HTML Messenger Parser Log\nGenerated on " + time.strftime('%c') +'\n\n'
        for message in conversation.messages:
            log += message.date + '\n' + message.sender + ': ' + message.content + '\n'

        logLocation = os.path.splitext(outputfile)[0] + '.log'
        with open(logLocation, 'w') as logFile:
            logFile.write(log)

        print("Log successfully saved in", logLocation)

    print("Conversation successfully parsed into HTML in", outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
