from neo4j import GraphDatabase
import json
import sys
import os

# TODO: Build thing to create regex
if len(sys.argv) != 2:
    print("USAGE: load.py folderpath")
    exit(1)

folderpath = sys.argv[1]
files = [file for file in os.listdir(folderpath) if file.endswith(".json")]

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
    # Create node for word
    session.run(word_query.format(word, len(word)))
    for clue in clues:
        session.run(clue_query.format(clue))
        session.run(rel_query.format(word, clue))

# connect to database and load 
if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("xword", "xword"))

    with driver.session() as session:
        with open(f"{folderpath}/{files[0]}", "r") as f:
            data = json.load(f)
        for word, clues in data.items():
            create_nodes(session, word, clues)

    driver.close()