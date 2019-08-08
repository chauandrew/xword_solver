from neo4j import GraphDatabase
import json
import sys
import string
import re

PUNCT = set(string.punctuation)

if len(sys.argv) != 2:
    print("USAGE: load_json.py filename")
    exit(1)

filename = sys.argv[1]


# turn string into tokens, separated by punctuation
tokenizer = re.compile(r"[\w]+|[.,!?;:\"/\-–—_]")
def gramize(phrase, n):
    tokens = tokenizer.findall(phrase)
    sequence = [tokens[i:] for i in range(0, n)]
    ngrams = filter((lambda x: len(x) == len([y for y in x if y not in PUNCT])), zip(*sequence))
    return  [''.join(grp) for grp in ngrams]

word_query = "MERGE (w:Word {body: $word, length: $len})"

clues_query = "WITH $clues AS clues " +\
              "UNWIND clues as clue MERGE (c:Clue {body: clue})"

rel_query = "WITH {clues} AS clues " +\
            "UNWIND clues AS clue " +\
            "MATCH (c:Clue {body: clue}) " +\
            "WITH c " +\
            "MATCH (w:Word {body: $word}) " +\
            "MERGE (c) -[:DESCRIBES]-> (w)"

phrase_query =  "WITH $words AS words " +\
                "UNWIND words AS word " +\
                "WITH word, length(word) AS length " +\
                "MERGE (w:Word {body: word, length: length})"

# Create nodes for a word, clues pair
def insert_relation(session, word, clues):
    if len(word) < 3 or len(word) > 23:
        return
    # first, insert the clue, word pair
    session.run(word_query, word=word, len=len(word)) # word node
    session.run(clues_query, clues=clues) # clue node
    session.run(rel_query, word=word, clues=clues) # word-clue relation
    # insert unigrams, bigrams, and trigrams from the clue as words
    for clue in clues:
        # session.run(phrase_query, words=gramize(clue, 1))
        session.run(phrase_query, words=gramize(clue, 2))
        # session.run(phrase_query, words=gramize(clue, 3))

# connect to database and load everything
if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("xword", "xword"))

    with driver.session() as session:
        with open(f"{filename}", "r") as f:
            data = json.load(f)
        for word, clues in data.items():
            try:
                insert_relation(session, word, clues)
            except:
                pass

    driver.close()
