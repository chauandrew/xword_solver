import json
from neo4j import GraphDatabase
import re
import queue

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
                (Clue(clue.group(1), 'ACROSS', hint=clue.group(2), board=self.board))
        for clue in data['clues']['down']:
            clue = clue_re.search(clue) # 1) num, 2) clue 
            self.clues[(clue.group(1), 'DOWN')] = \
                (Clue(clue.group(1), 'DOWN', hint=clue.group(2), board=self.board))
        # for clue in data['clues']['down']:
        #     clue = clue_re.search(clue) # 1) num, 2) clue 
        #     self.clues.add(Clue(clue.group(1), 'DOWN', hint=clue.group(2), board=self.board))
        self.tosolve = queue.Queue()
        # map(self.tosolve.put, self.clues)
        for clue in self.clues:
            self.tosolve.put(clue)
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
        while not self.tosolve.empty():
            curr = self.tosolve.get(False)
            num = curr[0]
            direction = curr[1]
            matches = self.query_clue(num, direction)
            if len(matches) == 1:
                self.board.set_word(num, direction, matches[0])
            # else:
                # matches = self.query_word(curr[0], curr[1])
                # if len(matches) == 1:
                #     print(f"{self.get_clue(curr[0], curr[1]).hint}: {matches[0]}")
                # else:
                    # self.tosolve.put(curr)
        self.board.print_board()
        self.solution.print_board()







