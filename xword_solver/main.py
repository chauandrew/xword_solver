import json
from neo4j import GraphDatabase
import re

from board import Board
from solver import XwordSolver




filename = "/home/achau/github/xword_solver/boards/20160427.json"
solver = XwordSolver(filename)
print(solver.query_word("RUSH", "____"))
print("FINISHED")



# uri = "bolt://localhost:7687"
# driver = GraphDatabase.driver(uri, auth=("xword", "xword"))

# def print_friends_of(tx, clue):
#     for record in tx.run("MATCH (c:Clue)-[:DESCRIBES]->(w:Word) "
#                          "WHERE c.body = {clue} "
#                          "RETURN w.body", clue=clue):
#         print(record["w.body"])

# with driver.session() as session:
#     session.read_transaction(print_friends_of, "RUSH")

# driver.close()