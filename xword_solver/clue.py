import json
from board import Board
from neo4j import GraphDatabase
import re
import queue

# class to organize clues and words
class Clue():
    def __init__(self, num, direction, hint = None, board = None):
        self.num = num
        self.dir = direction.upper()
        self.hint = hint.upper() if hint else None
        self.ptrn = board.get_word(num, direction) if board else None
        self.matches = []

    # define gt and lt for sorting
    def __lt__(self, other):
        return (self.ptrn(count('_'))/len(self.ptrn) < other.ptrn(count('_'))/len(other.ptrn))
    def __gt__(self, other):
        return (self.ptrn(count('_'))/len(self.ptrn) > other.ptrn(count('_'))/len(other.ptrn))
    # define eq and hash for hash tables 
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.num == other.num and self.dir == other.dir)
    def __hash__(self):
        return hash(self.num) + hash(self.dir)

    # update a clues' pattern over time. 
    def update_ptrn(self, board):
        self.ptrn = board.get_word(self.num, self.dir)

    # Get current matches for a word
    def get_matches(self):
        return self.matches

    # query a word by matching clue patterns 
    def query_clue(self, session, board):
        self.update_ptrn(board)
        pattern = re.compile(f"^{self.ptrn.replace('_', '.')}$")
        by_clue = lambda tx, clue: \
            tx.run( "MATCH (c:Clue)-[:DESCRIBES]->(w:Word) "
                    "WHERE c.body = $clue "
                    "RETURN w.body", clue=clue)

        words = session.read_transaction(by_clue, self.hint)
        words = [word['w.body'] for word in words]
        self.matches = list(filter(lambda x: pattern.match(x), words))
        return self.matches

    # query a word by matching clue patterns 
    def query_word(self, session, board):
        self.update_ptrn(board)
        pattern = re.compile(f"^{self.ptrn.replace('_', '.')}$")
        by_word = lambda tx: \
            tx.run( "MATCH (w:Word) "
                    "WHERE w.length = $len "
                    "AND w.body =~ $ptn RETURN w.body", 
                    len=len(self.ptrn), ptn=self.ptrn.replace('_', '.'))
        words = session.read_transaction(by_word)
        words = [word['w.body'] for word in words]
        self.matches = list(filter(lambda x: pattern.match(x), words))
        return self.matches
