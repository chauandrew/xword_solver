import json
from board import Board
from neo4j import GraphDatabase
import re

class XwordSolver():
    def __init__(self, boardfile):
        with open(boardfile, "r") as f:
            data = json.load(f)
        self.solution = Board(data['size']['rows'], data['size']['cols'], data['grid'], data['gridnums']) 
        self.board = self.solution.get_empty_board()
        clue_re = re.compile(r"(\d+). (.*)")
        self.clues = {'across': {}, 'down': {}}
        for clue in data['clues']['across']:
            clue = clue_re.search(clue)
            self.clues['across'][clue.group(1)] = clue.group(2)
        for clue in data['clues']['down']:
            clue = clue_re.search(clue)
            self.clues['down'][clue.group(1)] = clue.group(2)
        options = {'across': {}, 'down': {}}
        uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(uri, auth=("xword", "xword"))
    
    def __del__(self):
        self.driver.close()

    def query_word(self, clue, pattern):
        pattern = pattern.replace('_', '.').upper()
        by_clue = lambda tx, clue: \
            tx.run( "MATCH (c:Clue)-[:DESCRIBES]->(w:Word) "
                    "WHERE c.body = $clue "
                    "RETURN w.body", clue=clue)
        by_word = lambda tx, clue: \
            tx.run( "MATCH (w:Word) "
                    "WHERE w.length = $len "
                    "AND w.body =~ $ptn RETURN w.body", 
                    len=len(pattern), ptn=pattern)
        with self.driver.session() as session:
            words = session.read_transaction(by_clue, clue.upper())
            words = [word['w.body'] for word in words]
            words = list(filter(lambda x: re.search(f'^{pattern}$', x), words))
            if words: 
                return words
            words = session.read_transaction(by_word, pattern)
            words = [word['w.body'] for word in words]
            return list(filter(lambda x: re.search(f'^{pattern}$', x), words))


    # def gen_initial_words(self):