import sys
import requests
import datetime
import json
import re
import urllib
import html

if len(sys.argv) != 4:
    print("USAGE: xwordinfo.py folderpath startyear endyear")
    exit(1)
folderpath = sys.argv[1]

date = datetime.datetime(int(sys.argv[2]), 1, 1) # oldest available crossword
incr = datetime.timedelta(days=1)
today = datetime.datetime(int(sys.argv[3]), 1, 1)
year = int(date.strftime("%Y"))

def get_year(date):
    return int(date.strftime("%Y"))

def format_date(date):
    return date.strftime("%m/%d/%y")

def format_word(word):
    return html.unescape(word).upper()

url='https://www.xwordinfo.com/JSON/TrackData.aspx?date='
word_data = {}


while date < today:
    response = requests.get(url + format_date(date))
    if response.status_code == 200 and response.text != "": # if successful
        answers = json.loads(response.text)
        all_clues = answers['Across'] + (answers['Down'])
        for line in all_clues:
            try:
                pattern = re.search(r': (.+) : <b>([A-Z]+)</b>', line)
                clue = format_word(pattern.group(1))
                word = format_word(pattern.group(2))
                if word in word_data:
                    word_data[word].append(clue)
                else:
                    word_data[word] = [clue]
            except: 
                pass
    date += incr
    if get_year(date) > year:
        with open("{}/{}.json".format(folderpath, year), "w+") as f:
            json.dump(word_data, f, indent=2)
        print("Collected data from year: {}".format(year))
        year = get_year(date)
        word_data = {}

print("Finished collecting all data!")
