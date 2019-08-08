import json
from board import Board
from neo4j import GraphDatabase
import re
import queue

class XwordSolver():
    def __init__(self, boardfile):
        with open(boardfile, "r") as f:
            data = json.load(f)
        self.solution = Board(data['size']['rows'], data['size']['cols'], data['grid'], data['gridnums']) 
        self.board = self.solution.get_empty_board()
        clue_re = re.compile(r"(\d+). (.*)")
        self.clues = {}
        for clue in data['clues']['across']:
            clue = clue_re.search(clue) # 1) num, 2) clue 
            self.clues[int(clue.group(1))] = {
                'ptrn': clue.group(2),
                'across': True
                'matches': self.query_clue(clue.group(2), 
                                self.board.get_word(clue.group(2), 'ACROSS'))
            }
        for clue in data['clues']['down']:
            clue = clue_re.search(clue) # 1) num, 2) clue 
            self.clues[int(clue.group(1))] = {
                'ptrn': clue.group(2),
                'down': True
                'matches': self.query_clue(clue.group(2), 
                                self.board.get_word(clue.group(2), 'DOWN'))
            }
        uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(uri, auth=("xword", "xword"))
    
    def __del__(self):
        self.driver.close()
    
    # query a word by matching clue patterns 
    def query_clue(self, clue, pattern):
        pattern = pattern.replace('_', '.').upper()
        by_clue = lambda tx, clue: \
            tx.run( "MATCH (c:Clue)-[:DESCRIBES]->(w:Word) "
                    "WHERE c.body = $clue "
                    "RETURN w.body", clue=clue)
        with self.driver.session() as session:
            words = session.read_transaction(by_clue, clue.upper())
            words = [word['w.body'] for word in words]
            return list(filter(lambda x: re.search(f'^{pattern}$', x), words))

    # query a word by matching word patterns 
    def query_word(self, clue, pattern):
        pattern = pattern.replace('_', '.').upper()
        by_word = lambda tx, clue: \
            tx.run( "MATCH (w:Word) "
                    "WHERE w.length = $len "
                    "AND w.body =~ $ptn RETURN w.body", 
                    len=len(pattern), ptn=pattern)
        with self.driver.session() as session:
            words = session.read_transaction(by_word, pattern)
            words = [word['w.body'] for word in words]
            return list(filter(lambda x: re.search(f'^{pattern}$', x), words)

    # first attempt at solving a board (v. basic)
    def solve(self):
        # put words in queue ordered by number of matches available
        tosolve = queue.Queue(maxsize=len(self.clues) + 10)
        map(tosolve.put, sorted(self.clues.items(), key=(lambda x: len(x[1]['matches']))))
         
         








