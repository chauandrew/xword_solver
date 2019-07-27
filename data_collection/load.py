from neo4j import GraphDatabase
import json
import sys
import os

if len(sys.argv) != 2:
    print("USAGE: load.py filename")
    exit(1)

filename = sys.argv[1]

word_query = "MERGE (w:Word {{body: '{}', len: {}}}) " +\
             "ON CREATE SET w.freq = 1 " +\
             "ON MATCH SET w.freq = w.freq + 1" 

clue_query = "MERGE (c:Clue {{body: '{}'}})"
rel_query = "MATCH(w:Word {{body:'{}'}}) WITH w " +\
            "MATCH (c:Clue {{body:'{}'}})" +\
            "MERGE (c)-[:DESCRIBES]->(w)"

# Create nodes for a single word, clues pair
def create_nodes(session, word, clues):
    if len(word) < 3 or len(word) > 23:
        return
    # session.run(word_query.format(word, len(word))) # word node
    for clue in clues:
        if clue.strip() == "":
            continue
        session.run(clue_query.format(clue)) # clue node
        session.run(rel_query.format(word, clue)) # word-clue relation

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