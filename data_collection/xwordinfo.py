import sys
import requests
import datetime
import json
import re
import urllib

if len(sys.argv) != 2:
    print("USAGE: xwordinfo.py folderpath")
    exit(1)
folderpath = sys.argv[1]

date = datetime.datetime(1942, 2, 15) # oldest available crossword
incr = datetime.timedelta(days=1)
today = datetime.datetime.now()
year = int(date.strftime("%Y"))

def get_year(date):
    return int(date.strftime("%Y"))

def format_date(date):
    return date.strftime("%m/%d/%y")

def format_word(word):
    return urllib.parse.unquote(word).replace(';', '').replace('&quot', '\"'
        ).replace('&#39', '\'').upper()

url='https://www.xwordinfo.com/JSON/TrackData.aspx?date='
word_data = {}


while date < today:
    response = requests.get(url + format_date(date))
    if response.status_code == 200 and response.text != "": # if successful
        answers = json.loads(response.text)
        all_clues = answers['Across'] + (answers['Down'])
        for line in all_clues:
            pattern = re.search(r': (.+). : <b>([A-Z]+)</b>', line)
            clue = format_word(pattern.group(1))
            word = format_word(pattern.group(2))
            if word in word_data:
                word_data[word].append(clue)
            else:
                word_data[word] = [clue]
    date += incr
    if get_year(date) > year:
        with open(f"{folderpath}/{year}.json", "w+") as f:
            json.dump(word_data, f)
        year = get_year(date)
        print(f"Collected data from year: {year}")
        word_data = {}

print("Finished collecting all data!")
