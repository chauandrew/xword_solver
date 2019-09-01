import copy

sample_letters=["S","T","R","A","W",".",".","B","A","S","S",".","C","S","I","O","R","I","S","I","T",".","A","B","L","E",".","R","E","N","M","O","B","I","L","E",".","Y","E","A","R",".","A","P","P","A","D","S","A","L","E","S",".","T","V","M","O","V","I","E",".",".",".","M","I","N","A","J",".",".","O","C","E","A","N","A","D","A",".","A","S","T","U","D","E","N","T",".",".",".","R","E","A","L","M",".","A","M","I","S",".","O","B","I","E","E","C","H","O",".","O","N","P","O","P",".","P","A","R","K","S","O","S","O",".","P","I","E","R",".","G","I","J","O","E",".",".",".","P","E","T","C","R","A","T","E",".","A","N","D","I","N","D","E","X",".",".","S","M","A","R","T",".",".",".","T","O","R","R","E","N","T",".","A","R","M","O","I","R","E","S","K","I",".","T","O","W","N",".","P","A","T","R","O","L","O","I","L",".","E","R","I","E",".","S","N","E","A","K","S","K","A","L",".","R","I","T","Z",".",".","E","S","Q","U","E"]
sample_numbers = [1,2,3,4,5,0,0,6,7,8,9,0,10,11,12,13,0,0,0,0,14,0,15,0,0,0,0,16,0,0,17,0,0,0,0,0,0,18,0,0,0,0,19,0,0,20,0,0,0,0,0,21,0,22,0,0,23,0,0,0,0,0,0,24,0,0,0,25,0,0,26,0,0,0,0,27,28,29,0,30,0,0,0,31,32,0,0,0,0,0,33,0,0,34,0,0,35,0,0,0,0,36,37,38,39,40,0,0,0,0,41,0,0,0,0,0,42,0,0,0,43,0,0,0,0,44,0,0,0,0,45,0,0,0,0,0,0,0,46,47,0,0,0,0,48,0,0,49,0,0,50,51,52,0,0,0,0,53,0,0,0,54,0,0,0,55,0,0,0,0,56,57,0,58,0,0,0,59,60,61,62,0,0,0,63,0,0,64,0,65,0,0,0,0,0,66,0,0,0,67,0,0,0,0,68,0,0,0,0,0,69,0,0,0,70,0,0,0,0,0,71,0,0,0,0]

#TODO: Write a comparison operator 

LETTER = 0
BLACK  = 1

# Class to represent each square of a board
class Cell():
    def __init__(self, kind, letter):
        self.kind = kind    # either black or letter
        self.letter = letter # letter for printing / id
        self.across = None  # which across row the cell is in
        self.down = None    # whihc down row the cell is in
    
    def isBlack(self):
        return bool(self.kind == BLACK)

# Class to represent a board 
class Board:
    def __init__(self, ht, wi, letters, numbers):
        self.height = ht
        self.width = wi
        self.grid = []
        self.clue_index = {'across': {}, 'down': {}} # clues solved
        self.unsolved = {'across': set(), 'down': set()} # clues not solved yet
        clues = [] # array to hold indices of clues
        # Create grid for letters and numbers
        for i, (let, num) in enumerate(zip(letters, numbers)):
            if let == '.':
                self.grid.append(Cell(BLACK, let))
            elif num == 0:
                self.grid.append(Cell(LETTER, let))
            else:
                self.grid.append(Cell(LETTER, let))
                clues.append(i)
        # Assign across/down metainfo for each cell 
        for cluenum, index in enumerate(clues):
            cluenum += 1 # array starts 0, clues start at 1
            i = index
            # across tiles
            if (i % wi) == 0 or self.grid[i - 1].letter == '.':
                self.clue_index['across'][cluenum] = index
                while i < len(self.grid) and self.grid[i].letter != '.':
                    self.grid[i].across = cluenum
                    i += 1
            # down tiles
            i = index
            if i - wi < 0 or self.grid[i - wi].letter == '.':
                self.clue_index['down'][cluenum] = index
                while i < len(self.grid) and self.grid[i].letter != '.':
                    self.grid[i].down = cluenum
                    i += wi


    def print_board(self):
        for i, tile in enumerate(self.grid):
            if i % self.height == 0: 
                print('')
            print(tile.letter, end=" ")
        print('')

    # Returns a deep copy of the board, but without letter  values
    def get_empty_board(self):
        empty = copy.deepcopy(self)
        for tile in empty.grid:
            if not tile.isBlack():
                tile.letter = '_'
        for cluenum, _ in empty.clue_index['across'].items():
            empty.unsolved['across'].add(cluenum)
        for cluenum, _ in empty.clue_index['down'].items():
            empty.unsolved['down'].add(cluenum)
        return empty

    # 0,0 is top left corner, get cell from x,y coords
    # can also set y=0 and get cell by single array index
    def get_cell(self, x, y):
        idx = x + self.height * y
        return self.grid[idx] if idx < len(self.grid) else None

    # Get a word by number
    def get_word(self, num, kind):
        num = int(num)
        if kind.upper() == "ACROSS": 
            if num not in self.clue_index['across']:
                return ""
            index = self.clue_index['across'][num]
            offset = 1
        elif kind.upper() == "DOWN": 
            if num not in self.clue_index['down']:
                return ""
            index = self.clue_index['down'][num]
            offset = self.width
        else:
            return ""
        word = ""
        while index < len(self.grid) and self.grid[index].letter != '.':
            word += self.grid[index].letter
            index += offset
            if index % self.width == 0:
                break
        return word

    # Place word in board and return list of numbers affected.
    # Return false if word doesn't match existing characters
    def set_word(self, num, kind, word):
        # check existing word pattern exists and matches suggested word
        existing = self.get_word(num, kind)
        word = word.upper()
        if len(word) != len(existing):
            return False
        elif word == existing: 
            return []
        for new, old in zip(word, existing):
            if new != old and old != '_':
                return False
        # setup variables
        if kind.upper() == "DOWN": 
            index = self.clue_index['down'][int(num)]
            offset = self.width
        elif kind.upper() == "ACROSS": 
            index = self.clue_index['across'][int(num)]
            offset = 1
        else:
            return False
        updated = []
        # assign word in grid and remove it from unsolved list
        for i, letter in enumerate(word):
            self.grid[index + i * offset].letter = letter
            if offset == 1: # if across clu
                updated.append(self.grid[index + i * offset].down)
            else: # if down clue
                updated.append(self.grid[index + i * offset].across)
        self.unsolved[kind.lower()].discard(num)
        del updated[0] # first number points to clue we just set
        # Check if we completed other words, and return a list of clues updated
        for cluenum in updated.copy():
            if kind.upper() == "DOWN":
                if '_' not in self.get_word(cluenum, 'ACROSS'):
                    self.unsolved['across'].discard(cluenum)
                    updated.remove(cluenum)
            else: # across
                if '_' not in self.get_word(cluenum, 'DOWN'):
                    self.unsolved['down'].discard(cluenum)
                    updated.remove(cluenum)
        return updated 

    # return dict of across and down clues left
    def clues_left(self):
        return self.unsolved
