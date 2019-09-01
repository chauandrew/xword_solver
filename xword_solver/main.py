import json
from neo4j import GraphDatabase
import re

from board import Board
from solver import XwordSolver




filename = "/home/achau/xword_solver/boards/20180804.json"
solver = XwordSolver(filename)
# print( solver.get_clue(1, 'ACROSS').hint)
# print( solver.query_clue(1, 'ACROSS'))
# print( solver.query_word(1, 'ACROSS'))
solver.solve()
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