from neo4j import GraphDatabase
import sys

if len(sys.argv) != 3:
    print("USAGE: load_text.py filename")
    exit(1)

filename = sys.argv[1]

word_query = "WITH $words AS words " +\
            "UNWIND words AS word " +\
            "WITH word, length(word) AS length " +\
            "MERGE (w:Word: {body: word, length: length})"

# Create nodes for a list of words 
def create_nodes(session, words):
    words = [word for word in words if not (len(word) < 3 or len(word) > 23)]
    if not words:
        return
    session.run(word_query, words=words) # word node

# connect to database and load 
if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("xword", "xword"))

    with driver.session() as session:
        # open a text file with one word per line
        with open(f"{filename}", "r") as f:
            words = []
            # batch words for better performance
            for line in f.readlines():
                words.append(line.strip().upper())
                if len(words) >= 10:
                    create_nodes(session, words)
                    words = []
            create_nodes(session, words)

    driver.close()
