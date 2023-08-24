

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


class board():
    def __init__(self):
        self.piece_d = {x().identifier: x for x in piece.__subclasses__()}
        self.current_pieces = []
        self.chess_board = [[None for x in range(8)] for y in range(8)]
        self.turn = 0


    def place(self, operation:str, team_af:bool):
        op_element = [*operation]
        if len(op_element) == 2:
            index = self._conv(op_element)
            piece_obj = self.piece_d['p']
        elif len(op_element) != 3:
            print('Invalid operation')
            return
        else:
            index = self._conv(op_element[1::])
            piece_obj = self.piece_d[op_element[0].lower()]
        
        if self.chess_board[index[0]][index[1]] != None:
            print('Invalid operation')
            return
        final_obj = piece_obj()
        final_obj.team = team_af

        self.chess_board[index[0]][index[1]] = final_obj
        self.current_pieces.append(final_obj)
        

    def _conv(self, notation:list): #coverts chess notation to index position
        ind_x = 8 - int(notation[1]) 
        ind_y = (ord(notation[0].lower()) - ord('a'))
        return [ind_x, ind_y]


    def __repr__(self):
        print('\033[u', end='')
        print('\033[s', end='')
        string = ''
        for i in self.chess_board:
            for j in i:
                if j == None:
                    j = '#'
                else:
                    if j.team ^ self.turn % 2 == 1:
                        j = j.identifier.upper()
                    else:
                        j = j.identifier.lower()
                string += f'{j} '
            string += '\n'
        return string
    
    def lookup(self, working_piece:piece):
        indexs = []
        for i, row in enumerate(self.chess_board):
            for j, item in enumerate(row):
                if item != None:
                    if item.identifier == working_piece.identifier and item.team == (self.turn ^ 1):
                        indexs.append([i,j])
        return indexs

    
    def move(self, operation:str):
        take = False
        if 'x' in operation:
            take = True

        if (operation[0].lower() in self.piece_d) == 0:
            working_piece = self.piece_d['p']
            operation = 'p' + operation
        else:
            working_piece = self.piece_d[operation[0].lower()]
            working_piece.team = self.turn ^ 1
        
        piece_index = self.lookup(working_piece())
        position = self._conv([*(operation.lower())[-2:]])

        valid_piece_indices = self.validate(position, piece_index, take)

        if valid_piece_indices != []:
            index = valid_piece_indices[0]
            temp = self.chess_board[index[0]][index[1]]

            #make use of special function in piece class using flags (todo)
            if isinstance(temp, pawn): #means pawn can move 2 spaces only once
                temp.distance = 1

            self.chess_board[index[0]][index[1]] = None
            self.chess_board[position[0]][position[1]] = temp
            self.turn += 1

        else:
            print('Invalid Movement')


    def validate(self, position:list, piece_index:list, take:bool):

        # calculates relative position of target point from specifed piece(s)

        possible_vectors = [self._vector(i, position) for i in piece_index]
        possible_obj = [self.chess_board[x[0]][x[1]] for x in piece_index]

        valid_piece_indices = []
        valid_obj = []

        #checks to see if piece's movement reachs target using horizonal movement
        for pos, unit in enumerate(possible_obj):
            movements = unit.xmovement
            if take == True and unit.xxmovement != []:
                movements = unit.xxmovement
            for func in movements:
                if func(possible_vectors[pos][1]) == possible_vectors[pos][0] and abs(position[1] - piece_index[pos][1]) <= unit.distance: #checks if f(x) = y within range
                    valid_piece_indices.append(piece_index[pos])
                    valid_obj.append(unit)


        #checks to see if piece's movement reachs target using vertical movement
        for pos, unit in enumerate(possible_obj):
            movements = unit.ymovement
            if take == True and unit.xymovement != []:
                movements = unit.xymovement
            for func in movements:
                if func(possible_vectors[pos][0]) == possible_vectors[pos][1] and abs(position[0] - piece_index[pos][0]) <= unit.distance: #checks if f(y) = x within range
                    valid_piece_indices.append(piece_index[pos])
                    valid_obj.append(unit)


        if position in valid_piece_indices: # prevents moving to same square
            valid_piece_indices.remove(position)

        valid_piece_indices = list(set(tuple(sub) for sub in valid_piece_indices))

        #something's in the way? x-axis (piece blocking)
        
        if len(valid_piece_indices) == 1:
            return valid_piece_indices
        
        elif len(valid_piece_indices) > 1:
            for pos, unit in valid_obj:
                if unit.jump:
                    continue
                for i in range(position[1] - valid_piece_indices[pos][1]):
                    pass
                    return []

        else:
            return []
 

    def _vali(self, pos:list, targ:list, p:piece): #validates position
        raise NotImplemented
    
    def _vector(self, pos:list, targ:list):
        return [x[1] - x[0] for x in zip(pos, targ)]