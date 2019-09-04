from neo4j import GraphDatabase
import json
import sys
import string
import re
import signal

PUNCT = set(string.punctuation)

if len(sys.argv) != 2:
    print("USAGE: load_json.py filename")
    exit(1)

filename = sys.argv[1]


# turn string into tokens, separated by punctuation
tokenizer = re.compile(r"[A-Za-z]+|[.,!?;:\"/\-–—]")
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
reference_re = re.compile(r"[0-9]+\-(ACROSS|DOWN)") # match reference clues
def insert_relation(session, word, clues):
    if len(word) < 3 or len(word) > 23:
        return
    # first, insert the clue, word pair
    session.run(word_query, word=word, len=len(word)) # word node
    clues = [clue for clue in clues if not reference_re.search(clue)]
    if clues:
        session.run(clues_query, clues=clues) # clue node
        session.run(rel_query, word=word, clues=clues) # word-clue relation
    # insert unigrams, bigrams, and trigrams from the clue as words
    for clue in clues:
        for x in range(1, 4): # 1 2 3
            session.run(phrase_query, words=gramize(clue, x))

# connect to database and load everything
if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("xword", "xword"))

    with driver.session() as session:
        print("Adding constraints...")
        session.run("CREATE CONSTRAINT ON (w:Word) ASSERT w.body IS UNIQUE")
        session.run("CREATE CONSTRAINT ON (c:Clue) ASSERT c.body IS UNIQUE")
        with open(f"{filename}", "r") as f:
            data = json.load(f)
        # load each word into database
        print(f"Processing {len(data)} words...")
        curr = 0
        for word, clues in data.items():
            if curr % 1000 == 0:
                print(f"Processing words {curr}-{len(data) if len(data) < curr + 1000 else curr + 1000}...")
            try:
                insert_relation(session, word, clues)
            except Exception as e:
                print(f"Exception caught: {e}", file=sys.stderr)
            curr += 1
        print("Scoring Words...")
        # add hint counts to rank words by
        session.run("""
            MATCH (w:Word)<-[r]-(:Clue) 
            WITH count(r) AS score, w 
            SET w.score = score
        """)

    driver.close()
    print("Finished!")
