import math
import random
import copy

class ChessException(Exception):
    def __init__(self, message):
        self.message = message



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

    def m_add(self, move:'movement'):
        self.past.append(move)


            
class pawn(piece):
    def __init__(self):
        super().__init__()
        self.ymovement = [lambda y: 0 if y < 0 and self.team == 0 else 999, lambda y: 0 if y > 0 and self.team == 1 else 999]
        self.xxmovement = [lambda x: -abs(x) if self.team == 1 else 999, lambda x: abs(x) if self.team == 0 else 999]
        self.distance = 2
        self.promote = True
        self.identifier = 'p'

    def m_add(self, move_desc):
        super().m_add(move_desc)
        self.distance = 1

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
    def __init__(self, start:list, vector:list, exe:bool, team:bool):
        self.start = start
        self.vector = vector
        self.team = team
        self.exe = exe #if move takes a piece or not


class board():
    def __init__(self):
        self.piece_d = {x().identifier: x for x in piece.__subclasses__()}
        self.chess_board = [[0 for x in range(8)] for y in range(8)]
        self.piece_pos = [] #list of indexes of pices on board
        self.turn = 0
        self.first = 1
    

    def full_decode(self, notation:str):
        """Takes in chess notation of a move and creates a 'movement' object that describes it"""
        notation = notation.lower()

        if notation[0] not in self.piece_d.keys():
            notation = 'p' + notation

        char_piece = str(notation[0])
        target = self._notate_to_index(notation[-2::])
        execute = False
        
        if 'x' in notation:
            execute = True
            notation.replace("x", "") #removes x to make interpretion of disambiguators easier

        if len(notation) == 5: #checks if disambiguator gives full corrdinate
            start = self._notate_to_index(notation[1:-2])

        if len(notation) == 4:
            for p1, p2 in self.piece_pos:
                # checks if digit in disambiguator appears in any of the current piece position then checks if it is the described piece
                if self._notate_to_index(notation[1],single=True) in [p1, p2]:
                    if isinstance(self.chess_board[p1][p2], self.piece_d[char_piece]):
                        start = [p1, p2]
                        break
            else:
                raise ChessException()
        
        vec = self._vector(start=start, target=target)
            
        return movement(start=start, vector=vec, exe=execute, team=self.turn)
        
            
    
    def place(self, notation:str, team:bool):
        """Takes in chess notation of: [piece][postion] and places piece at that board. \n
        team: 0 is black, 1 is white. \n
        **pieces can be overwritten using this function**"""
        if len(notation) < 3:
            notation = 'p' + notation
        piece_char = notation[0].lower()
        p1, p2 = self._notate_to_index(notation[-2::])

        piece_class = self.piece_d[piece_char]
        temp = piece_class()
        temp.team = team

        self.chess_board[p1][p2] = temp

        if [p1, p2] not in self.piece_pos:
            self.piece_pos.append([p1, p2])


    def execute(self, move:movement):
        """Executes movement object on board \n
        If move is immpossible, returns false, otherwise returns true
        """
        if self.movement_val(move) != True:
            print("Invalid chess move")
            return False
        
        temp = self.chess_board[move.start[0]][move.start[1]]

        temp.m_add(move)

        self.chess_board[move.start[0]][move.start[1]] = 0

        t1, t2 = self._devectorise(start=move.start, vector=move.vector) #finds end point of move
        self.chess_board[t1][t2] = temp

        p = self.piece_pos.index(move.start)
        self.piece_pos[p] = [t1,t2] # updates position of piece on piece list

        self.turn += 1


        return True
    

    
    def piece_lookup(self, index:list):
        """
        Returns indexes of pieces that can reach input index
        """
        raise NotImplementedError


    
    def movement_val(self, move:movement) -> bool:
        """
        Returns True if movement is valid, returns False otherwise
        """
        c_piece = self._lookup(move.start, back=1)
        if c_piece == False:
            return False
        
        if self._val_vector(direct=c_piece, move=move) == False:
            return False
        
        if self._jump_check(move=move, obj=c_piece) == False:
            return False
        
        return True
    
    def __repr__(self):
        final = ''

        for value in self._board_iterate(repr=True):
            final += '|' + value
        
        return final



    def _jump_check(self, move:movement, obj:piece) -> bool:
        """
        Checks if there is a piece between movement
        """
        if obj.jump == True:
            possible_piece = self._lookup(move.start + move.vector, back=1)
            if issubclass(type(possible_piece), piece) == 0:
                return True
            else:
                return possible_piece.team^obj.team
            

        obsticles = 0
        for px in range(move.vector[0]+1): #iterates across x of vector
            for py in range(move.vector[1]+1): #iterates across y
                pos = [sum(x) for x in zip(move.start,[px,py])]

                lookup_data = self._lookup(pos, back=1)
                if lookup_data != True and id(lookup_data) != id(obj):
                    obsticles += 1
        
        if obsticles == 0:
            return True
        else:
            return False

    def _board_iterate(self, repr:bool=False):
        """
        Yeilds raw board data in order from row 8 (board notation) downwards.\n
        Outputs identifier of piece instead of object is 'repr = true'
        """
        for row in self.chess_board:
            for element in row:
                if issubclass(type(element), piece) and repr == True:
                    if element.team ^ self.turn == 0: #capitalises output if piece can moved this turn
                        yield element.identifier.upper()
                    else:
                        yield element.identifier

                elif repr == True and element == 0:
                    yield ' '
                else:
                    yield element
            
            if repr == True:
                yield '\n'




    def _lookup(self, index:list, back:bool = 0):
        """
        checks if piece exists in the indexed position.\n
        if back = 1, returns instead the raw data of the piece it indexes \n
        always returns false if no piece is found
        """
        p1, p2 = index
        if issubclass(type(self.chess_board[p1][p2]), piece):
            if back == 1:
                return self.chess_board[p1][p2]
            else:
                return True
        else:
            return False
        
    def _distance(self, vector:list):
        """
        returns rounded down distance from center of vector
        """
        return math.sqrt(vector[0]**2 + vector[1]**2)


    def _devectorise(self, start:list, vector:list):
        """Returns the index of the target position by adding vector to start"""
        final = []
        for total in zip(start, vector):
            final.append(sum(total))
        
        return final
        

    def _val_vector(self, direct:piece, move:movement, path_back:bool = 0):

        """
        Checks if disired movement of piece matches existing piece vector as bool.\n
        If path_back = 1: returns the function that matched the vector or outputs 0 if none found
        """

        for path in direct.xmovement:
            if path(move.vector[1]) == move.vector[0]:
                if self._distance(move.vector) <= direct.distance:
                    if path_back == 1:
                        return path
                    return True
    

        for path in direct.ymovement:
            if path(move.vector[0]) == move.vector[1]:
                if self._distance(move.vector) <= direct.distance:
                    if path_back == 1:
                        return path
                    return True
            
        if move.exe == 1:
            for path in direct.xxmovement:
                if path(move.vector[1]) == move.vector[0]:
                    if self._distance(move.vector) <= direct.distance:
                        if path_back == 1:
                            return path
                        return True
        

            for path in direct.xymovement:
                if path(move.vector[0]) == move.vector[1]:
                    if self._distance(move.vector) <= direct.distance:
                        if path_back == 1:
                            return path
                        return True
            
        return 0


    def _notate_to_index(self, notation:str, single:bool=0) -> list:
        """Takes in position in chess notation and outputs index on board \n
        if single = True, notation takes in one int or str value, returns index of that single value"""
        notation = str(notation).lower()
        if single == True:
            if isinstance(notation, str):
                return int(ord(notation) - ord('a'))
            else:
                return 8 - int(notation[1])
        part1 = 8 - int(notation[1])
        part2 = ord(notation[0]) - ord('a')
        return [part1, part2]

    
    def _decode(self, notation:str) -> list:
        """
        Takes in standard chess notation as string and returns a vector and starting position
        """
        piece_key = notation[0]
        target_pos = notation[-2::]
        raise NotImplementedError
        
    def _vector(self, start:list, target:list):
        final = [0,0]
        for i,value in enumerate(zip(start, target)):
            final[i] = value[1] - value[0]
        return final