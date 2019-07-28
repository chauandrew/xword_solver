from neo4j import GraphDatabase
import json
import sys

if len(sys.argv) != 2:
    print("USAGE: load_json.py filename")
    exit(1)

filename = sys.argv[1]

word_query ="MERGE (w:Word {body: $word, length: $len}) " +\
            "ON CREATE SET w.freq = 1 " +\
            "ON MATCH SET w.freq = w.freq + 1" 

clue_query ="WITH $clues AS clues " +\
            "UNWIND clues as clue MERGE (c:Clue {body: clue})"

rel_query = "WITH {clues} AS clues " +\
            "UNWIND clues AS clue " +\
            "MATCH (c:Clue {body: clue}) " +\
            "WITH c " +\
            "MATCH (w:Word {body: $word}) " +\
            "MERGE (c) -[:DESCRIBES]-> (w)"


# Create nodes for a single word, clues pair
def create_nodes(session, word, clues):
    if len(word) < 3 or len(word) > 23:
        return
    session.run(word_query, word=word, len=len(word)) # word node
    session.run(clue_query, clues=clues) # clue node
    session.run(rel_query, word=word, clues=clues) # word-clue relation

# connect to database and load 
if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("xword", "xword"))

    with driver.session() as session:
        with open(f"{filename}", "r") as f:
            data = json.load(f)
        for word, clues in data.items():
            try:
                create_nodes(session, word, clues)
            except:
                pass

    driver.close()
