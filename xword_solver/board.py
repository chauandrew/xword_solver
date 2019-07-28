import copy

sample_letters=["S","T","R","A","W",".",".","B","A","S","S",".","C","S","I","O","R","I","S","I","T",".","A","B","L","E",".","R","E","N","M","O","B","I","L","E",".","Y","E","A","R",".","A","P","P","A","D","S","A","L","E","S",".","T","V","M","O","V","I","E",".",".",".","M","I","N","A","J",".",".","O","C","E","A","N","A","D","A",".","A","S","T","U","D","E","N","T",".",".",".","R","E","A","L","M",".","A","M","I","S",".","O","B","I","E","E","C","H","O",".","O","N","P","O","P",".","P","A","R","K","S","O","S","O",".","P","I","E","R",".","G","I","J","O","E",".",".",".","P","E","T","C","R","A","T","E",".","A","N","D","I","N","D","E","X",".",".","S","M","A","R","T",".",".",".","T","O","R","R","E","N","T",".","A","R","M","O","I","R","E","S","K","I",".","T","O","W","N",".","P","A","T","R","O","L","O","I","L",".","E","R","I","E",".","S","N","E","A","K","S","K","A","L",".","R","I","T","Z",".",".","E","S","Q","U","E"]
sample_numbers = [1,2,3,4,5,0,0,6,7,8,9,0,10,11,12,13,0,0,0,0,14,0,15,0,0,0,0,16,0,0,17,0,0,0,0,0,0,18,0,0,0,0,19,0,0,20,0,0,0,0,0,21,0,22,0,0,23,0,0,0,0,0,0,24,0,0,0,25,0,0,26,0,0,0,0,27,28,29,0,30,0,0,0,31,32,0,0,0,0,0,33,0,0,34,0,0,35,0,0,0,0,36,37,38,39,40,0,0,0,0,41,0,0,0,0,0,42,0,0,0,43,0,0,0,0,44,0,0,0,0,45,0,0,0,0,0,0,0,46,47,0,0,0,0,48,0,0,49,0,0,50,51,52,0,0,0,0,53,0,0,0,54,0,0,0,55,0,0,0,0,56,57,0,58,0,0,0,59,60,61,62,0,0,0,63,0,0,64,0,65,0,0,0,0,0,66,0,0,0,67,0,0,0,0,68,0,0,0,0,0,69,0,0,0,70,0,0,0,0,0,71,0,0,0,0]


LETTER = 0
BLACK  = 1

class Cell():
    def __init__(self, kind, letter):
        self.type = kind    # either black or letter
        self.letter = letter # letter for printing / id
        self.across = None  # which across row the cell is in
        self.down = None    # whihc down row the cell is in
    
    def isBlack(self):
        return bool(self.type == BLACK)

# TODO: redo
class Board:
    def __init__(self, ht, wi, letters, numbers):
        self.height = ht
        self.width = wi
        self.grid = []
        self.nums = [None] # holds index of grid clues
        self.solved = {'across': set(), 'down': set()} # clues solved
        self.tosolve = {'across': set(), 'down': set()} # clues not solved yet
        # Create grid for letters and numbers
        for i, (let, num) in enumerate(zip(letters, numbers)):
            if let == '.':
                self.grid.append(Cell(BLACK, let))
            elif num == 0:
                self.grid.append(Cell(LETTER, let))
            else:
                self.grid.append(Cell(LETTER, let))
                self.nums.append(i)
        # Assign across/down metainfo for each cell 
        for cluenum, i in enumerate(self.nums):
            if i == None: continue
            # across tiles
            index = i
            if (index % wi) == 0 or self.grid[index - 1].letter == '.':
                self.solved['across'].add(cluenum)
                while index < len(self.grid) and self.grid[index].letter != '.':
                    self.grid[index].across = cluenum
                    index += 1
            # down tiles
            index = i
            if index - wi < 0 or self.grid[index - wi].letter == '.':
                self.solved['down'].add(cluenum)
                while index < len(self.grid) and self.grid[index].letter != '.':
                    self.grid[index].down = cluenum
                    index += wi


    def print_board(self):
        for i, tile in enumerate(self.grid):
            if i % self.height == 0: 
                print('')
            print(tile.letter, end=" ")
        print('')

    # TODO: redo    
    # Returns a deep copy of the board, but without letter  values
    def get_empty_board(self):
        empty = copy.deepcopy(self)
        for tile in empty.grid:
            if not tile.isBlack():
                tile.letter = '_'
        empty.solved = {'across': set(), 'down': set()} 
        empty.tosolve['across'].update(self.solved['across']) # solved + unsolved = all
        empty.tosolve['down'].update(self.solved['down'])
        return empty

    # 0,0 is top left corner, get cell from x,y coords
    # can also set y=0 and get cell by single array index
    def get_cell(self, x, y):
        idx = x + self.height * y
        return self.grid[idx] if idx < len(self.grid) else None

    # TODO: Redo
    # Get a word by number
    def get_word(self, num, kind):
        index = self.nums[num] 
        if kind.upper() == "ACROSS": 
            if num != self.grid[index].across:
                return ""
            offset = 1
        elif kind.upper() == "DOWN": 
            if num != self.grid[index].down:
                return ""
            offset = self.width
        else:
            return ""
        word = ""
        while  index < len(self.grid) and self.grid[index].letter != '.':
            word += self.grid[index].letter
            index += offset
        return word

    # TODO: redo
    # Place word in board and return list of numbers affected.
    # Return false if word doesn't match existing characters
    def set_word(self, num, kind, word):
        # check existing word
        existing = self.get_word(num, kind)
        if len(word) != len(self.get_word(num, kind)):
            return False
        for new, old in zip(word, existing):
            if new != old and old != '_':
                return False

        if kind.upper() == "ACROSS": 
            offset = 1
        elif kind.upper() == "DOWN": 
            offset = self.width
        else:
            return False
        index = self.nums[num]
        updated = []
        for i, letter in enumerate(word):
            self.grid[index + i * offset].letter = letter
            if offset == 1: # across, but faster than text search
                updated.append(self.grid[index + i * offset].down)
            else:
                updated.append(self.grid[index + i * offset].across)
        try: 
            if kind.upper() == "DOWN":
                self.solved['down'].add(i)
                self.tosolve['down'].remove(i)
            else:
                self.solved['across'].add(i)
                self.tosolve['across'].remove(i)
        except: 
            pass
        
        return updated[1:] # first index will always be input number

    # return dict of across and down clues left
    def clues_left(self):
        return self.tosolve