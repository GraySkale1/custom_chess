import math

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

class movement():
    """describes a desired movement as a starting position and vector expressed in index form"""
    def __init__(self, start:list, vector:list, exe:bool):
        self.start = start
        self.vector = vector
        self.exe = exe #if move takes a piece or not


class board():
    def __init__(self):
        self.piece_d = {x().identifier: x for x in piece.__subclasses__()}
        self.current_pieces = []
        self.chess_board = [[None for x in range(8)] for y in range(8)]
        self.piece_pos = [] #list of indexes of pices on board
        self.turn = 0
        self.first = 1

    def _distance(self, vector:list):
        """
        returns rounded down distance from center of vector
        """
        return math.sqrt(vector[0]**2 + vector[0]**2)
    
    def movement_val(self, move:movement) -> bool:
        """
        Returns True if movement is valid, returns False otherwise
        """
        if c_piece:=self._lookup(move.start, back=1) == False:
            return False
        
        if 
        

                
        
    def _val_vector(self, direct:piece, move:movement, path_back:bool = 0):

        """
        Checks if disired movement of piece matches existing piece vector as bool.\n
        If path_back = 1: returns the function that matched the vector or outputs 0 if none found
        """
        if move.axis == 0:
            for path in direct.xmovement:
                if path(move.vector[0]) == move.vector[1] and self._distance(move.vector) <= direct.distance:
                    if path_back == 1:
                        return path
                    return True
        
        else:
            for path in direct.ymovement:
                if path(move.vector[1]) == move.vector[0] and self._distance(move.vector) <= direct.distance:
                    if path_back == 1:
                        return path
                    return True
            
        if move.exe == 1:
            if move.axis == 0:
                for path in direct.xxmovement:
                    if path(move.vector[0]) == move.vector[1] and self._distance(move.vector) <= direct.distance:
                        if path_back == 1:
                            return path
                        return True
            
            else:
                for path in direct.xymovement:
                    if path(move.vector[1]) == move.vector[0] and self._distance(move.vector) <= direct.distance:
                        if path_back == 1:
                            return path
                        return True
            
        return 0

    def _jump_check(self, move:movement, obj:piece) -> bool:
        """
        Checks if there is a piece between movement
        """
        if obj.jump == True:
            possible_piece = self._lookup(move.start + move.vector, back=1)
            if isinstance(possible_piece, piece) and :
                return possible_piece.team^obj.team
            


        obsticles = 0
        for px in range(move.vector[0]): #iterates across x of vector
            for py in range(move.vector[1]): #iterates across y
                pos = move.start + [px,py]
                obsticles += self._lookup(pos)
        
        if obsticles == 0:
            return True
        else:
            return False



    def _lookup(self, index:list, back:bool = 0):
        """
        checks if piece exists in the indexed position.\n
        if back = 1, returns instead the piece it indexes
        """
        if isinstance(self.chess_board[index], piece):
            if back == 1:
                return self.chess_board[index]
            else:
                return True
        else:
            return False


    def piece_lookup(self, index:list,):
        """
        Returns indexes of pieces that can reach input index
        """
        for index in self.piece_pos:
           self._val_vector()
            



    
    def _decode(self, notation:str) -> list:
        """
        Takes in standard chess notation as string and returns a vector and starting position
        """
        piece_key = notation[0]
        target_pos = notation[-2::]
        
    def _vector(self, start:list, target:list):
        final = [0,0]
        for i,value in enumerate(zip(start, target)):
            final[i] = value[1] - value[0]
        return final