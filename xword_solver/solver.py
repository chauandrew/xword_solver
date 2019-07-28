import json
import board

class XwordSolver():
    def __init__(self, boardfile):
        with open(boardfile, "r") as f:
            data = json.load(f)
        self.solution = Board(data.size.rows, data.size.cols, data.grid, data.gridnums) 
        self.board = self.solution.get_empty_board()
        clue_re - re.compile(r"(\d+). (.*)")
        self.clues = {'across': {}, 'down': {}}
        for clue in data['clues']['across']:
            clue = clue_re.search(clue)
            self.clues['across'][clue.group(1)] = clue.group(2)
        for clue in data['clues']['down']:
            clue = clue_re.search(clue)
            self.clues['down'][clue.group(1)] = clue.group(2)
        