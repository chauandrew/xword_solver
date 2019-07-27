import requests
import datetime
import json
import re
import urllib


date = datetime.datetime(1942, 2, 15) # oldest available crossword
incr = datetime.timedelta(days=1)
today = datetime.datetime.now()

def format_date(date):
    return date.strftime("%m/%d/%y")

def format_word(word):
    return urllib.parse.unquote(word).replace(';', '').replace('&quot', '\"'
        ).replace('&#39', '\'').upper()

url='https://www.xwordinfo.com/JSON/TrackData.aspx?date='
word_data = {}

try:
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
finally:
    with open("/home/achau/College/github/xword_solver/data_collection/xwordinfo.json", "w+") as f:
        json.dump(word_data, f)