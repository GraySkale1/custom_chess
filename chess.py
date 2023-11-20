import math
import base
from piece_class import piece

class ChessException(Exception):
    def __init__(self, message):
        self.message = message



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

        if 'x' in notation:
            execute = True
            notation = notation.replace("x", "") #removes x to make interpretion of disambiguators easier

        if notation[0] not in self.piece_d.keys():
            notation = 'p' + notation

        elif len(notation) == 2:
            notation = 'p' + notation


        char_piece = notation[0]
        target = self._notate_to_index(notation[-2::])
        execute = False
        start = None


        if len(notation) == 5: #checks if disambiguator gives full corrdinate
            start = self._notate_to_index(notation[1:-2])

        elif len(notation) == 4:
            for p1, p2 in self.piece_pos:
                # checks if digit in disambiguator appears in any of the current piece position then checks if it is the described piece
                if self._notate_to_index(notation[1],single=True) in [p1, p2]:
                    if isinstance(self.chess_board[p1][p2], self.piece_d[char_piece]):
                        start = [p1, p2]
                        break

        else:
            for p in self.piece_lookup(target=target)
        
        if start == None:
            return 0
        vec = self._vector(start=start, target=target)
            
        return movement(start=start, vector=vec, exe=execute, team=self.turn % 2)
        
            
    
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

        if move.exe == True:
            print(f'{temp.identifier} takes {self.chess_board[t1][t2].identifier}')

        if t1 == temp.team * 7: #funny epic hack
            premotion = temp.promote()
            if (premotion != 0) and (premotion.lower() in self.piece_d.keys()):
                promotion_shell = self.piece_d[premotion.lower()]()
                promotion_shell.past = temp.past
                temp = promotion_shell
                temp.past.append('promote placeholder')


        self.chess_board[t1][t2] = temp

        p = self.piece_pos.index(move.start)
        self.piece_pos[p] = [t1,t2] # updates position of piece on piece list


        self.turn += 1

        return True
    

    
    def piece_lookup(self, target:list):
        """
        generator that returns movement objects of pieces that can be moved to that position
        """
        takes = False
        if issubclass(self.chess_board[target[0]][target[1]], piece):
            takes = True
            e_team = self.chess_board[target[0]][target[1]].team


        for piece_index in self.piece_pos:
            vector = self._vector(piece_index)
            if takes == True:
                temp =  movement(start=piece_index, vector=vector, exe=1, team=)
            else:
                temp = movement(start=piece_index, vector=vector, exe=0, team=team)

            if self.movement_val(temp) == True:
                yield temp



    
    def movement_val(self, move:movement) -> bool:
        """
        Returns True if movement is valid, returns False otherwise
        """
        if isinstance(move, movement) == 0:
            return False
        
        c_piece = self._lookup(move.start, back=1)
        if c_piece == False:
            return False
        
        vector = self._val_vector(direct=c_piece, move=move, path_back=1)
        if vector == False:
            return False
        
        if self._jump_check(move=move, obj=c_piece, equation=vector) == False:
            return False
        
        return True
    
    def __repr__(self):
        final = ''

        for value in self._board_iterate(repr=True):
            final += '|' + value
        
        return final



    def _jump_check(self, move:movement, obj:piece, equation:'function') -> bool:
        """
        Checks if there is a piece between movement
        """
        if obj.jump == True:
            target = self._devectorise(move.start, move.vector)
            possible_piece = self._lookup(target, back=1)
            if possible_piece == 0:
                return True
            else:
                # only returns true if teams are different using xor
                return possible_piece.team ^ obj.team
            

        obsticles = 0

        if equation in obj.xmovement or equation in obj.xxmovement: #determines which coordinate has a many to one relationship
            index = 0 
        else:
            index = 1

        #index = 0 means that postion one of the index should be iterated and vice versa
        

        for i in range(max(move.vector)):

            px = i if index == 0 else equation(i)
            py = equation(i) if index == 0 else i

            pos = [sum(x) for x in zip([px,py], move.start)]

            lookup_data = self._lookup(pos, back=1)
            if lookup_data != False:
                if id(lookup_data) != id(obj) :
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
                    if element.team ^ (self.turn % 2) == 0: #capitalises output if piece can moved this turn
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