import requests
import re
import string
import json
import sys

if len(sys.argv) != 3:
    print("Usage: python3 crosswordtracker [outfile] [A-Z]") 
    print("EX:\tpython3 crosswordtracker abc.json abc")
    exit(1)

outfile = sys.argv[1]
letters = sys.argv[2]

# group 1 is clue or word or page num
page_re = re.compile(r"class=\"paginator\">[0-9]+<\/a>")
word_re = re.compile(r"\/answer\/([a-z\-\_]+)")
clue_re = re.compile(r"\/clue\/[a-z\-\_]+\/\">([A-Za-z ]+)")

# example:  "http://crosswordtracker.com/browse/answers-starting-with-a"
word_html = "http://crosswordtracker.com/browse/answers-starting-with-"
# word_html_page = "http://crosswordtracker.com/browse/answers-starting-with-%s?page=n"
# example:  "http://crosswordtracker.com/answer/alligator"
clue_html = "http://crosswordtracker.com/answer/"

word_data = {}

def get_max_pages(html):
    pages = page_re.findall(html)
    return len(pages) + 1

def text_format(string):
    return string.strip(' -1234567890').replace(" ", "_").upper()


# for each letter in the alphabet
try:
    for letter in letters:
        letter = letter.lower() 
        url = f"{word_html}{letter}/"
        letter_resp = requests.get(url)
        if letter_resp.status_code != 200:
            continue
        npages = get_max_pages(letter_resp.text)
        # for each page of words
        for i in range(1, npages + 1): #range is inclusive
            page_url = f"{url}?page={i}"
            page_resp = requests.get(page_url)
            if page_resp.status_code != 200:
                continue
            words = word_re.findall(page_resp.text)
            # for each word, find matching clues
            for word in words:
                if len(word) < 3: 
                    continue
                clue_url = f"{clue_html}{word.lower()}"
                clue_resp = requests.get(clue_url)
                if clue_resp.status_code != 200:
                    continue
                clues = clue_re.findall(clue_resp.text)
                # store each clue 
                formatted_word = text_format(word)
                for clue in clues:
                    if not formatted_word in word_data:
                        word_data[formatted_word] = [text_format(clue)]
                    else:
                        word_data[formatted_word].append(text_format(clue))
finally:
    with open(outfile, 'w') as f:
        json.dump(word_data, f, indent=2)
