from piece_class import piece


            
class pawn(piece):
    def __init__(self):
        super().__init__()
        self.ymovement = [lambda y: 0 if y < 0 and self.team == 0 else 999, lambda y: 0 if y > 0 and self.team == 1 else 999]
        self.xxmovement = [lambda x: -abs(x) if self.team == 0 else 999, lambda x: abs(x) if self.team == 1 else 999]
        self.distance = 2
        self.identifier = 'p'

    def m_add(self, move_desc):
        super().m_add(move_desc)
        self.distance = 1.5

    def promote(self):
        promote_piece = str(input('Promote piece: '))
        return promote_piece

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
        self.xmovement = [lambda x: 2*(x**2), lambda x: -2*(x**2), lambda x: 0.25*(x**2), lambda x: -0.25*(x**2)]
        self.distance = 3
        self.jump = True
        self.identifier = 'n'

class Queen(piece):
    def __init__(self):
        super().__init__()
        self.xmovement = [lambda x: x, lambda x: -x, lambda x: 0]
        self.ymovement = [lambda y: 0]
        self.identifier = 'q'

class King(piece):
    def __init__(self):
        super().__init__()
        self.xmovement = [lambda x: x, lambda x: -x, lambda x: 0]
        self.ymovement = [lambda y: 0]
        self.distance = 1.5
        self.identifier = 'k'