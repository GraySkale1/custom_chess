import numpy


class ChessException(Exception):
    pass

def index_2_obj(myList:list, v):
    for i, x in enumerate(myList):
        for y in x:
            if isinstance(y, v):
                return (i, x.index(v))



class piece():
    def __init__(self):
        self.xmovement = []
        self.ymovement = []
        self.past = []
        self.xxmovement = []
        self.xymovement = []
        self.distance = 999
        self.jump = False
        self.promote = False
        self.team = 1   # 1 - white, 0 - black
        self.identifier = ''

    def special_logic(self):
        pass


            
class pawn(piece):
    def __init__(self):
        super().__init__()
        self.ymovement = [lambda y: 0 if self.team == 1 and y <= 0 else 999, lambda y: 0 if self.team == 0 and y >= 0 else 999]
        self.xxmovement = [lambda x: -abs(x) if self.team == 1 else 999, lambda x: abs(x) if self.team == 0 else 999]
        self.distance = 2
        self.promote = True
        self.identifier = 'p'


class rook(piece):
    def __init__(self):
        super().__init__()
        self.xmovement = [lambda x: 0]
        self.ymovement = [lambda y: 0]
        self.identifier = 'r'

class bishop(piece):
    def __init__(self):
        super().__init__()
        self.xmovement = [lambda x: x, lambda x: -x]
        self.identifier = 'b'

class knight(piece):
    def __init__(self):
        super().__init__()
        self.xmovement = [lambda x: x*2, lambda x: -x*2]
        self.ymovement = [lambda y: y*2, lambda y: -y*2]
        self.distance = 1
        self.jump = True
        self.identifier = 'n'



class action():
    def __init__(self, start_pos:list, end_pos:list, board:'board',  special:int = 0, exe:bool = False): #special denotes actions like castling, will have dictionary
        if special == 0:
            self.action_position = start_pos
            self.final_position = end_pos
            self.exe = exe

            if board.chess_board[self.action_position] == 0: #checks if there is a valid piece assigned
                raise ChessException("Action given null piece")
            else:
                self.action_piece = board.piece_d[board.chess_board[self.action_position]]

        self.special = 0

    def run(self, board:'board'):
        if self.exe:
            del board.chess_board[self.final_position]

        board.chess_board[self.final_position] = board.chess_board[self.final_position]
        board.chess_board[self.final_position] == None

        self.action_piece.past.append(memory(self))

class memory():
    def __init__(self, mem:action):
        self.start_pos = mem.action_position
        self.end_pos = mem.final_position
        self.kill = mem.exe



class board():
    def __init__(self):
        self.piece_d = {x().identifier: x for x in piece.__subclasses__()}
        self.current_pieces = []
        self.chess_board = [[None for x in range(8)] for y in range(8)]
        self.turn = 0
        self.first = 1


    def lookup(self, target:piece):
        possible_index = []
        copy = self.chess_board
        #
        while any(isinstance(sublist, target) in sublist for sublist in copy):
            possible_index.append(index_2_obj(target)) #looks for position of first instance of object
            copy[possible_index[-1]] = None
    
    def _decode(self, notation:str) -> 'action':
        plain_piece = notation[0]
        position = 
        





