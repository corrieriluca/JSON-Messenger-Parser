# JSON Messenger Parser

**_Still under active development_**

*Beautiful image here*

This program allows you to parse a Facebook Messenger JSON save file which you can
get from your [Facebook settings menu](https://www.facebook.com/settings?tab=your_facebook_information) 
(Download Your Information). It parses the JSON file into a beautiful and readable
HTML file which you can display in your browser with a nice and simple messenger-like
style.

## How to use it
### Installation

This program has been tested with Python 3.7.3

It requires Jinja2 in order to work properly and render the HTML file.

I highly recommend you to use a virtual environment with `virtualenv` :
```bash
git clone https://github.com/corrieriluca/JSON-to-HTML-Messenger-Parser.git
cd JSON-to-HTML-Messenger-Parser
virtualenv env
source env/bin/activate
# use the program
deactivate
```
Finally you can use `pip` in order to install Jinja2. This program has been tested with
Jinja2 2.10.
```bash
pip install -r requirements.txt
```

### Basic usage

You can run `python3 main.py -h` to display help:
```
Basic usage: main.py -i <jsonfile> -o <htmlouputfile> -n <your_username> -l <FR/EN>

Arguments:
-i, --input <path>: the path to the Messenger JSON file of your conversation
-o --output <path>: the path to the HTML output file (created if it does not exist)
-n, --username <your_username>: your username in the conversation (ex: -n 'John Doe')
-l, --lang <FR/EN>: the language to display dates and other elements
-g, --log: save a log with the messages in [outputfile].log
-h, --help: display this help
```

This program supports two languages : English and French, in order to display properly
dates and other translated elements. Messages are not translated !

You have the choice to save a log file with `-g` or `--log` in which just the messages,
their sender and their date are displayed.

You can choose to specify your username in the conversation in order to distinguish
your messages from those of others.
