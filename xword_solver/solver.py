import json
from neo4j import GraphDatabase
import re
import queue
import html

from board import Board
from clue import Clue


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
            self.clues[(clue.group(1), 'ACROSS')] = \
                (Clue(clue.group(1), 'ACROSS', 
                hint=html.unescape(clue.group(2)),
                board=self.board))
        for clue in data['clues']['down']:
            clue = clue_re.search(clue) # 1) num, 2) clue 
            self.clues[(clue.group(1), 'DOWN')] = \
                (Clue(clue.group(1), 'DOWN', 
                hint=html.unescape(clue.group(2)),
                board=self.board))
        uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(uri, auth=("xword", "xword"))
    
    def __del__(self):
        self.driver.close()
    
    def get_clue(self, num, direction):
        return self.clues[(str(num), direction.upper())]

    def query_clue(self, num, direction):
        with self.driver.session() as session:
            return self.get_clue(num, direction).query_clue(session, self.board)

    def query_word(self, num, direction):
        with self.driver.session() as session:
            return self.get_clue(num, direction).query_word(session, self.board)

    # first attempt at solving a board (v. basic)
    def solve(self):
        firstpass = queue.Queue()
        secondpass = queue.Queue()
        count = 0
        [firstpass.put(clue) for clue in self.clues.keys()]
        while not firstpass.empty():
            curr = firstpass.get(False)
            num = curr[0]
            direction = curr[1]
            matches = self.query_clue(num, direction)
            if not matches:
                secondpass.put(curr)
                count += 1
            elif len(matches) == 1:
                print(curr, matches[0])
                self.board.set_word(num, direction, matches[0])
            else:
                firstpass.put(curr)

        # TODO: Implement a real algorithm 
        # Notes: abbrev's could be 'in brief' or 'for short' 
        for _ in range(count << 1):
            if secondpass.empty():
                break
            curr = secondpass.get(False)
            num = curr[0]   
            direction = curr[1]
            matches = self.query_word(num, direction)
            if not matches:
                # probably recursive step base case
                pass
            elif len(matches) == 1:
                print(curr, matches[0])
                self.board.set_word(num, direction, matches[0])
            else:
                secondpass.put(curr)

        self.board.print_board()
        self.solution.print_board()







